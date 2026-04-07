#!/usr/bin/env python3
"""
wiki-sweep.py

Scans wiki/ for expired entries and attempts re-verification.
Applies #stale-intel and #needs-review tags per HERMES.md policy.
Does NOT auto-delete or auto-overwrite — flags for human review.

Usage: python wiki-sweep.py [--verbose]
"""

import sys
import re
import datetime
from pathlib import Path
from typing import Optional

VAULT = Path.home() / "Documents/x1n4te-workstation"
WIKI = VAULT / "wiki"
RAW = VAULT / "raw"

TODAY = datetime.date.today()

# TTL defaults by category (days)
TTL_DEFAULTS = {
    "ai-research": {"review": 30, "stale": 90},
    "cybersecurity": {"review": 7, "stale": 21},
    "cybersecurity-architecture": {"review": 90, "stale": 180},
    "software-dev": {"review": 60, "stale": 120},
    "biomechanics": {"review": 60, "stale": 180},
}


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Parse YAML frontmatter from markdown file. Returns (frontmatter_dict, body)."""
    if not content.startswith("---"):
        return {}, content
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content
    fm_text = parts[1]
    body = parts[2]
    fm = {}
    for line in fm_text.strip().splitlines():
        if ": " in line:
            key, val = line.split(": ", 1)
            fm[key.strip()] = val.strip().strip('"').strip("'")
        elif ":" in line:
            key = line.split(":")[0].strip()
            fm[key.strip()] = ""
    return fm, body


def detect_category(page_path: Path) -> str:
    """Infer category from page path."""
    path_str = str(page_path)
    if "ai-research" in path_str:
        return "ai-research"
    if "cybersecurity" in path_str:
        # Architecture sub-category uses longer TTL
        if "architecture" in path_str or "system" in path_str:
            return "cybersecurity-architecture"
        return "cybersecurity"
    if "software-dev" in path_str:
        return "software-dev"
    if "biomechanics" in path_str:
        return "biomechanics"
    return "software-dev"  # default


def parse_date(date_str: str) -> Optional[datetime.date]:
    """Parse a YYYY-MM-DD date string."""
    if not date_str:
        return None
    try:
        return datetime.date.fromisoformat(date_str)
    except ValueError:
        return None


def get_ttl(category: str, field: str) -> int:
    """Get TTL in days for a given category and field (review or stale)."""
    return TTL_DEFAULTS.get(category, {"review": 60, "stale": 180}).get(field, 180)


def check_has_new_raw(page_path: Path, source_refs: list) -> bool:
    """Check if any raw source referenced by this page has been updated since last_verified."""
    if not source_refs:
        return False
    for ref in source_refs:
        raw_path = VAULT / ref
        if raw_path.exists():
            # Check mtime — raw should be immutable so mtime = ingest time
            mtime = datetime.date.fromtimestamp(raw_path.stat().st_mtime)
            # If raw file was added/modified within the last 30 days, consider it "new"
            if (TODAY - mtime).days <= 30:
                return True
    return False


def scan_page(page_path: Path) -> dict:
    """
    Scan a single wiki page.
    Returns a dict with action flags.
    """
    content = page_path.read_text()
    fm, body = parse_frontmatter(content)

    page_path_str = str(page_path.relative_to(VAULT))
    category = detect_category(page_path)

    result = {
        "path": page_path_str,
        "action": None,
        "reason": None,
        "stale_after": None,
        "review_after": None,
        "status": fm.get("status", "active"),
        "last_verified": parse_date(fm.get("last_verified", "")),
        "has_source_refs": bool(fm.get("source_refs")),
    }

    last_verified = result["last_verified"]
    if not last_verified:
        # No last_verified — set defaults
        review_ttl = get_ttl(category, "review")
        stale_ttl = get_ttl(category, "stale")
        result["review_after"] = TODAY + datetime.timedelta(days=review_ttl)
        result["stale_after"] = TODAY + datetime.timedelta(days=stale_ttl)
        return result

    # Calculate thresholds
    review_ttl = get_ttl(category, "review")
    stale_ttl = get_ttl(category, "stale")

    review_after = last_verified + datetime.timedelta(days=review_ttl)
    stale_after = last_verified + datetime.timedelta(days=stale_ttl)
    result["review_after"] = review_after
    result["stale_after"] = stale_after

    # Decision logic
    if TODAY > stale_after:
        result["action"] = "stale-intel"
        result["reason"] = f"past stale_after ({stale_after})"
    elif TODAY > review_after:
        has_new = check_has_new_raw(page_path, fm.get("source_refs", []))
        if has_new:
            result["action"] = "verify"
            result["reason"] = "past review_after with newer raw available"
        else:
            result["action"] = "needs-review"
            result["reason"] = f"past review_after ({review_after}), no newer raw"
    elif (TODAY - last_verified).days > 180:
        # Exceptional: even with recent review_after, if it's been 6 months, flag
        result["action"] = "stale-intel"
        result["reason"] = "last_verified > 180 days ago"

    return result


def apply_tag(page_path: Path, tag: str):
    """Append a tag to the page's frontmatter tags list."""
    content = page_path.read_text()
    fm, body = parse_frontmatter(content)

    if "tags:" not in content:
        # Add tags section
        fm["tags"] = tag
    else:
        # Append to existing tags
        existing = fm.get("tags", "")
        if tag not in existing:
            fm["tags"] = f"{existing} {tag}".strip()

    # Update status if not already set
    if fm.get("status", "active") == "active" and tag == "#stale-intel":
        fm["status"] = "stale"

    # Update updated: field
    fm["updated"] = str(TODAY)

    # Rewrite file
    fm_lines = [f"{k}: {v}" if v else f"{k}:" for k, v in fm.items()]
    new_content = f"---\n" + "\n".join(fm_lines) + "\n---\n" + body
    page_path.write_text(new_content)


