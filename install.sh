#!/bin/bash
# Quick Install Script for Performance Review Generator
# Usage: curl -fsSL https://your-url/install.sh | bash

set -e

SKILL_NAME="performance-review-generator"
SKILL_DIR="$HOME/.cursor/skills/$SKILL_NAME"
REPO_URL="https://github.com/deepak-bhatt/cursor-skills/$SKILL_NAME"

echo "🚀 Installing Performance Review Generator skill..."
echo ""

# Check prerequisites
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is required but not installed."
    echo "   Install Python 3.7+ and try again."
    exit 1
fi

# Create skills directory
mkdir -p "$HOME/.cursor/skills"

# Check if skill already exists
if [ -d "$SKILL_DIR" ]; then
    echo "⚠️  Skill already installed at: $SKILL_DIR"
    read -p "   Do you want to update it? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Installation cancelled."
        exit 0
    fi
    rm -rf "$SKILL_DIR"
fi

# Install method 1: From Git (if available)
if command -v git &> /dev/null && [ -n "$REPO_URL" ]; then
    echo "📦 Cloning from repository..."
    git clone "$REPO_URL" "$SKILL_DIR" 2>/dev/null || {
        echo "⚠️  Git clone failed, falling back to download..."
        INSTALL_METHOD="download"
    }
else
    INSTALL_METHOD="download"
fi

# Install method 2: Download ZIP (fallback)
if [ "$INSTALL_METHOD" = "download" ]; then
    echo "📦 Downloading skill package..."
    
    # Try with curl
    if command -v curl &> /dev/null; then
        curl -fsSL "https://your-cdn/performance-review-generator.zip" -o /tmp/skill.zip
    # Try with wget
    elif command -v wget &> /dev/null; then
        wget -q "https://your-cdn/performance-review-generator.zip" -O /tmp/skill.zip
    else
        echo "❌ Error: Neither curl nor wget found. Cannot download skill."
        exit 1
    fi
    
    # Extract
    echo "📦 Extracting..."
    unzip -q /tmp/skill.zip -d "$HOME/.cursor/skills/"
    rm /tmp/skill.zip
fi

# Make scripts executable
cd "$SKILL_DIR"
chmod +x *.py test_skill.sh 2>/dev/null || true

# Run tests
echo ""
echo "🧪 Running tests..."
if ./test_skill.sh > /dev/null 2>&1; then
    echo "✅ Tests passed!"
else
    echo "⚠️  Tests failed, but installation completed."
    echo "   You can still use the skill - check documentation for help."
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Performance Review Generator installed!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📍 Location: $SKILL_DIR"
echo ""
echo "🚀 Quick Start:"
echo ""
echo "   In Cursor:"
echo '   "Use performance-review-generator skill to create my review"'
echo ""
echo "   Command line:"
echo "   cd $SKILL_DIR"
echo "   python3 generate_review.py ~/Downloads/objectives.csv"
echo ""
echo "📚 Documentation:"
echo "   $SKILL_DIR/QUICKSTART.md"
echo "   $SKILL_DIR/README.md"
echo ""
echo "🎉 Ready to transform your performance reviews!"
echo ""
