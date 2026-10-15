"""通过真实 CLI 和临时文件系统验证发行包，不使用模拟调用。"""

import json
import os
from pathlib import Path
import re
import subprocess
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent
INSTALLER = ROOT / 'scripts' / 'install-skills.py'


class InstallationTests(unittest.TestCase):
    """验证资源完整性、幂等性和已有内容保护。"""

    def run_install(self, destination, *arguments):
        """运行实际安装程序并保留退出状态与诊断。"""
        return subprocess.run([sys.executable, str(INSTALLER), '--dest', str(destination), *arguments], capture_output=True, text=True)

    def test_all_skills_are_self_contained_and_idempotent(self):
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / 'skills'
            result = self.run_install(destination)
            self.assertEqual(result.returncode, 0, result.stderr)
            manifest = json.loads((ROOT / '.claude-plugin/plugin.json').read_text(encoding='utf-8'))
            expected = {Path(item).name for item in manifest['skills']}
            self.assertEqual({p.parent.name for p in destination.glob('*/SKILL.md')}, expected)
            self.assertEqual(len(list(destination.rglob('SKILL.md'))), len(expected))
            for adapter in destination.glob('*/agents/openai.yaml'):
                line = next(value for value in adapter.read_text(encoding='utf-8').splitlines() if value.strip().startswith('short_description:'))
                description = json.loads(line.split(':', 1)[1].strip())
                self.assertGreaterEqual(len(description), 25, str(adapter))
                self.assertLessEqual(len(description), 64, str(adapter))
            for path in destination.rglob('*.md'):
                text = path.read_text(encoding='utf-8')
                self.assertNotIn('${CLAUDE_PLUGIN_ROOT}', text, str(path))
                prose = re.sub(r'^\s*```[^\n]*\n.*?^\s*```\s*$', '', text, flags=re.M | re.S)
                prose = re.sub(r'`[^`\n]*`', '', prose)
                for value in re.findall(r'\]\(([^\s()]+)\)', prose):
                    if value.startswith('#') or re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', value):
                        continue
                    target = (path.parent / value.split('#')[0]).resolve()
                    self.assertTrue(target.is_relative_to(destination), f'{path}: {value}')
                    self.assertTrue(target.exists(), f'{path}: {value}')
            snapshot = {str(p): p.read_bytes() for p in destination.rglob('*') if p.is_file()}
            second = self.run_install(destination)
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertIn('0 of', second.stdout)
            self.assertEqual(snapshot, {str(p): p.read_bytes() for p in destination.rglob('*') if p.is_file()})

    def test_conflict_prevents_partial_install(self):
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary)
            conflict = destination / 'spec'
            conflict.mkdir()
            conflict.joinpath('SKILL.md').write_text('User-owned skill', encoding='utf-8')
            result = self.run_install(destination, '--skill', 'implement', '--skill', 'spec')
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse((destination / 'implement').exists())
            self.assertEqual(conflict.joinpath('SKILL.md').read_text(encoding='utf-8'), 'User-owned skill')

    def test_local_edits_are_preserved_even_with_replace(self):
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary)
            first = self.run_install(destination, '--skill', 'implement')
            self.assertEqual(first.returncode, 0, first.stderr)
            path = destination / 'implement' / 'SKILL.md'
            path.write_text('Local edit', encoding='utf-8')
            update = self.run_install(destination, '--skill', 'implement', '--replace')
            self.assertNotEqual(update.returncode, 0)
            self.assertEqual(path.read_text(encoding='utf-8'), 'Local edit')

    def test_managed_update_requires_replace_and_removes_old_resources(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            source = base / 'source'
            source.joinpath('scripts').mkdir(parents=True)
            shutil.copy2(INSTALLER, source / 'scripts/install-skills.py')
            source.joinpath('LICENSE').write_text('Test fixture license', encoding='utf-8')
            skill = source / 'skills/meta/example'
            skill.mkdir(parents=True)
            skill.joinpath('SKILL.md').write_text('---\nname: example\ndescription: Fixture\n---\n[Resource](note.md)\n', encoding='utf-8')
            skill.joinpath('note.md').write_text('Original resource', encoding='utf-8')
            destination = base / 'installed'
            command = [sys.executable, str(source / 'scripts/install-skills.py'), '--dest', str(destination)]
            initial = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(initial.returncode, 0, initial.stderr)
            skill.joinpath('SKILL.md').write_text('---\nname: example\ndescription: Updated fixture\n---\nUpdated workflow\n', encoding='utf-8')
            skill.joinpath('note.md').unlink()
            refused = subprocess.run(command, capture_output=True, text=True)
            self.assertNotEqual(refused.returncode, 0)
            self.assertTrue(destination.joinpath('example/note.md').exists())
            updated = subprocess.run(command + ['--replace'], capture_output=True, text=True)
            self.assertEqual(updated.returncode, 0, updated.stderr)
            self.assertFalse(destination.joinpath('example/note.md').exists())
            self.assertIn('Updated workflow', destination.joinpath('example/SKILL.md').read_text(encoding='utf-8'))

    def test_unknown_skill_and_source_destination_are_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / 'not-created'
            invalid = self.run_install(destination, '--skill', 'not-a-skill')
            self.assertNotEqual(invalid.returncode, 0)
            self.assertFalse(destination.exists())
        source = self.run_install(ROOT / '.agents' / 'skills', '--skill', 'spec')
        self.assertNotEqual(source.returncode, 0)

    def test_claude_hook_emits_current_rules_as_valid_json(self):
        bash = shutil.which('bash')
        if not bash:
            self.skipTest('Bash is required by the Claude SessionStart hook')
        environment = dict(os.environ, CLAUDE_PLUGIN_ROOT=str(ROOT))
        environment.pop('CURSOR_PLUGIN_ROOT', None)
        environment.pop('COPILOT_CLI', None)
        result = subprocess.run([bash, 'hooks/session-start'], cwd=ROOT, env=environment, capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(result.returncode, 0, result.stderr)
        context = json.loads(result.stdout)['hookSpecificOutput']['additionalContext']
        self.assertIn('48 skills', context)
        self.assertIn('confirm document paths', context)
        self.assertNotIn('EXTREMELY_IMPORTANT', context)


if __name__ == '__main__':
    unittest.main()
