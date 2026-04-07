#!/usr/bin/env python3
"""
wipe-and-recompile.py

Nuclear reset of wiki/ directory.
Backs up the current wiki/ to a timestamped directory and git branch,
then re-creates the wiki skeleton.
raw/ and PROTECTED_PATHS are NEVER touched.

Usage:
  python wipe-and-recompile.py [--dry-run]
  python wipe-and-recompile.py [--confirm]    # actually perform the wipe

WARNING: This is a destructive operation on wiki/ ONLY.
raw/ is always preserved. Thesis files in raw/ are protected.

Requires: sudo (for chattr operations — not used in this script,
          but raw-ingest requires it separately)
"""

import shutil
import subprocess
import datetime
import sys
import os
from pathlib import Path

VAULT = Path.home() / "Documents/x1n4te-workstation"
WIKI = VAULT / "wiki"
RAW = VAULT / "raw"

TIMESTAMP = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
BACKUP_DIR = VAULT / f"wiki.backup.{TIMESTAMP}"
GIT_BRANCH = f"wiki-reset-{TIMESTAMP}"

# PATHS THAT THIS SCRIPT WILL NEVER TOUCH
# These are verified before ANY destructive operation.
PROTECTED_PATHS = [
    str(VAULT / "raw"),
    str(VAULT / "raw/software-dev/wims-bfp/thesis"),
    str(VAULT / "raw/software-dev/wims-bfp/thesis-chapters"),
    str(VAULT / "HERMES.md"),
    str(VAULT / "workflows"),
    str(VAULT / "scripts"),
    str(VAULT / "sessions"),
    str(VAULT / "conflict-queue"),
]


def is_protected(path_str: str) -> bool:
    """Return True if this path is protected and must not be wiped."""
    path_str = str(path_str)
    for protected in PROTECTED_PATHS:
        if path_str == protected or path_str.startswith(protected + "/"):
            return True
    return False


def check_no_protected_in_wiki():
    """Verify that no protected path is inside wiki/ that we would wipe."""
    for item in WIKI.rglob("*"):
        if is_protected(item):
            print(f"ERROR: Protected path found inside wiki/: {item}")
            print("Aborting. This should never happen.")
            sys.exit(1)
    print("✓ No protected paths found inside wiki/")


def get_git_root() -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=VAULT,
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print("ERROR: Not a git repository. Run: cd ~/Documents/x1n4te-workstation && git init")
        sys.exit(1)
    return Path(result.stdout.strip())


def create_backup():
    """Move current wiki/ to backup directory."""
    if not WIKI.exists():
        print("WARNING: wiki/ does not exist — nothing to back up")
        return False

    check_no_protected_in_wiki()

    size = sum(f.stat().st_size for f in WIKI.rglob("*") if f.is_file())
    print(f"Backing up wiki/ → {BACKUP_DIR.name}/")
    print(f"  Total size: {size / 1024 / 1024:.1f} MB")
    print(f"  Total files: {sum(1 for _ in WIKI.rglob('*') if _.is_file())}")

    shutil.move(str(WIKI), str(BACKUP_DIR))
    print(f"✓ Backup created: {BACKUP_DIR}")
    return True


