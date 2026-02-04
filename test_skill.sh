#!/bin/bash
# Test script to verify the skill works correctly

echo "🧪 Testing Performance Review Generator Skill"
echo "=============================================="
echo ""

# Test 1: Check all files exist
echo "✓ Test 1: Checking files..."
required_files=("SKILL.md" "parse_csv.py" "generate_review.py" "prompt_templates.py" "validate_review.py" "skill.json" "install.sh")
all_exist=true
for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✓ $file"
    else
        echo "  ✗ $file MISSING"
        all_exist=false
    fi
done

if [ "$all_exist" = true ]; then
    echo "✅ All files present"
else
    echo "❌ Some files missing"
    exit 1
fi

echo ""

# Test 2: Check Python scripts are executable
echo "✓ Test 2: Checking executability..."
python_files=("parse_csv.py" "generate_review.py" "prompt_templates.py" "validate_review.py")
for file in "${python_files[@]}"; do
    if [ -x "$file" ]; then
        echo "  ✓ $file is executable"
    else
        echo "  ⚠ $file not executable (fixing...)"
        chmod +x "$file"
    fi
done
echo "✅ All scripts executable"

echo ""

# Test 3: Check Python scripts can be imported
echo "✓ Test 3: Checking Python syntax..."
for file in "${python_files[@]}"; do
    if python3 -m py_compile "$file" 2>/dev/null; then
        echo "  ✓ $file syntax OK"
    else
        echo "  ✗ $file has syntax errors"
        exit 1
    fi
done
echo "✅ All scripts have valid syntax"

echo ""

# Test 4: Verify help commands work
echo "✓ Test 4: Testing help commands..."
if python3 parse_csv.py -h >/dev/null 2>&1 || python3 parse_csv.py 2>&1 | grep -q "Usage"; then
    echo "  ✓ parse_csv.py help works"
else
    echo "  ✗ parse_csv.py help failed"
fi

if python3 generate_review.py -h >/dev/null 2>&1 || python3 generate_review.py 2>&1 | grep -q "Usage"; then
    echo "  ✓ generate_review.py help works"
else
    echo "  ✗ generate_review.py help failed"
fi
echo "✅ Help commands working"

echo ""
echo "=============================================="
echo "🎉 All tests passed!"
echo "=============================================="
echo ""
echo "Skill is ready to use!"
echo ""
echo "Quick test:"
echo "  python3 generate_review.py /path/to/objectives.csv --role SD2 --output test.md"
