#!/usr/bin/env bash
# One-Click Installer for Antigravity Custom Skills (macOS / Linux)
set -e

TARGET_DIR="$HOME/.gemini/config/skills"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_DIR="$SCRIPT_DIR/skills"

echo ">>> Installing Antigravity Skills to: $TARGET_DIR"
mkdir -p "$TARGET_DIR"

for skill in "$SOURCE_DIR"/*/; do
    if [ -d "$skill" ]; then
        skill_name=$(basename "$skill")
        echo "Installing skill: $skill_name..."
        rm -rf "$TARGET_DIR/$skill_name"
        cp -r "$skill" "$TARGET_DIR/$skill_name"
        echo "  [OK] $skill_name installed."
    fi
done

echo ""
echo ">>> All skills successfully installed globally! Restart or open Antigravity to discover them."
