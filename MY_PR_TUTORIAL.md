# My Personal PR Tutorial (Private Notes)

This is my personal step-by-step guide for creating branches, pushing changes, opening PRs, and merging safely.

## 1) Start from latest main

```bash
git checkout main
git pull origin main
```

## 2) Create a branch for the task

```bash
git checkout -b feature/<task-name>
```

Example:

```bash
git checkout -b feature/inventory-export
```

## 3) Work and commit

```bash
git add .
git commit -m "feat: add inventory export"
```

## 4) Push branch

```bash
git push -u origin feature/<task-name>
```

## 5) Open Pull Request

- Base: `main`
- Compare: `feature/<task-name>`
- PR description should include:
  - What changed
  - Why this change was needed
  - How it was tested
  - Screenshots (if UI changed)

## 6) Review and update PR

If changes are requested:

```bash
# edit files
git add .
git commit -m "fix: address review comments"
git push
```

PR updates automatically.

## 7) Merge strategy

Recommended:
- Squash and merge (clean history)
- Delete branch after merge

## 8) Keep main protected

Rules to keep:
- No direct push to `main`
- PR required
- At least 1 review before merge

## 9) Hotfix flow

```bash
git checkout main
git pull origin main
git checkout -b fix/<issue-name>
# fix
git add .
git commit -m "fix: ..."
git push -u origin fix/<issue-name>
```

Open PR to `main`.

## 10) Useful checks

```bash
git status
git branch -vv
git remote -v
git log --oneline -n 10
```
