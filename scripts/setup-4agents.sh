#!/usr/bin/env bash
# setup-4agents.sh — Bootstrap WIMS-BFP 4-agent Discord workflow
# Usage: bash setup-4agents.sh

set -e

echo "=== WIMS-BFP 4-Agent Setup ==="
echo ""

# Check prerequisites
command -v hermes >/dev/null 2>&1 || { echo "hermes not found. Install: curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash"; exit 1; }

PROFILES_DIR="$HOME/.hermes/profiles"
REQUIRED_PROFILES=(orchestrator builder tester critic)

echo "[1/4] Validating profile structure..."
for profile in "${REQUIRED_PROFILES[@]}"; do
  if [[ -d "$PROFILES_DIR/$profile" ]]; then
    echo "  ✓ $profile exists"
  else
    echo "  ✗ $profile missing — run: hermes profile create $profile"
    exit 1
  fi
done

echo ""
echo "[2/4] RTX 3090 endpoint check..."
echo "  Ensure vLLM is running on your RTX box:"
echo "  vllm serve qwen3.5-24b-sushi-coder --host 0.0.0.0 --port 8000"
echo ""
read -p "Is the RTX endpoint accessible at localhost:8000? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
  echo "Start vLLM on your RTX 3090 first, then re-run."
  exit 1
fi

echo ""
echo "[3/4] Discord bot tokens..."
echo "Create 4 bots at: https://discord.com/developers/applications"
echo ""
for profile in "${REQUIRED_PROFILES[@]}"; do
  TOKEN_FILE="$PROFILES_DIR/$profile/.env"
  if grep -q "your_discord_bot_token_here" "$TOKEN_FILE" 2>/dev/null; then
    echo "  ⚠ $profile: DISCORD_BOT_TOKEN not set in .env"
  else
    echo "  ✓ $profile: bot token configured"
  fi
done

echo ""
echo "[4/4] Profile configs summary..."
echo ""
for profile in "${REQUIRED_PROFILES[@]}"; do
  CONFIG="$PROFILES_DIR/$profile/config.yaml"
  if [[ -f "$CONFIG" ]]; then
    DEFAULT_MODEL=$(grep "default:" "$CONFIG" | head -1 | awk '{print $2}')
    echo "  $profile → $DEFAULT_MODEL"
  fi
done

echo ""
echo "=== Next Steps ==="
echo ""
echo "1. Fill in Discord bot tokens in: ~/.hermes/profiles/*/.env"
echo "2. Fill in API keys:"
echo "   - orchestrator: MINIMAX_API_KEY"
echo "   - tester: OPENROUTER_API_KEY"
echo "3. Set up Discord server with channels:"
echo "   - 🏛-orchestrator  - 🔨-builder  - 🧪-tester  - 🔍-critic"
echo "   - 📋-handoff  - 🛡-admin"
echo "4. Start agents:"
echo "   hermes -p orchestrator  # Terminal 1"
echo "   hermes -p builder       # Terminal 2"
echo "   hermes -p tester        # Terminal 3"
echo "   hermes -p critic        # Terminal 4"
echo ""
echo "Documentation: ~/Documents/x1n4te-workstation/wiki/entities/wims-bfp-agentic-workflow.md"
