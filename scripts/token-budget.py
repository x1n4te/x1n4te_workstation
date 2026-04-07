#!/usr/bin/env python3
"""
token-budget.py

Measures the token cost of vault initialization.
Run this at the start of each session to verify init stays under budget.

Usage: python token-budget.py [--verbose]
"""

import sys
from pathlib import Path

try:
    import tiktoken
except ImportError:
    print("ERROR: tiktoken not installed. Run: pip install tiktoken")
    sys.exit(1)

VAULT = Path.home() / "Documents/x1n4te-workstation"
MODEL = "cl100k_base"  # GPT-4 tokenizer — close enough for estimation

TOKEN_BUDGET = 50_000
WARN_THRESHOLD = 40_000


def count_tokens(text: str) -> int:
    enc = tiktoken.get_encoding(MODEL)
    return len(enc.encode(text))


def read_file(path: Path) -> str:
    if path.exists():
        return path.read_text()
    return ""


def extract_last_n_lines(content: str, n: int = 20) -> str:
    lines = content.splitlines()
    if len(lines) <= n:
        return content
    return "\n".join(lines[-n:])


def measure_vault_init() -> dict:
    results = {}

    # HERMES.md
    hermes = VAULT / "HERMES.md"
    content = read_file(hermes)
    results["HERMES.md"] = {
        "tokens": count_tokens(content),
        "chars": len(content),
        "exists": bool(content),
    }

    # wiki/index.md
    index = VAULT / "wiki/index.md"
    content = read_file(index)
    results["wiki/index.md"] = {
        "tokens": count_tokens(content),
        "chars": len(content),
        "exists": bool(content),
    }

    # wiki/log.md (last 20 entries)
    log = VAULT / "wiki/log.md"
    content = extract_last_n_lines(read_file(log), 20)
    results["wiki/log.md (last 20)"] = {
        "tokens": count_tokens(content),
        "chars": len(content),
        "exists": log.exists(),
    }

    # sessions/last-session.md
    last_session = VAULT / "sessions/last-session.md"
    content = read_file(last_session)
    results["sessions/last-session.md"] = {
        "tokens": count_tokens(content),
        "chars": len(content),
        "exists": last_session.exists(),
    }

    # Missing From Startup Context (last session file's section)
    # Extract from the last-session.md if it exists
    missing_content = ""
    if last_session.exists():
        lines = last_session.read_text().splitlines()
        in_missing = False
        missing_lines = []
        for line in lines:
            if "## Missing From Startup Context" in line or "## Missing" in line:
                in_missing = True
                continue
            if in_missing:
                if line.startswith("## ") and "Missing" not in line:
                    break
                missing_lines.append(line)
        missing_content = "\n".join(missing_lines)
    results["Missing From Startup Context"] = {
        "tokens": count_tokens(missing_content),
        "chars": len(missing_content),
        "exists": bool(missing_content),
    }

    return results


def main():
    verbose = "--verbose" in sys.argv or "-v" in sys.argv

    print(f"Token Budget Report — {VAULT}")
    print(f"Model: {MODEL}")
    print(f"Budget: {TOKEN_BUDGET:,} tokens")
    print()

    results = measure_vault_init()
    total_tokens = 0

    print(f"{'File':<45} {'Tokens':>8} {'Chars':>10} {'Status':>12}")
    print("-" * 78)

    for name, data in results.items():
        t = data["tokens"]
        c = data["chars"]
        total_tokens += t
        status = "✓" if data["exists"] else "MISSING"
        print(f"{name:<45} {t:>8,} {c:>10,} {status:>12}")

    print("-" * 78)
    print(f"{'TOTAL INIT TOKENS':<45} {total_tokens:>8,}")
    print()

    # Budget check
    pct = (total_tokens / TOKEN_BUDGET) * 100
    print(f"Context budget used: {pct:.1f}% ({total_tokens:,} / {TOKEN_BUDGET:,})")

    if total_tokens > TOKEN_BUDGET:
        print()
        print("⚠️  WARNING: Init exceeds 50,000 token budget!")
        print("   Recommended actions:")
        print("   1. Truncate wiki/log.md to last 5 entries:")
        print(f"      python -c \"l=open('{VAULT}/wiki/log.md').readlines();open('{VAULT}/wiki/log.md','w').writelines(l[-5:])\"")
        print("   2. Archive old sessions: move sessions/<2025-*.md> to sessions/archive/")
        print("   3. Check HERMES.md — if it grew beyond 5,000 tokens, trim")
        print()
    elif total_tokens > WARN_THRESHOLD:
        print()
        print(f"⚠️  CAUTION: Init at {pct:.1f}% of budget — monitor growth")
    else:
        print()
        print(f"✓ Healthy — {TOKEN_BUDGET - total_tokens:,} tokens remaining for conversation")

    # Context window estimate
    # MiniMax-M2 context is ~1M tokens; other models vary
    print()
    print("Estimated remaining conversation budget:")
    for model, ctx in [("MiniMax-M2", 1_000_000), ("claude-sonnet-4", 200_000), ("gpt-4o", 128_000)]:
        remaining = ctx - total_tokens
        pct_ctx = (remaining / ctx) * 100
        print(f"  {model}: ~{remaining:,} tokens ({pct_ctx:.1f}% free)")

    if verbose:
        print()
        print("=== Per-File Breakdown ===")
        for name, data in results.items():
            if data["exists"]:
                lines = data["chars"] // 80 + 1
                print(f"  {name}: ~{lines} lines, {data['tokens']} tokens")


if __name__ == "__main__":
    main()
