#!/bin/bash
# ai-collab-sync.sh
# Syncs a local markdown collaboration folder to GitHub.
# Run manually or drop in /etc/cron.daily/ for automatic daily sync.
#
# SETUP:
# 1. Set the three variables below
# 2. chmod +x ai-collab-sync.sh
# 3. For manual run: bash ai-collab-sync.sh
# 4. For auto daily: copy to /etc/cron.daily/ and chmod +x
#    sudo cp ai-collab-sync.sh /etc/cron.daily/ai-collab-sync
#    sudo chmod +x /etc/cron.daily/ai-collab-sync
#
# VARIABLES:
# COLLAB_REPO  - full path to your local git repo folder
# GIT_BRANCH   - branch name (main or master, check with: git branch)
# SYNC_USER    - your linux username (who owns the repo)
#                only matters when running as root via cron
#                leave blank if running manually as yourself

COLLAB_REPO="/pathto/your/FILES/"
GIT_BRANCH="main"
SYNC_USER=""

# --- do not edit below this line ---

SYNC_LOG="/tmp/ai-collab-sync.log"

run_sync() {
    echo "[$(date)] Starting sync..."
    cd "$COLLAB_REPO" || { echo "ERROR: could not cd to $COLLAB_REPO"; exit 1; }
    git stash
    git pull --rebase origin "$GIT_BRANCH"
    git stash pop
    git add -A
    git diff --cached --quiet || {
        git commit -m "sync: $(date +%Y-%m-%d\ %H:%M)"
        git push origin "$GIT_BRANCH"
    }
    echo "[$(date)] Done."
}

if [ -n "$SYNC_USER" ] && [ "$(whoami)" = "root" ]; then
    su - "$SYNC_USER" -c "bash $0" >> "$SYNC_LOG" 2>&1
else
    run_sync >> "$SYNC_LOG" 2>&1
fi
