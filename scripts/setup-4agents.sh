#!/usr/bin/env bash
# setup-4agents.sh — Bootstrap WIMS-BFP 4-agent CLI delegation workflow
# 1 Discord gateway (Orchestrator) + 3 CLI-only sub-agents
# Usage: bash setup-4agents.sh

set -e

echo "=== WIMS-BFP 4-Agent CLI Delegation Setup ==="
echo ""

# Check prerequisites
command -v hermes >/dev/null 2>&1 || { echo "hermes not found. Install: curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash"; exit 1; }

PROFILES_DIR="$HOME/.hermes/profiles"
REQUIRED_PROFILES=(orchestrator builder tester critic)

echo "[1/5] Validating profile structure..."
for profile in "${REQUIRED_PROFILES[@]}"; do
  if [[ -d "$PROFILES_DIR/$profile" ]]; then
    echo "  ✓ $profile exists"
  else
    echo "  ✗ $profile missing — run: hermes profile create $profile"
    exit 1
  fi
done

echo ""
echo "[2/5] Checking Discord bot token (orchestrator only)..."
ORCH_ENV="$PROFILES_DIR/orchestrator/.env"
if grep -q "your_orchestrator_discord_token_here" "$ORCH_ENV" 2>/dev/null; then
  echo "  ⚠ orchestrator: DISCORD_BOT_TOKEN not set in .env"
  echo "    Create 1 Discord app at: https://discord.com/developers/applications"
  echo "    Enable: Presence Intent, Server Members Intent, Message Content Intent"
else
  echo "  ✓ orchestrator: bot token configured"
fi

echo ""
echo "[3/5] Checking API keys..."
echo "  MINIMAX_API_KEY: $(grep 'MINIMAX_API_KEY' "$ORCH_ENV" 2>/dev/null | grep -v 'your' || echo 'NOT SET')"
echo "  OPENROUTER_API_KEY: $(grep 'OPENROUTER_API_KEY' "$PROFILES_DIR/tester/.env" 2>/dev/null | grep -v 'your' || echo 'NOT SET')"

echo ""
echo "[4/5] RTX 3090 Ollama endpoint check..."
echo "  Ensure Ollama is running on your RTX box:"
echo "    export OLLAMA_NUM_GPU=999"
echo "    export CUDA_VISIBLE_DEVICES=0"
echo "    ollama serve"
echo ""
echo "  Models to create (once each on the RTX box):"
echo "    cd ~/.hermes/profiles/builder && ollama create qwen3.5-27b-sushi-coder-builder -f Modelfile"
echo "    cd ~/.hermes/profiles/critic  && ollama create qwen3.5-27b-sushi-coder-critic  -f Modelfile"

echo ""
echo "[5/5] Profile configs summary..."
echo ""
for profile in "${REQUIRED_PROFILES[@]}"; do
  CONFIG="$PROFILES_DIR/$profile/config.yaml"
  if [[ -f "$CONFIG" ]]; then
    DEFAULT_MODEL=$(grep "default:" "$CONFIG" | head -1 | awk '{print $2}')
    echo "  $profile → $DEFAULT_MODEL"
  fi
done

echo ""
echo "=== Architecture ==="
echo ""
echo "  Discord: hermes-orchestrator (only 1 bot needed)"
echo "  Builder: CLI invocation → hermes -p builder -q 'task'"
echo "  Tester:  CLI invocation → hermes -p tester  -q 'task'"
echo "  Critic:  CLI invocation → hermes -p critic  -q 'task'"
echo ""
echo "=== Next Steps ==="
echo ""
echo "1. Fill in Discord bot token: ~/.hermes/profiles/orchestrator/.env"
echo "2. Fill in API keys:"
echo "   - orchestrator: MINIMAX_API_KEY"
echo "   - tester: OPENROUTER_API_KEY"
echo "3. Set up RTX 3090 Ollama (pull + create models)"
echo "4. Confirm Ollama networking (SSH tunnel or OLLAMA_HOST=0.0.0.0)"
echo "5. Start orchestrator: hermes -p orchestrator"
echo ""
echo "Documentation: ~/Documents/x1n4te-workstation/wiki/entities/wims-bfp-agentic-workflow.md"
