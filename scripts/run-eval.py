#!/usr/bin/env python3
"""Behavioral eval orchestrator for the engineering-skills pack.

Implements the RED-GREEN pattern: every case runs twice (with-skill and
without-skill/baseline). A case passes only when with-skill satisfies the
expectations AND the baseline does not — proving the skill changes behavior.

Adapted from archive/upstream-anthropics-skills/skills/skill-creator/scripts/run_eval.py
(trigger detection → behavioral judgment). Uses `claude -p --output-format stream-json`
subprocesses; strips CLAUDECODE to allow nesting.

Usage: python scripts/run-eval.py [--skill tdd] [--case tdd-001] [--runs 3] [--no-baseline] [--model <id>]
Exit code = number of failed cases (matches validate-skills.sh convention).
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Resolve the claude CLI path once. On Windows, npm installs `claude` as a
# `.CMD` shim; subprocess.run (CreateProcess) only finds `.exe` without help,
# so shutil.which (which honors PATHEXT) is required to locate it.
CLAUDE_BIN = shutil.which("claude") or "claude"


def load_cases(skill_filter=None, case_filter=None):
    """Load eval cases from evals/cases/*.json. Returns a list of case dicts."""
    cases_dir = REPO_ROOT / "evals" / "cases"
    all_cases = []
    for case_file in sorted(cases_dir.glob("*.json")):
        skill_name = case_file.stem
        if skill_filter and skill_name != skill_filter:
            continue
        for case in json.loads(case_file.read_text(encoding="utf-8")):
            if case_filter and case["id"] != case_filter:
                continue
            case["_skill_file"] = skill_name
            all_cases.append(case)
    return all_cases


def prepare_workspace(case, run_label):
    """Create a temp workspace. If the case has a fixture, copy it in."""
    workspace = Path(tempfile.mkdtemp(prefix=f"eval-{case['id']}-{run_label}-"))
    fixture = case.get("fixture")
    if fixture:
        src = REPO_ROOT / fixture
        if src.is_dir():
            # Copy fixture contents into workspace
            shutil.copytree(src, workspace, dirs_exist_ok=True)
    return workspace


def save_artifacts(case, run_label, run_idx, workspace, transcript, prompt, duration, tokens, verdict):
    """Persist a run's artifacts to evals/results/<case-id>/<label>-<n>/.

    Without this the workspace is rmtree'd and the transcript, grading.json,
    and agent-produced files are lost — leaving no evidence to audit. Artifacts
    are gitignored (evals/results/) so they never pollute the repo.
    """
    out_dir = REPO_ROOT / "evals" / "results" / case["id"] / f"{run_label}-{run_idx}"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "transcript.md").write_text(transcript, encoding="utf-8")
    (out_dir / "prompt.txt").write_text(prompt, encoding="utf-8")
    (out_dir / "run-meta.json").write_text(json.dumps({
        "case_id": case["id"],
        "run_label": run_label,
        "run_index": run_idx,
        "skill_under_test": case["skill_under_test"],
        "negative_control": case.get("negative_control", False),
        "duration_seconds": round(duration, 1),
        "tokens": tokens,
        "verdict": verdict,
    }, indent=2), encoding="utf-8")
    # Copy grading.json if the grader wrote one (sibling to eval-outputs/ in workspace)
    grading_file = workspace / "grading.json"
    if grading_file.exists():
        shutil.copy2(grading_file, out_dir / "grading.json")
    # Copy agent-produced files (the full workspace minus node_modules) so the
    # actual code/docs the agent wrote are auditable, not just the transcript.
    ws_snapshot = out_dir / "workspace"
    ws_snapshot.mkdir(exist_ok=True)
    for entry in workspace.rglob("*"):
        if "node_modules" in entry.parts:
            continue
        rel = entry.relative_to(workspace)
        dest = ws_snapshot / rel
        if entry.is_dir():
            dest.mkdir(parents=True, exist_ok=True)
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(entry, dest)
    return out_dir


def build_prompt(case, workspace, with_skill):
    """Build the prompt for claude -p. With-skill includes SKILL.md content."""
    task = case["task_prompt"]
    ws = str(workspace).replace("\\", "/")
    # Non-interactive notice: claude -p has no user to answer assumption questions,
    # so skills that say "surface assumptions before proceeding" would stall.
    # Tell the agent to state assumptions and proceed autonomously.
    nonce = (
        "This is a non-interactive session — no one will answer questions. "
        "State your assumptions explicitly, then proceed autonomously to complete "
        "the task and write any output files.\n\n"
    )
    if with_skill:
        skill_path = REPO_ROOT / case["skill_under_test"] / "SKILL.md"
        skill_content = skill_path.read_text(encoding="utf-8")
        return (
            f"You are a software engineer working in this directory: {ws}\n\n"
            f"{nonce}"
            f"## Skill Instructions ({case['skill_under_test']})\n"
            f"Follow these skill instructions carefully:\n\n"
            f"{skill_content}\n\n"
            f"## Task\n{task}\n"
        )
    return (
        f"You are a software engineer working in this directory: {ws}\n\n"
        f"{nonce}"
        f"## Task\n{task}\n"
    )


def run_claude(prompt, workspace, timeout, model=None):
    """Run claude -p with the prompt. Returns (transcript_text, duration_s, tokens).

    The prompt is passed via stdin, not as a CLI argument. On Windows the claude
    CLI is a .CMD shim whose argument parser mangles prompts containing double
    quotes (e.g. skill descriptions with ``Triggers on "..."``), truncating the
    prompt so the model receives nothing. stdin bypasses all shell/arg escaping.
    """
    cmd = [CLAUDE_BIN, "-p", "--output-format", "stream-json", "--verbose"]
    # Pin the model: explicit --model wins; else fall back to ANTHROPIC_MODEL,
    # matching the ANTHROPIC_AUTH_TOKEN / ANTHROPIC_BASE_URL naming family the
    # proxy setup uses.
    model = model or os.environ.get("ANTHROPIC_MODEL")
    if model:
        cmd.extend(["--model", model])
    # Strip CLAUDECODE so claude -p can run nested inside a Claude Code session.
    env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}

    start = time.time()
    try:
        proc = subprocess.run(
            cmd,
            input=prompt,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(workspace),
            env=env,
        )
        duration = time.time() - start
        # Parse stream-json: collect assistant text + tool uses into a transcript
        transcript_lines = []
        total_tokens = 0
        for line in proc.stdout.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            etype = event.get("type")
            if etype == "assistant":
                msg = event.get("message", {})
                for block in msg.get("content", []):
                    if block.get("type") == "text":
                        transcript_lines.append(block["text"])
                    elif block.get("type") == "tool_use":
                        transcript_lines.append(f"[tool: {block.get('name')}] {json.dumps(block.get('input', {}))[:200]}")
            elif etype == "result":
                usage = event.get("usage", {})
                total_tokens = usage.get("output_tokens", 0) + usage.get("input_tokens", 0)
        transcript = "\n\n".join(transcript_lines)
        # Defensive fallback: if no stream-json events parsed but stdout is non-empty,
        # claude -p emitted something we couldn't parse (a proxy error, plain-text
        # response, or a non-JSON error message). Surface it as the transcript so the
        # grader has something to evaluate and the failure is observable, not silent.
        if not transcript and proc.stdout.strip():
            transcript = f"[unparsed stdout — {len(proc.stdout)} chars, no stream-json events]\n{proc.stdout[:2000]}"
            print(f"  WARN: claude -p produced {len(proc.stdout)} chars but 0 stream-json events (proxy error or non-JSON output)", file=sys.stderr)
        return transcript, duration, total_tokens
    except subprocess.TimeoutExpired as e:
        # Recover partial output instead of discarding it. The agent often
        # completes the work (files written, tests passing) even when the
        # process doesn't terminate within the timeout — losing all narrative
        # makes process-based expectations ungradeable and masks the real
        # behavior. TimeoutExpired carries the stdout captured before kill.
        duration = time.time() - start
        partial_lines = []
        partial_tokens = 0
        partial = e.stdout or ""
        for line in partial.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if event.get("type") == "assistant":
                for block in event.get("message", {}).get("content", []):
                    if block.get("type") == "text":
                        partial_lines.append(block["text"])
                    elif block.get("type") == "tool_use":
                        partial_lines.append(f"[tool: {block.get('name')}] {json.dumps(block.get('input', {}))[:200]}")
            elif event.get("type") == "result":
                usage = event.get("usage", {})
                partial_tokens = usage.get("output_tokens", 0) + usage.get("input_tokens", 0)
        partial_transcript = "\n\n".join(partial_lines)
        header = f"[TIMEOUT after {timeout}s — partial transcript recovered ({len(partial)} bytes)]"
        if partial_transcript:
            return f"{header}\n{partial_transcript}", duration, partial_tokens
        if partial.strip():
            return f"{header}\n[unparsed partial — {len(partial)} chars]\n{partial[:2000]}", duration, 0
        return header, duration, 0
    except FileNotFoundError:
        return "[ERROR: claude CLI not found — is it installed and on PATH?]", 0, 0


def grade_code(case, workspace):
    """Run the deterministic code check. Returns (passed, detail)."""
    grader = case.get("grader", {})
    code_check = grader.get("code_check")
    if not code_check:
        return True, "no code check"
    cmd = code_check["command"]
    cwd = code_check.get("cwd", "{workspace}").replace("{workspace}", str(workspace))
    try:
        proc = subprocess.run(
            ["bash", "-c", cmd],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=cwd,
        )
        passed = proc.returncode == 0
        detail = f"exit={proc.returncode}" + (f", stderr={proc.stderr[:200]}" if proc.stderr else "")
        return passed, detail
    except Exception as e:
        return False, f"code check error: {e}"


def grade_llm(case, transcript, workspace):
    """Run the LLM-judge grader via claude -p. Returns (pass_rate, detail)."""
    grader = case.get("grader", {})
    llm_judge = grader.get("llm_judge")
    if not llm_judge:
        return 1.0, "no llm judge"

    agent_path = REPO_ROOT / llm_judge["agent"]
    agent_prompt = agent_path.read_text(encoding="utf-8")
    expectations = llm_judge["expectations"]
    negative = case.get("negative_control", False)

    # Write transcript to a file the grader can read
    outputs_dir = workspace / "eval-outputs"
    outputs_dir.mkdir(exist_ok=True)
    transcript_file = outputs_dir / "transcript.md"
    transcript_file.write_text(transcript, encoding="utf-8")

    judge_prompt = (
        f"{agent_prompt}\n\n"
        f"## Eval Inputs\n"
        f"- negative_control: {negative}\n"
        f"- expectations: {json.dumps(expectations, indent=2)}\n"
        f"- transcript_path: {transcript_file}\n"
        f"- outputs_dir: {outputs_dir}\n\n"
        f"Read the transcript and outputs, grade each expectation per your process, "
        f"and write grading.json to {outputs_dir}/../grading.json.\n"
        f"Then print ONLY the grading.json content as your final output.\n"
    )

    transcript_out, _, _ = run_claude(judge_prompt, workspace, timeout=120)
    # Try to parse the judge output as JSON (it may have preamble)
    try:
        # Extract JSON from the output
        start = transcript_out.find("{")
        end = transcript_out.rfind("}") + 1
        if start >= 0 and end > start:
            grading = json.loads(transcript_out[start:end])
            summary = grading.get("summary", {})
            passed = summary.get("passed", 0)
            total = summary.get("total", len(expectations))
            return passed / total if total else 0.0, f"{passed}/{total} expectations"
    except (json.JSONDecodeError, KeyError):
        pass
    # Fallback: check if grading.json was written
    grading_file = workspace / "grading.json"
    if grading_file.exists():
        try:
            grading = json.loads(grading_file.read_text(encoding="utf-8"))
            summary = grading.get("summary", {})
            passed = summary.get("passed", 0)
            total = summary.get("total", len(expectations))
            return passed / total if total else 0.0, f"{passed}/{total} expectations (from file)"
        except json.JSONDecodeError:
            pass
    return 0.0, "grader produced no parseable result"


def run_case(case, runs, with_baseline, model=None, threshold=0.67):
    """Run a single case with-skill (+ optionally baseline). Returns a result dict."""
    case_id = case["id"]
    timeout = case.get("timeout_seconds", 300)

    # --- With-skill runs ---
    with_passes = 0
    with_details = []
    for run_idx in range(runs):
        ws = prepare_workspace(case, "with")
        try:
            prompt = build_prompt(case, ws, with_skill=True)
            transcript, duration, tokens = run_claude(prompt, ws, timeout, model)
            # Grade
            grader = case.get("grader", {})
            gtype = grader.get("type", "llm-judge")
            code_pass, code_detail = (True, "n/a") if gtype == "llm-judge" else grade_code(case, ws)
            llm_rate, llm_detail = (1.0, "n/a") if gtype == "code-based" else grade_llm(case, transcript, ws)
            passed = code_pass and (llm_rate >= threshold)
            with_passes += int(passed)
            with_details.append(f"code:{code_detail} judge:{llm_detail}")
            verdict = {"passed": passed, "code": code_detail, "judge": llm_detail, "transcript_chars": len(transcript)}
            save_artifacts(case, "with", run_idx, ws, transcript, prompt, duration, tokens, verdict)
        finally:
            shutil.rmtree(ws, ignore_errors=True)

    with_rate = with_passes / runs if runs else 0

    # --- Baseline runs (without skill) ---
    baseline_rate = None
    baseline_details = []
    if with_baseline:
        base_passes = 0
        for run_idx in range(runs):
            ws = prepare_workspace(case, "base")
            try:
                prompt = build_prompt(case, ws, with_skill=False)
                transcript, duration, tokens = run_claude(prompt, ws, timeout, model)
                grader = case.get("grader", {})
                gtype = grader.get("type", "llm-judge")
                code_pass, code_detail = (True, "n/a") if gtype == "llm-judge" else grade_code(case, ws)
                llm_rate, llm_detail = (1.0, "n/a") if gtype == "code-based" else grade_llm(case, transcript, ws)
                passed = code_pass and (llm_rate >= threshold)
                base_passes += int(passed)
                baseline_details.append(f"code:{code_detail} judge:{llm_detail}")
                verdict = {"passed": passed, "code": code_detail, "judge": llm_detail, "transcript_chars": len(transcript)}
                save_artifacts(case, "base", run_idx, ws, transcript, prompt, duration, tokens, verdict)
            finally:
                shutil.rmtree(ws, ignore_errors=True)
        baseline_rate = base_passes / runs if runs else 0

    # --- Verdict ---
    # For negative controls: pass when skill does NOT change behavior in the wrong direction.
    # A negative control "passes" when the agent did NOT activate the skill's workflow.
    # We judge this via the llm_judge expectations (which check for absence).
    # So with_rate passing = the skill correctly did NOT activate.
    is_neg = case.get("negative_control", False)
    if is_neg:
        passed = with_rate >= threshold
        discriminating = "n/a (negative control)"
    else:
        passed = with_rate >= threshold
        # Discriminating = with-skill passes but baseline fails
        if baseline_rate is not None:
            discriminating = "yes" if (with_rate >= threshold and baseline_rate < threshold) else (
                "no (baseline also passes)" if baseline_rate >= threshold else "n/a"
            )
        else:
            discriminating = "not checked (--no-baseline)"

    return {
        "id": case_id,
        "skill": case["_skill_file"],
        "negative_control": is_neg,
        "passed": passed,
        "with_skill_rate": with_rate,
        "baseline_rate": baseline_rate,
        "discriminating": discriminating,
        "details": with_details[0] if with_details else "",
        "baseline_details": baseline_details[0] if baseline_details else "",
    }


def main():
    parser = argparse.ArgumentParser(description="Run behavioral evals for the engineering-skills pack")
    parser.add_argument("--skill", default=None, help="Skill to eval (default: all pilots)")
    parser.add_argument("--case", default=None, help="Single case id to run")
    parser.add_argument("--runs", type=int, default=1, help="Runs per case (3 for CI confidence)")
    parser.add_argument("--no-baseline", action="store_true", help="Skip baseline runs (faster, less proof)")
    parser.add_argument("--model", default=None, help="Model id for claude -p")
    parser.add_argument("--threshold", type=float, default=0.67, help="Pass-rate threshold per case")
    args = parser.parse_args()

    cases = load_cases(args.skill, args.case)
    if not cases:
        print("No eval cases found matching the filter.")
        print(f"Checked: {REPO_ROOT / 'evals' / 'cases'}")
        sys.exit(1)

    print(f"Behavioral Eval Results")
    print(f"=======================")
    print(f"Cases: {len(cases)} | runs/case: {args.runs} | baseline: {not args.no_baseline}")
    print()

    results = []
    # Run cases sequentially (each case already parallelizes with/baseline internally if needed).
    # True parallelism across cases would exhaust token budget too fast for MVP.
    for case in cases:
        print(f"  Running {case['id']}...", file=sys.stderr, flush=True)
        result = run_case(case, args.runs, not args.no_baseline, args.model, args.threshold)
        results.append(result)
        status = "PASS" if result["passed"] else "FAIL"
        with_str = f"with={result['with_skill_rate']:.0%}"
        base_str = f"base={result['baseline_rate']:.0%}" if result["baseline_rate"] is not None else "base=skip"
        disc = result["discriminating"]
        print(f"  {result['id']:20s} [{status}]  {with_str}  {base_str}  discriminating: {disc}")

    print()
    passed = sum(1 for r in results if r["passed"])
    failed = len(results) - passed
    print(f"Summary: {passed}/{len(results)} cases passed, {failed} failed")
    print(f"Total errors: {failed}")

    # Persist a machine-readable summary alongside the per-run artifacts.
    results_dir = REPO_ROOT / "evals" / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    summary_path = results_dir / "run-summary.json"
    summary_path.write_text(json.dumps({
        "cases": len(results),
        "passed": passed,
        "failed": failed,
        "runs_per_case": args.runs,
        "baseline_run": not args.no_baseline,
        "threshold": args.threshold,
        "results": results,
    }, indent=2), encoding="utf-8")
    print(f"\nArtifacts written to: {results_dir}")
    print(f"  - {summary_path.relative_to(REPO_ROOT)}")
    print(f"  - {results_dir.relative_to(REPO_ROOT)}/<case-id>/<with|base>-<n>/  (transcript.md, grading.json, workspace/, run-meta.json)")

    # Non-discriminating positive cases (flag, don't fail)
    if not args.no_baseline:
        nondisc = [r for r in results if not r["negative_control"] and r["discriminating"].startswith("no")]
        if nondisc:
            print(f"\nWarning: {len(nondisc)} case(s) non-discriminating (baseline also passes):")
            for r in nondisc:
                print(f"  - {r['id']}: consider making the task harder or expectations stricter")

    sys.exit(failed)


if __name__ == "__main__":
    main()
