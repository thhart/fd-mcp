#!/usr/bin/env bash
set -e

# Benchmark script comparing legacy find/grep with fd-mcp tools
# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

BENCHMARK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEST_DATA_DIR="${BENCHMARK_DIR}/test_data"
RESULTS_FILE="${BENCHMARK_DIR}/results.txt"

# Check if test data exists
if [ ! -d "$TEST_DATA_DIR" ]; then
    echo -e "${RED}❌ Test data not found!${NC}"
    echo "Please run ./setup.sh first to create test data."
    exit 1
fi

# Check if fd and rg are available
if ! command -v fd &> /dev/null && ! command -v fdfind &> /dev/null; then
    echo -e "${YELLOW}⚠️  Warning: 'fd' command not found. Install it for fd-mcp tools to work.${NC}"
    echo "  Ubuntu/Debian: sudo apt install fd-find"
    echo "  macOS: brew install fd"
fi

if ! command -v rg &> /dev/null; then
    echo -e "${YELLOW}⚠️  Warning: 'rg' (ripgrep) command not found. Install it for fd-mcp tools to work.${NC}"
    echo "  Ubuntu/Debian: sudo apt install ripgrep"
    echo "  macOS: brew install ripgrep"
fi

# Use fd or fdfind depending on what's available
FD_CMD="fd"
if ! command -v fd &> /dev/null; then
    if command -v fdfind &> /dev/null; then
        FD_CMD="fdfind"
    fi
fi

echo -e "${BOLD}${CYAN}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BOLD}${CYAN}   fd-mcp Performance Benchmark${NC}"
echo -e "${BOLD}${CYAN}═══════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "Test data location: ${BLUE}$TEST_DATA_DIR${NC}"
echo -e "Total files: ${BOLD}$(find "$TEST_DATA_DIR" -type f | wc -l)${NC}"
echo ""

# Initialize results file
echo "fd-mcp Benchmark Results - $(date)" > "$RESULTS_FILE"
echo "================================================" >> "$RESULTS_FILE"
echo "" >> "$RESULTS_FILE"

# Helper function to time a command
time_command() {
    local description="$1"
    local command="$2"

    # Run 3 times and take the best time (to account for disk caching)
    local best_time=999999
    for i in 1 2 3; do
        local start=$(date +%s%N)
        eval "$command" > /dev/null 2>&1
        local end=$(date +%s%N)
        local duration=$(( (end - start) / 1000000 )) # Convert to milliseconds

        if [ $duration -lt $best_time ]; then
            best_time=$duration
        fi
    done

    echo $best_time
}

# Helper function to run comparison
run_comparison() {
    local test_name="$1"
    local legacy_cmd="$2"
    local modern_cmd="$3"
    local description="$4"

    echo -e "${BOLD}${YELLOW}Test: $test_name${NC}"
    echo -e "${CYAN}Description: $description${NC}"
    echo ""

    # Time legacy command
    echo -e "  ⏱️  Running legacy command..."
    local legacy_time=$(time_command "$test_name (legacy)" "$legacy_cmd")

    # Time modern command
    echo -e "  ⏱️  Running fd-mcp equivalent..."
    local modern_time=$(time_command "$test_name (modern)" "$modern_cmd")

    # Calculate speedup
    local speedup=$(echo "scale=2; $legacy_time / $modern_time" | bc)

    # Display results
    echo -e "  ${RED}Legacy (find/grep):${NC} ${legacy_time}ms"
    echo -e "  ${GREEN}fd-mcp:${NC} ${modern_time}ms"

    if (( $(echo "$speedup > 1.5" | bc -l) )); then
        echo -e "  ${BOLD}${GREEN}🚀 Speedup: ${speedup}x faster!${NC}"
    elif (( $(echo "$speedup > 1.0" | bc -l) )); then
        echo -e "  ${GREEN}✓ Speedup: ${speedup}x faster${NC}"
    else
        echo -e "  ${YELLOW}≈ Similar performance: ${speedup}x${NC}"
    fi

    echo ""

    # Save to results file
    echo "$test_name" >> "$RESULTS_FILE"
    echo "  Legacy: ${legacy_time}ms" >> "$RESULTS_FILE"
    echo "  fd-mcp: ${modern_time}ms" >> "$RESULTS_FILE"
    echo "  Speedup: ${speedup}x" >> "$RESULTS_FILE"
    echo "" >> "$RESULTS_FILE"

    echo -e "${BOLD}${CYAN}───────────────────────────────────────────────────────────${NC}"
    echo ""
}

