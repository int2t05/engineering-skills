#!/usr/bin/env python3
"""将选定技能和依赖资源打包为可独立发现的本地技能目录。"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent
LINK = re.compile(r'(?<=\]\()([^\s()]+)(?=\))')
OWNER = '.engineering-skills.json'


def file_hashes(folder):
    """记录实际文件内容，用于保护安装后的人工修改。"""
    return {
        p.relative_to(folder).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(folder.rglob('*')) if p.is_file() and p.name != OWNER
    }


def build_skill(source, destination):
    """复制技能并递归补齐外部引用，发行内容不依赖原始仓库。"""
    shutil.copytree(source, destination, ignore=shutil.ignore_patterns('__pycache__', '*.pyc', 'node_modules', '.git'))
    queue = [(source / p.relative_to(destination), p) for p in destination.rglob('*.md')]
    visited = set()
    while queue:
        original, output = queue.pop()
        if original in visited:
            continue
        visited.add(original)
        text = original.read_text(encoding='utf-8')

        def rewrite(match):
            value = match.group()
            if value.startswith('#') or re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', value):
                return value
            target_text, separator, fragment = value.partition('#')
            target = (original.parent / unquote(target_text)).resolve()
            if not target.is_relative_to(ROOT):
                raise ValueError(f'Reference escapes source repository: {original}: {value}')
            if not target.exists():
                raise ValueError(f'Missing resource: {original}: {value}')
            suffix = separator + fragment
            if target.is_relative_to(source):
                installed = destination / target.relative_to(source)
            elif target.name == 'SKILL.md':
                # 跨技能导航保留为源码链接，避免嵌套技能被重复发现。
                return 'https://github.com/int2t05/engineering-skills/blob/main/' + target.relative_to(ROOT).as_posix() + suffix
            else:
                installed = destination / '_pack' / target.relative_to(ROOT)
                if target.is_dir():
                    raise ValueError(f'External directory reference needs an explicit file: {value}')
                if not installed.exists():
                    installed.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(target, installed)
                    if target.suffix == '.md':
                        queue.append((target, installed))
            return os.path.relpath(installed, output.parent).replace('\\', '/') + suffix

        # 示例代码里的虚构链接不是资源依赖，不参与发行链接解析。
        chunks = re.split(r'(^[ \t]*(?:`{3,}|~{3,})[^\n]*\n.*?^[ \t]*(?:`{3,}|~{3,})[ \t]*$|`+[^`\n]*`+)', text, flags=re.M | re.S)
        output.write_text(''.join(chunk if index % 2 else LINK.sub(rewrite, chunk) for index, chunk in enumerate(chunks)), encoding='utf-8', newline='\n')
    shutil.copy2(ROOT / 'LICENSE', destination / 'LICENSE')


def install(destination, names, replace=False):
    """先完整构建并检查冲突，再安装；只更新未被人工修改的本包目录。"""
    destination = destination.resolve()
    if destination.is_relative_to(ROOT):
        raise ValueError('Use a destination outside the source checkout to avoid duplicate skill discovery')
    sources = {p.parent.name: p.parent for p in ROOT.glob('skills/*/*/SKILL.md')}
    unknown = set(names) - sources.keys()
    if unknown:
        raise ValueError('Unknown skills: ' + ', '.join(sorted(unknown)))
    selected = names or sorted(sources)
    with tempfile.TemporaryDirectory(prefix='engineering-skills-build-') as temporary:
        staging = Path(temporary)
        planned = []
        for name in selected:
            built = staging / name
            build_skill(sources[name], built)
            hashes = file_hashes(built)
            target = destination / name
            if target.exists() or target.is_symlink():
                if target.is_symlink() or not target.is_dir():
                    raise ValueError(f'Refusing to overwrite non-directory or symlink: {target}')
                marker = target / OWNER
                if not marker.is_file():
                    raise ValueError(f'Existing skill is not managed by this installer: {target}')
                previous = json.loads(marker.read_text(encoding='utf-8'))
                if not isinstance(previous, dict) or previous.get('owner') != 'engineering-skills':
                    raise ValueError(f'Unexpected ownership: {target}')
                actual = file_hashes(target)
                if actual != previous.get('files'):
                    raise ValueError(f'Installed skill has local changes; preserve them before updating: {target}')
                if actual == hashes:
                    continue
                if not replace:
                    raise ValueError(f'Update requires --replace: {target}')
            built.joinpath(OWNER).write_text(json.dumps({'owner': 'engineering-skills', 'files': hashes}, indent=2) + '\n', encoding='utf-8')
            planned.append((built, target))
        destination.mkdir(parents=True, exist_ok=True)
        for built, target in planned:
            # 目标已验证归属和内容，暂存旧目录以便单项安装失败时恢复。
            backup = staging / (target.name + '-previous')
            if target.exists():
                shutil.move(str(target), str(backup))
            try:
                shutil.copytree(built, target)
            except Exception:
                if target.exists():
                    shutil.rmtree(target)
                if backup.exists():
                    shutil.move(str(backup), str(target))
                raise
    return len(planned), len(selected)


def main():
    """显式目标支持任意宿主，默认使用 Codex 的用户级发现目录。"""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dest', type=Path, default=Path.home() / '.agents' / 'skills')
    parser.add_argument('--skill', action='append', default=[], help='Repeat to select multiple skills; default: all')
    parser.add_argument('--replace', action='store_true', help='Update installer-owned, unmodified skills')
    args = parser.parse_args()
    try:
        changed, total = install(args.dest, sorted(set(args.skill)), args.replace)
    except (ValueError, OSError, json.JSONDecodeError) as error:
        print(str(error), file=sys.stderr)
        return 1
    print(f'Installed/updated {changed} of {total} skills in {args.dest.resolve()}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
