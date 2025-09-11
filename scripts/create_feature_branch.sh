#!/bin/bash
# This script creates a new feature branch from the main branch.
# Usage: ./create_feature_branch.sh
set -e

# === configuration ===
TARGET_BRANCH="main"
PR_BRANCH="auto/update-csv-changes"
COMMIT_MESSAGE="Update CSV changes"
PR_TITLE="Automated Update of CSV Changes"
PR_BODY="This pull request contains automated updates to the CSV files."
# =====================

# === Files/directories to watch ===
WATCHED_PATHS=("data/")
# ==================================

# === Helper functions to check for changes ===
function has_changes() {
  for path in "${WATCHED_PATHS[@]}"; do
    if [ -n "$(git status --porcelain "$path")" ]; then
      return 0
    fi
  done
  return 1
}
# ========================================

# === Main script logic ===

if [ "$(git rev-parse --abbrev-ref HEAD)" != "$TARGET_BRANCH" ]; then
    echo "🔄 Switching to '$TARGET_BRANCH' branch."
    git checkout "$TARGET_BRANCH" || { echo "Error: Failed to switch to '$TARGET_BRANCH' branch."; exit 1; }
else
    echo "✅ Already on '$TARGET_BRANCH' branch."
fi

# Fetch latest changes from remote
git fetch origin $TARGET_BRANCH

# Check for changes in watched paths
if has_changes; then
    echo "🔍 Changes detected in watched files in $WATCHED_PATHS."

    echo "Create a new branch $PR_BRANCH."
    git checkout -b "$PR_BRANCH"

    echo "Stage and commit all changes."
     COMMIT_MSG="$COMMIT_MESSAGE - $(date +'%Y-%m-%d')"
 
    git add .
    git commit -m "$COMMIT_MSG"

    # Push the new branch to remote
    git push -u origin "$PR_BRANCH"

    echo "✅ Changes have been committed and pushed to branch '$PR_BRANCH'."
    git checkout "$TARGET_BRANCH"
    echo "Switched back to '$TARGET_BRANCH' branch."

    # Note: The following PR creation step requires GitHub CLI (gh) to be installed and authenticated.
    # Uncomment the lines below if you want to create a PR automatically.
    # echo "Creating a pull request..."
    # Create a pull request using GitHub CLI
    # gh pr create --base "$TARGET_BRANCH" --head "$PR_BRANCH" \
    #     --title "$PR_TITLE" --body "$PR_BODY"

    # echo "✅ Pull request has been created."
    
else
    echo "ℹ️ No changes in watched files. No PR created."
fi
