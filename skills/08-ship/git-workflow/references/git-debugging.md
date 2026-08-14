# Git Debugging Commands

Standard git commands for locating when and where a change was introduced. Load when
diagnosing a regression or tracing history.

```bash
git bisect start && git bisect bad HEAD && git bisect good <known-good>   # find the commit that broke it
git log --oneline -20                                                       # recent history
git diff HEAD~5..HEAD -- src/                                               # what changed in src
git blame src/services/task.ts                                              # who last touched a line
git log --grep="validation" --oneline                                       # commits matching a keyword
```
