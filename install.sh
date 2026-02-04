#!/bin/bash
set -e

# Performance Review Generator - Installation Script
# Repository: https://github.com/deathook007/perf-review-tool

echo "🚀 Installing Performance Review Generator..."
echo ""

# Define installation directory
SKILL_DIR="$HOME/.cursor/skills/performance-review-generator"

# Check if Cursor skills directory exists
if [ ! -d "$HOME/.cursor/skills" ]; then
    echo "📁 Creating Cursor skills directory..."
    mkdir -p "$HOME/.cursor/skills"
fi

# Remove existing installation if present
if [ -d "$SKILL_DIR" ]; then
    echo "🗑️  Removing existing installation..."
    rm -rf "$SKILL_DIR"
fi

# Clone the repository
echo "📦 Downloading from GitHub..."
if command -v git &> /dev/null; then
    if git clone https://github.com/deathook007/perf-review-tool.git "$SKILL_DIR" 2>/dev/null; then
        echo "   ✓ Successfully cloned repository"
    else
        echo "⚠️  Git clone failed, trying alternative method..."
        # Download as zip
        curl -L https://github.com/deathook007/perf-review-tool/archive/refs/heads/main.zip -o /tmp/perf-review-tool.zip
        unzip -q /tmp/perf-review-tool.zip -d /tmp/
        mkdir -p "$SKILL_DIR"
        cp -r /tmp/perf-review-tool-main/* "$SKILL_DIR/"
        rm -rf /tmp/perf-review-tool.zip /tmp/perf-review-tool-main
        echo "   ✓ Downloaded and extracted"
    fi
else
    echo "⚠️  Git not found. Downloading as zip..."
    curl -L https://github.com/deathook007/perf-review-tool/archive/refs/heads/main.zip -o /tmp/perf-review-tool.zip
    unzip -q /tmp/perf-review-tool.zip -d /tmp/
    mkdir -p "$SKILL_DIR"
    cp -r /tmp/perf-review-tool-main/* "$SKILL_DIR/"
    rm -rf /tmp/perf-review-tool.zip /tmp/perf-review-tool-main
    echo "   ✓ Downloaded and extracted"
fi

# Remove .git directory if present (clean installation)
if [ -d "$SKILL_DIR/.git" ]; then
    rm -rf "$SKILL_DIR/.git"
fi

# Make scripts executable
echo "🔧 Setting up permissions..."
chmod +x "$SKILL_DIR"/*.py 2>/dev/null || true
chmod +x "$SKILL_DIR"/*.sh 2>/dev/null || true

# Check Python installation
echo "🐍 Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not found."
    echo "   Install Python 3: https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
echo "   ✓ Python $PYTHON_VERSION found"

# Success message
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Installation Complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📍 Installed to: $SKILL_DIR"
echo ""
echo "🎯 Usage in Cursor AI:"
echo "   Just say: 'Use performance-review-generator to create my review'"
echo ""
echo "📝 Direct Command Line Usage:"
echo "   python3 $SKILL_DIR/generate_review.py YOUR_FILE.csv --role 'SDE 2' -o review.md"
echo ""
echo "📖 Documentation: https://github.com/deathook007/perf-review-tool"
echo ""
