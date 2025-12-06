# fd-mcp Benchmark Suite

This directory contains benchmarking tools to demonstrate the performance advantages of fd-mcp tools over traditional bash commands.

## Quick Start

```bash
# 1. Generate test data (default: 100,000 files)
./setup.sh

# 2. Run benchmarks
./run_benchmark.sh
```

## Setup Options

The `setup.sh` script supports configurable file counts:

```bash
# Default: 100,000 files
./setup.sh

# Custom file count
./setup.sh -n 10000     # 10,000 files
./setup.sh -n 1000000   # 1 million files

# Show help
./setup.sh --help
```

### Minimum Requirements

- **File count**: Minimum 100 files
- **Python 3**: Required for file generation
- **Disk space**: Approximately 1MB per 100 files

## File Distribution

The benchmark creates a realistic mix of file types:

| Type | Percentage | Description |
|------|------------|-------------|
| Python source | 15% | Module files with classes |
| Python helpers | 5% | Helper function files |
| Test files | 15% | Unit tests |
| JavaScript components | 10% | React-like components |
| JavaScript utilities | 5% | Utility functions |
| JSON config | 5% | Configuration files |
| YAML config | 5% | Settings files |
| Documentation | 10% | Markdown docs |
| Shell scripts | 8% | Bash scripts |
| Python libraries | 4% | Library modules |
| JavaScript libraries | 3% | Common utilities |
| Examples | 10% | Example scripts |
| Text files | 3% | Data files |
| Environment files | 1% | .env files |
| README files | 1% | Documentation |
| Mixed files | ~5% | Legacy and integration tests |

## Benchmark Tests

The benchmark suite tests the following operations:

1. **Find all Python files** - Testing file discovery by extension
2. **Find test files by pattern** - Pattern matching performance
3. **Search TODO in Python files** - Content search in specific file types
4. **Search FIXME with context** - Context-aware content search
5. **Count all files** - Simple file counting
6. **Count Python files** - Filtered file counting
7. **Find recently modified files** - Time-based filtering
8. **Find class definitions** - Code pattern matching
9. **Search TODO in JavaScript** - Cross-language content search
10. **Search for function definitions** - Complex regex patterns
11. **Find config files** - Multiple extension matching
12. **Search in documentation** - Markdown file searches

## Performance Expectations

Based on the default 100,000 file dataset:

| Operation | Traditional (find/grep) | fd-mcp | Expected Speedup |
|-----------|------------------------|---------|------------------|
| File by extension | ~2-5s | ~0.3-0.5s | 5-10x |
| Content search | ~10-30s | ~0.5-1s | 10-100x |
| Recent files | ~3-8s | ~0.5-1s | 3-5x |
| File counting | ~1-3s | ~0.2-0.4s | 5-8x |

*Note: Actual performance varies based on hardware, especially disk I/O speed.*

## Implementation Details

### File Generation

The `setup.sh` script is a wrapper that:
1. Parses command-line arguments
2. Validates inputs
3. Delegates to `generate_files.py` for fast, reliable file creation

The Python implementation (`generate_files.py`) is used for:
- **Speed**: Much faster than bash loops for large file counts
- **Reliability**: No shell quirks or loop issues
- **Maintainability**: Easier to read and modify

### File Content

All generated files contain realistic code patterns:
- TODO and FIXME comments for search testing
- Class and function definitions for pattern matching
- Proper syntax for relevant file types
- Numbered identifiers for uniqueness

## Troubleshooting

### Slow File Generation

If setup is slow:
- Check available disk space
- Consider using a faster filesystem (SSD vs HDD)
- Reduce file count for testing

### Benchmark Fails

If benchmarks fail:
- Ensure `fd` (or `fdfind`) is installed
- Ensure `ripgrep` (`rg`) is installed
- Check that test_data directory exists and is populated

### Installation

```bash
# Ubuntu/Debian
sudo apt install fd-find ripgrep

# macOS
brew install fd ripgrep
```

## Cleaning Up

```bash
# Remove test data
rm -rf test_data/

# Or regenerate with different count
./setup.sh -n 10000
```

## Contributing

To modify the benchmark:

1. Edit `generate_files.py` for file generation changes
2. Edit `run_benchmark.sh` for new benchmark tests
3. Test with small file counts first (`-n 1000`)
4. Verify results with the default 100,000 files
