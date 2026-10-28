#!/usr/bin/env bash
# Creates one public GitHub repo per folder and pushes the code.
# Needs: git and GitHub CLI (gh), and you must be logged in (run: gh auth login)
set -e
gh auth status >/dev/null 2>&1 || { echo "Run 'gh auth login' first."; exit 1; }
for d in */; do
  name=${d%/}
  echo "== $name"
  (
    cd "$name"
    rm -rf .git
    git init -q -b main
    git add .
    git commit -q -m "Initial commit"
    gh repo create "$name" --public --source=. --remote=origin --push
  )
done
echo "Done. Your repos are at https://github.com/$(gh api user -q .login)?tab=repositories"