def git_commit_backup():
    """Commit the backup to a dedicated git branch."""
    git = get_git_root()

    # Create and push backup branch
    subprocess.run(["git", "checkout", "-b", GIT_BRANCH], cwd=git, check=False)
    subprocess.run(
        ["git", "add", str(BACKUP_DIR.relative_to(VAULT))],
        cwd=git, check=True
    )
    result = subprocess.run(
        ["git", "commit", "-m", f"WIP reset: corrupted wiki backed up to {BACKUP_DIR.name}"],
        cwd=git,
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print(f"✓ Backup committed to branch: {GIT_BRANCH}")
        print(f"  To restore: git checkout {GIT_BRANCH}")
    else:
        print(f"WARNING: git commit failed: {result.stderr}")

    # Switch back to master
    subprocess.run(["git", "checkout", "master"], cwd=git, check=False)


def recreate_skeleton():
    """Re-create the wiki/ directory skeleton (empty — no content)."""
    WIKI.mkdir(parents=True, exist_ok=True)

    subdirs = [
        "mocs",
        "sources/ai-research",
        "sources/cybersecurity",
        "sources/software-dev",
        "sources/biomechanics",
        "concepts",
        "entities",
        "analyses",
        "sessions",
    ]

    for d in subdirs:
        (WIKI / d).mkdir(parents=True, exist_ok=True)

    # Re-create empty index, log, overview
    for fname in ["index.md", "log.md", "overview-state-of-field.md"]:
        fpath = WIKI / fname
        if not fpath.exists():
            fpath.write_text("")

    print("✓ Wiki skeleton re-created")


def dry_run_report():
    """Print what WOULD happen without actually doing it."""
    print("=== DRY RUN — No changes made ===")
    print()
    print(f"VAULT: {VAULT}")
    print(f"WIKI: {WIKI}")
    print(f"BACKUP: {BACKUP_DIR}")
    print()
    print("PROTECTED PATHS (will NOT be touched):")
    for p in PROTECTED_PATHS:
        print(f"  {p}")
    print()

    if WIKI.exists():
        check_no_protected_in_wiki()
        size = sum(f.stat().st_size for f in WIKI.rglob("*") if f.is_file())
        files = sum(1 for _ in WIKI.rglob("*") if _.is_file())
        print(f"Would back up wiki/: {files} files, {size / 1024 / 1024:.1f} MB")
        print(f"  → {BACKUP_DIR}/")
    else:
        print("wiki/ does not exist — nothing to back up")

    print()
    print("Would re-create wiki/ skeleton:")
    print("  mocs/")
    print("  sources/{ai-research,cybersecurity,software-dev,biomechanics}/")
    print("  concepts/")
    print("  entities/")
    print("  analyses/")
    print("  sessions/")
    print("  index.md, log.md, overview-state-of-field.md (empty)")
    print()
    print("Would NOT touch:")
    for p in PROTECTED_PATHS:
        print(f"  {p}")
    print()
    print("Next step after this script:")
    print("  → Run: python workflows/full-compile.md")
    print("  → Or: ask Hermes to run full-compile workflow")


def main():
    dry_run = "--dry-run" in sys.argv
    confirmed = "--confirm" in sys.argv

    print(f"wipe-and-recompile.py — {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print()

    if dry_run:
        dry_run_report()
        return

    if not confirmed:
        print("ERROR: This is a destructive operation.")
        print()
        print("This script will:")
        print(f"  1. Move wiki/ → {BACKUP_DIR}/")
        print(f"  2. Commit backup to git branch: {GIT_BRANCH}")
        print("  3. Re-create empty wiki/ skeleton")
        print()
        print("The following paths are PROTECTED and will NOT be touched:")
        for p in PROTECTED_PATHS:
            print(f"  {p}")
        print()
        print("raw/ is NEVER touched.")
        print()
        print("To proceed, run with --confirm:")
        print(f"  python wipe-and-recompile.py --confirm")
        print()
        print("To see what would happen without making changes:")
        print(f"  python wipe-and-recompile.py --dry-run")
        return

    # Pre-flight: verify raw/ is still protected
    if RAW.exists():
        try:
            result = subprocess.run(
                ["sudo", "lsattr", str(RAW)],
                capture_output=True,
                text=True,
                timeout=5
            )
            if "i" not in result.stdout:
                print("⚠️  WARNING: raw/ does not have immutable bit set!")
                print("   Run: sudo chattr +i ~/Documents/x1n4te-workstation/raw")
        except Exception:
            pass  # sudo might not be available in this context

    # Pre-flight: check protected paths
    for protected in PROTECTED_PATHS:
        p = Path(protected)
        if p.exists():
            print(f"✓ Protected path verified: {p}")

    # Do the wipe
    backed_up = create_backup()

    if backed_up:
        git_commit_backup()

    recreate_skeleton()

    print()
    print("=" * 60)
    print("WIPE COMPLETE")
    print("=" * 60)
    print()
    print("wiki/ has been reset. To rebuild:")
    print("  1. Run: python scripts/token-budget.py")
    print("  2. Then ask Hermes to run the full-compile workflow")
    print()
    print(f"Backup branch: {GIT_BRANCH}")
    print(f"To restore: git checkout {GIT_BRANCH}")
    print()


if __name__ == "__main__":
    main()
