#!/usr/bin/env bash
# One-Click Installer for Antigravity Custom Skills & MCP Tools (macOS / Linux)
set -e

CONFIG_DIR="$HOME/.gemini/config"
TARGET_DIR="$CONFIG_DIR/skills"
MCP_CONFIG="$CONFIG_DIR/mcp_config.json"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_DIR="$SCRIPT_DIR/skills"

echo "=========================================================="
echo "   Antigravity Skills & MCP Automatic Setup"
echo "=========================================================="

# 1. Install Skills
echo ""
echo ">>> [1/2] Installing Skills to: $TARGET_DIR"
mkdir -p "$TARGET_DIR"

for skill in "$SOURCE_DIR"/*/; do
    if [ -d "$skill" ]; then
        skill_name=$(basename "$skill")
        echo "  -> Installing $skill_name..."
        rm -rf "$TARGET_DIR/$skill_name"
        cp -r "$skill" "$TARGET_DIR/$skill_name"
        echo "     [OK] $skill_name installed."
    fi
done

# 2. Configure MCP Servers
echo ""
echo ">>> [2/2] Checking MCP Servers in: $MCP_CONFIG"
if [ ! -f "$MCP_CONFIG" ]; then
    cp "$SCRIPT_DIR/mcp_config.example.json" "$MCP_CONFIG"
    echo "  -> Created new mcp_config.json with Playwright & Chrome-DevTools!"
else
    echo "  -> mcp_config.json already exists. Check mcp_config.example.json to add any missing tools."
fi

echo ""
echo "=========================================================="
echo " [SUCCESS] Setup complete! Restart Antigravity to load tools."
echo "=========================================================="
