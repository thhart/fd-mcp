#!/usr/bin/env bash
set -e

# Setup script for fd-mcp benchmark
# Creates test files with various patterns for benchmarking

# Default configuration
DEFAULT_FILE_COUNT=10000

# Parse command-line arguments
FILE_COUNT=${DEFAULT_FILE_COUNT}

show_usage() {
    cat << EOF
Usage: $0 [OPTIONS]

Setup benchmark test data for fd-mcp performance testing.

OPTIONS:
    -n, --num-files COUNT    Number of files to generate (default: ${DEFAULT_FILE_COUNT})
    -h, --help              Show this help message

EXAMPLES:
    $0                      # Create ${DEFAULT_FILE_COUNT} files (default)
    $0 -n 10000            # Create 10,000 files
    $0 -n 1000000          # Create 1,000,000 files

EOF
}

while [[ $# -gt 0 ]]; do
    case $1 in
        -n|--num-files)
            FILE_COUNT="$2"
            shift 2
            ;;
        -h|--help)
            show_usage
            exit 0
            ;;
        *)
            echo "Error: Unknown option $1"
            show_usage
            exit 1
            ;;
    esac
done

# Validate file count
if ! [[ "$FILE_COUNT" =~ ^[0-9]+$ ]] || [ "$FILE_COUNT" -lt 100 ]; then
    echo "Error: File count must be a number >= 100"
    exit 1
fi

BENCHMARK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is required but not found"
    echo "Please install Python 3 to use this script"
    exit 1
fi

# Run the Python generator
exec python3 "$BENCHMARK_DIR/generate_files.py" -n "$FILE_COUNT"
