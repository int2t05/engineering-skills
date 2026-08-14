#!/usr/bin/env bash
# Run behavioral evals for the engineering-skills pack.
# Usage: bash scripts/run-eval.sh [--skill tdd] [--case tdd-001] [--runs 3] [--no-baseline] [--model <id>]
# Matches validate-skills.sh style: bash entry, Python orchestration, exit code = failure count.
# Behavioral evals are slow + token-costly — run on demand, never as a CI gate.
set -euo pipefail
cd "$(dirname "$0")/.."

python scripts/run-eval.py "$@"
