# buggy-diff fixture

A pre-merge change in `src/userService.js` for the `code-review` skill eval.
The file contains several issues of varying severity — the reviewer must find
them, not be told what they are.

## Setup

This fixture is a git repo with the change already committed on a feature
branch. The agent reviews `git diff main..feature` (or just reads the file).
See `cases/code-review.json`.