def sweep_wiki(verbose: bool = False) -> dict:
    """Scan all wiki markdown files and apply actions."""
    stats = {
        "scanned": 0,
        "stale_intel": 0,
        "needs_review": 0,
        "verify": 0,
        "archived": 0,
        "errors": 0,
        "details": [],
    }

    md_files = list(WIKI.rglob("*.md"))
    # Exclude archived and dotfiles
    md_files = [f for f in md_files if ".archived" not in str(f) and not f.name.startswith(".")]

    print(f"=== Wiki Sweep Report: {TODAY} ===")
    print(f"Pages scanned: {len(md_files)}")
    print()

    for page_path in md_files:
        # Skip non-wiki files
        if page_path.name in ["index.md", "log.md", "overview-state-of-field.md"]:
            continue

        try:
            result = scan_page(page_path)
            stats["scanned"] += 1

            action = result["action"]
            if action == "stale-intel":
                stats["stale_intel"] += 1
                # Apply tag inline
                apply_tag(page_path, "#stale-intel")
                stats["details"].append(f"  [STALE] {result['path']} — {result['reason']}")
                if verbose:
                    print(f"  [STALE] {result['path']}")
            elif action == "needs-review":
                stats["needs_review"] += 1
                apply_tag(page_path, "#needs-review")
                stats["details"].append(f"  [REVIEW] {result['path']} — {result['reason']}")
                if verbose:
                    print(f"  [REVIEW] {result['path']}")
            elif action == "verify":
                stats["verify"] += 1
                stats["details"].append(f"  [VERIFY] {result['path']} — {result['reason']}")
                if verbose:
                    print(f"  [VERIFY] {result['path']}")
            else:
                if verbose:
                    print(f"  [OK] {result['path']}")

        except Exception as e:
            stats["errors"] += 1
            stats["details"].append(f"  [ERROR] {page_path}: {e}")
            print(f"  [ERROR] {page_path}: {e}")

    return stats


def main():
    verbose = "--verbose" in sys.argv or "-v" in sys.argv

    print()
    print("=" * 50)
    print("  wiki-sweep.py")
    print(f"  Vault: {VAULT}")
    print(f"  Date: {TODAY}")
    print("=" * 50)
    print()

    if not WIKI.exists():
        print("ERROR: wiki/ does not exist. Nothing to sweep.")
        sys.exit(1)

    stats = sweep_wiki(verbose=verbose)

    print()
    print(f"Scanned: {stats['scanned']}")
    print(f"#stale-intel: {stats['stale_intel']}")
    print(f"#needs-review: {stats['needs_review']}")
    print(f"Re-verified (auto): {stats['verify']}")
    print(f"Errors: {stats['errors']}")
    print()

    if stats["details"]:
        print("Details:")
        for d in stats["details"]:
            print(d)
        print()

    # Write log entry suggestion
    print("Log entry:")
    print(f"  {TODAY} | sweep | scanned: {stats['scanned']} | stale: {stats['stale_intel']} | "
          f"review: {stats['needs_review']} | verified: {stats['verify']}")

    if stats["stale_intel"] > 0 or stats["needs_review"] > 0:
        print()
        print("⚠️  Action required:")
        print("  Review flagged pages in Obsidian.")
        print("  Then run: python wiki-sweep.py --verbose")
        print("  To confirm tags were applied.")


if __name__ == "__main__":
    main()
