#!/usr/bin/env bash
set -euo pipefail

PATTERN="${PATTERN:-sk-}"   # can override: PATTERN='sk-[A-Za-z0-9]+' bash script.sh
REMOTE="${REMOTE:-origin}"
BRANCH="${BRANCH:-main}"

echo "==> Repo: $(pwd)"
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || { echo "Not inside a git repo."; exit 1; }

# Require clean tree
if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "Working tree has uncommitted changes. Commit/stash first."
  exit 1
fi

# Backup branch
ts="$(date +%Y%m%d-%H%M%S)"
backup_branch="backup-before-secret-clean-$ts"
git branch "$backup_branch"
echo "==> Backup branch: $backup_branch"

# Ensure git-filter-repo exists
if ! command -v git-filter-repo >/dev/null 2>&1; then
  echo "==> Installing git-filter-repo..."
  if command -v python3 >/dev/null 2>&1; then
    python3 -m pip install --user git-filter-repo
  else
    python -m pip install --user git-filter-repo
  fi
  export PATH="$HOME/.local/bin:$PATH"
fi
command -v git-filter-repo >/dev/null 2>&1 || { echo "git-filter-repo not found on PATH."; exit 1; }

# Rewrite history: remove leaked files everywhere
echo "==> Rewriting history (removing ai_voice_utils.py from all commits)..."
git filter-repo --force \
  --path "ai_voice_utils.py" \
  --path "Mental Health Chatbot/ai_voice_utils.py" \
  --invert-paths

# Re-add safe replacements (optional but convenient)
safe_py='import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("Missing OPENAI_API_KEY environment variable")
'
printf "%s\n" "$safe_py" > "ai_voice_utils.py"
if [ -d "Mental Health Chatbot" ]; then
  mkdir -p "Mental Health Chatbot"
  printf "%s\n" "$safe_py" > "Mental Health Chatbot/ai_voice_utils.py"
fi

# Ensure .env ignored
touch .gitignore
grep -qxF ".env" .gitignore || echo ".env" >> .gitignore
grep -qxF "*.env" .gitignore || echo "*.env" >> .gitignore
grep -qxF ".env.*" .gitignore || echo ".env.*" >> .gitignore

git add -A
git commit -m "Remove leaked secret from history; add safe utils + ignore .env" || true

echo "==> Scan WORKING TREE for '$PATTERN'..."
if git grep -nI --no-color -e "$PATTERN" -- .; then
  echo "!! Found '$PATTERN' in working tree. Remove it before pushing."
  exit 1
else
  echo "==> OK: none found in working tree."
fi

echo "==> Scan ALL COMMITS for '$PATTERN' (this can take a bit on big repos)..."
# This searches each commit snapshot (tree) for the pattern.
# We chunk commits to avoid OS command-length limits.
set +e
results="$(git rev-list --all \
  | xargs -n 50 git grep -nI --no-color -e "$PATTERN" 2>/dev/null)"
status=$?
set -e

if [ "$status" -eq 0 ] && [ -n "$results" ]; then
  echo "!! Found '$PATTERN' somewhere in history:"
  echo "$results"
  echo
  echo "Fix: remove/rotate the key, then remove the file/secret from history (filter-repo already did for the two paths)."
  echo "If this is still triggering, the secret exists in OTHER files/paths—search above output and clean those too."
  exit 1
fi
echo "==> OK: none found in any commit snapshot."

echo "==> Force-pushing rewritten history to $REMOTE/$BRANCH..."
git push --force-with-lease "$REMOTE" "$BRANCH"
echo "✅ Done."