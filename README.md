# fd-mcp

A Model Context Protocol (MCP) server that provides fast file search capabilities using [fd](https://github.com/sharkdp/fd), a modern alternative to the traditional `find` command.

## What is fd-mcp?

fd-mcp bridges [fd](https://github.com/sharkdp/fd) with AI assistants like Claude Code through the Model Context Protocol. It exposes fd's powerful file search capabilities as MCP tools, enabling AI assistants to efficiently navigate and search codebases.

## Why fd?

fd offers significant advantages over traditional file search tools:

- **Blazing Fast**: Written in Rust, fd is often 5-10x faster than `find` for typical searches
- **User-Friendly Syntax**: Simple, intuitive patterns instead of cryptic flags (`fd pattern` vs `find -name "*pattern*"`)
- **Smart Defaults**: Automatically respects `.gitignore` and skips hidden files/directories
- **Colorized Output**: Enhanced readability with syntax highlighting
- **Parallel Execution**: Leverages multiple CPU cores for faster searches
- **Regex Support**: Built-in regex pattern matching without complex syntax

## Use Cases

This MCP server is particularly useful for:

- **Codebase Navigation**: Quickly locate files by name, extension, or pattern across large projects
- **Project Analysis**: Find all files of a specific type (e.g., all Python test files, all configuration files)
- **Code Exploration**: Help AI assistants understand project structure by efficiently listing directories and files
- **Pattern Matching**: Search for files using regex patterns (e.g., find all migration files, test suites)
- **Selective Searches**: Filter by file type, depth, or exclude specific patterns
- **Performance**: Fast searches even in monorepos or large codebases with thousands of files

## Prerequisites

Install fd:
```bash
# Ubuntu/Debian
sudo apt install fd-find

# macOS
brew install fd

# Arch
pacman -S fd
```

## Installation

```bash
cd fd-mcp
pip install -e .
```

## Usage with Claude Code

Add to your Claude Code MCP settings (`~/.claude.json`):

```json
{
  "mcpServers": {
    "fd": {
      "command": "fd-mcp"
    }
  }
}
```

Or run directly:
```json
{
  "mcpServers": {
    "fd": {
      "command": "python",
      "args": ["-m", "fd_mcp.server"],
      "cwd": "/home/th/dev/os/fd-mcp"
    }
  }
}
```

## Tools

### fd_search

Search for files and directories.

| Parameter | Type | Description |
|-----------|------|-------------|
| pattern | string | Regex pattern (optional) |
| path | string | Search directory (default: ".") |
| type | string | f=file, d=dir, l=symlink, x=exec, e=empty |
| extension | string | Filter by extension |
| hidden | bool | Include hidden files |
| no_ignore | bool | Don't respect .gitignore |
| max_depth | int | Max search depth |
| exclude | string | Glob pattern to exclude |
| case_sensitive | bool | Case-sensitive search |
| absolute_path | bool | Return absolute paths |
| max_results | int | Limit results (default: 100) |

### fd_count

Count files matching a pattern.

## Examples

Find all Python files:
```
fd_search(extension="py")
```

Find test files:
```
fd_search(pattern="test_.*", extension="py")
```

List directories only:
```
fd_search(type="d", max_depth=2)
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
