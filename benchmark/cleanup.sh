#!/usr/bin/env bash
set -e

# Cleanup script for fd-mcp benchmark
# Removes test data and results

BENCHMARK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEST_DATA_DIR="${BENCHMARK_DIR}/test_data"
RESULTS_FILE="${BENCHMARK_DIR}/results.txt"

echo "🧹 Cleaning up benchmark data..."

# Remove test data
if [ -d "$TEST_DATA_DIR" ]; then
    echo "  Removing test data directory..."
    rm -rf "$TEST_DATA_DIR"
    echo "  ✓ Test data removed"
else
    echo "  No test data found"
fi

# Remove results file
if [ -f "$RESULTS_FILE" ]; then
    echo "  Removing results file..."
    rm -f "$RESULTS_FILE"
    echo "  ✓ Results file removed"
else
    echo "  No results file found"
fi

echo ""
echo "✅ Cleanup complete!"
echo ""
echo "To run benchmarks again:"
echo "  1. ./setup.sh    - Create test data"
echo "  2. ./run_benchmark.sh - Run benchmarks"