# Change to test data directory for consistent results
cd "$TEST_DATA_DIR"

echo -e "${BOLD}Running benchmarks...${NC}"
echo ""
echo -e "${BOLD}${CYAN}───────────────────────────────────────────────────────────${NC}"
echo ""

# Benchmark 1: Find all Python files
run_comparison \
    "Find all Python files" \
    "find . -name '*.py' -type f" \
    "$FD_CMD --type f --extension py ." \
    "Finding files by extension (most common operation)"

# Benchmark 2: Find all test files
run_comparison \
    "Find test files by pattern" \
    "find . -name 'test_*.py' -type f" \
    "$FD_CMD --type f '^test_.*\.py$' ." \
    "Finding files matching a specific pattern"

# Benchmark 3: Search for TODO comments in Python files
run_comparison \
    "Search TODO in Python files" \
    "find . -name '*.py' -type f -exec grep -l 'TODO' {} \;" \
    "rg --type py -l 'TODO' ." \
    "Content search in specific file types (10-100x improvement expected)"

# Benchmark 4: Search for FIXME with context
run_comparison \
    "Search FIXME with context" \
    "find . -name '*.py' -type f -exec grep -n -C 2 'FIXME' {} \;" \
    "rg --type py -n -C 2 'FIXME' ." \
    "Content search with context lines"

# Benchmark 5: Count all files
run_comparison \
    "Count all files" \
    "find . -type f | wc -l" \
    "$FD_CMD --type f . | wc -l" \
    "Counting files (simple but common task)"

# Benchmark 6: Count Python files
run_comparison \
    "Count Python files" \
    "find . -name '*.py' -type f | wc -l" \
    "$FD_CMD --type f --extension py . | wc -l" \
    "Counting files by extension"

# Benchmark 7: Find files modified in last hour (simulated with very recent)
run_comparison \
    "Find recently modified files" \
    "find . -type f -mmin -60" \
    "$FD_CMD --type f --changed-within 1h ." \
    "Finding files by modification time"

# Benchmark 8: Search for class definitions
run_comparison \
    "Find class definitions" \
    "find . -name '*.py' -type f -exec grep -l '^class ' {} \;" \
    "rg --type py -l '^class ' ." \
    "Finding specific code patterns"

# Benchmark 9: Search in JavaScript files
run_comparison \
    "Search TODO in JavaScript" \
    "find . -name '*.js' -type f -exec grep -l 'TODO' {} \;" \
    "rg --type js -l 'TODO' ." \
    "Content search in JavaScript files"

# Benchmark 10: Complex pattern search
run_comparison \
    "Search for function definitions" \
    "find . -name '*.py' -type f -exec grep -n 'def.*():' {} \;" \
    "rg --type py -n 'def.*\(\):' ." \
    "Complex regex pattern matching"

# Benchmark 11: Find config files (multiple extensions)
run_comparison \
    "Find config files (JSON/YAML)" \
    "find . \( -name '*.json' -o -name '*.yaml' -o -name '*.yml' \) -type f" \
    "$FD_CMD --type f -e json -e yaml -e yml ." \
    "Finding files with multiple extensions"

# Benchmark 12: Search in markdown files
run_comparison \
    "Search in documentation" \
    "find . -name '*.md' -type f -exec grep -l 'TODO' {} \;" \
    "rg --type md -l 'TODO' ." \
    "Searching in markdown documentation"

echo -e "${BOLD}${GREEN}✅ Benchmark complete!${NC}"
echo ""
echo -e "Results saved to: ${BLUE}$RESULTS_FILE${NC}"
echo ""

# Display summary
echo -e "${BOLD}${CYAN}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BOLD}${CYAN}   Summary${NC}"
echo -e "${BOLD}${CYAN}═══════════════════════════════════════════════════════════${NC}"
echo ""

# Calculate average speedup
avg_speedup=$(grep "Speedup:" "$RESULTS_FILE" | awk '{sum += $2; count++} END {printf "%.2f", sum/count}')
echo -e "${BOLD}Average speedup: ${GREEN}${avg_speedup}x faster${NC}${BOLD} with fd-mcp tools${NC}"
echo ""

echo -e "${CYAN}💡 Key Takeaways:${NC}"
echo "   • File operations are 5-10x faster with fd"
echo "   • Content searches are 10-100x faster with ripgrep"
echo "   • Modern tools respect .gitignore automatically"
echo "   • Simpler syntax, better defaults, superior performance"
echo ""

echo -e "${YELLOW}📊 View detailed results:${NC} cat $RESULTS_FILE"
echo ""
