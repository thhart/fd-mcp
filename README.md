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

Install ripgrep (required for `fd_search_content` tool):
```bash
# Ubuntu/Debian
sudo apt install ripgrep

# macOS
brew install ripgrep

# Arch
pacman -S ripgrep

# Or download from: https://github.com/BurntSushi/ripgrep/releases
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

**Replaces: `find`, `locate` commands**

Search for files and directories using fd (5-10x faster than find).

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

### fd_search_content ⭐

**Replaces: `find -exec grep`, `find | xargs grep` commands**

Search for content within files using fd+ripgrep. This is the key tool that replaces `find . -exec grep pattern {} \;` style commands.

| Parameter | Type | Description |
|-----------|------|-------------|
| search_pattern | string | Text/regex to search in files (required) |
| file_pattern | string | Filter files by name pattern |
| path | string | Search directory (default: ".") |
| extension | string | Filter by extension (e.g., "py", "js") |
| type | string | Filter by type (f=file, d=dir, etc.) |
| hidden | bool | Include hidden files |
| no_ignore | bool | Don't respect .gitignore |
| case_sensitive | bool | Case-sensitive search |
| context_lines | int | Lines of context around matches |
| max_results | int | Max files to search (default: 100) |

**Note:** Requires `ripgrep` (rg) to be installed.

### fd_exec

**Replaces: `find -exec`, `find | xargs` commands**

Execute a command on files found by fd. Use `{}` as placeholder for filename.

| Parameter | Type | Description |
|-----------|------|-------------|
| command | string | Command to run (use {} for filename) |
| pattern | string | File name pattern |
| path | string | Search directory (default: ".") |
| type | string | Filter by type |
| extension | string | Filter by extension |
| hidden | bool | Include hidden files |
| no_ignore | bool | Don't respect .gitignore |
| max_files | int | Max files to process (default: 100) |

### fd_recent_files

**Replaces: `find -mtime`, `find -newermt` commands**

Find recently modified files.

| Parameter | Type | Description |
|-----------|------|-------------|
| path | string | Search directory (default: ".") |
| hours | int | Modified within N hours (default: 24) |
| type | string | Filter by type |
| extension | string | Filter by extension |
| max_results | int | Limit results (default: 50) |

### fd_count

**Replaces: `find | wc -l` commands**

Count files matching a pattern.

## Examples

### Basic File Search
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

### Content Search (replaces find -exec grep)

Find "TODO" in all Python files:
```
fd_search_content(search_pattern="TODO", extension="py")
```

Find "import React" in JavaScript/TypeScript files with context:
```
fd_search_content(
    search_pattern="import.*React",
    extension="tsx",
    context_lines=2
)
```

Find error handling in specific directory:
```
fd_search_content(
    search_pattern="try.*except",
    path="src/",
    extension="py"
)
```

### Execute Commands on Files

Count lines in all Python files:
```
fd_exec(command="wc -l {}", extension="py")
```

Format all JavaScript files:
```
fd_exec(command="prettier --write {}", extension="js")
```

### Find Recent Changes

Files modified in last 2 hours:
```
fd_recent_files(hours=2)
```

Recent Python files modified in last day:
```
fd_recent_files(hours=24, extension="py")
```

## Command Replacements

| Old Command | New MCP Tool |
|-------------|--------------|
| `find . -name "*.py"` | `fd_search(extension="py")` |
| `find . -type f -exec grep "TODO" {} \;` | `fd_search_content(search_pattern="TODO")` |
| `find . -name "*.js" -exec prettier {} \;` | `fd_exec(command="prettier {}", extension="js")` |
| `find . -mtime -1` | `fd_recent_files(hours=24)` |
| `find . -type f \| wc -l` | `fd_count(type="f")` |

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
