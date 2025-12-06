#!/usr/bin/env python3
"""MCP server for fast file search using fd (fdfind)."""

import asyncio
import shutil
import subprocess
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

# Detect fd binary name (fd on most systems, fdfind on Debian/Ubuntu)
FD_CMD = shutil.which("fd") or shutil.which("fdfind")
RG_CMD = shutil.which("rg")

server = Server("fd-mcp")


def build_fd_command(
    pattern: str = "",
    path: str = ".",
    file_type: str | None = None,
    extension: str | None = None,
    hidden: bool = False,
    no_ignore: bool = False,
    max_depth: int | None = None,
    exclude: str | None = None,
    case_sensitive: bool = False,
    absolute_path: bool = False,
) -> list[str]:
    """Build fd command with arguments."""
    if not FD_CMD:
        raise RuntimeError("fd/fdfind not found in PATH")

    cmd = [FD_CMD]

    if hidden:
        cmd.append("--hidden")
    if no_ignore:
        cmd.append("--no-ignore")
    if case_sensitive:
        cmd.append("--case-sensitive")
    if absolute_path:
        cmd.append("--absolute-path")
    if file_type:
        cmd.extend(["--type", file_type])
    if extension:
        cmd.extend(["--extension", extension])
    if max_depth is not None:
        cmd.extend(["--max-depth", str(max_depth)])
    if exclude:
        cmd.extend(["--exclude", exclude])

    if pattern:
        cmd.append(pattern)
    cmd.append(path)

    return cmd


def run_fd(cmd: list[str], max_results: int = 100) -> str:
    """Execute fd command and return output."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30,
        )
        lines = result.stdout.strip().split("\n") if result.stdout.strip() else []

        if len(lines) > max_results:
            output = "\n".join(lines[:max_results])
            output += f"\n\n... and {len(lines) - max_results} more results (truncated)"
        else:
            output = "\n".join(lines)

        if result.stderr:
            output += f"\n\nWarnings: {result.stderr}"

        return output if output else "No matches found."

    except subprocess.TimeoutExpired:
        return "Error: Command timed out after 30 seconds"
    except Exception as e:
        return f"Error: {e}"


def run_fd_with_content_search(
    search_pattern: str,
    file_pattern: str = "",
    path: str = ".",
    extension: str | None = None,
    file_type: str | None = None,
    hidden: bool = False,
    no_ignore: bool = False,
    case_sensitive: bool = False,
    context_lines: int = 0,
    max_results: int = 100,
) -> str:
    """Search for content within files found by fd using ripgrep."""
    if not RG_CMD:
        return "Error: ripgrep (rg) not found. Please install ripgrep for content search."

    # Build fd command to find files
    fd_cmd = [FD_CMD]
    if hidden:
        fd_cmd.append("--hidden")
    if no_ignore:
        fd_cmd.append("--no-ignore")
    if file_type:
        fd_cmd.extend(["--type", file_type])
    if extension:
        fd_cmd.extend(["--extension", extension])
    if file_pattern:
        fd_cmd.append(file_pattern)
    fd_cmd.append(path)

    # Build ripgrep command
    rg_cmd = [RG_CMD]
    if not case_sensitive:
        rg_cmd.append("--ignore-case")
    if context_lines > 0:
        rg_cmd.extend(["--context", str(context_lines)])
    rg_cmd.extend(["--line-number", "--heading", "--color=never"])
    rg_cmd.append(search_pattern)

    try:
        # Get file list from fd
        fd_result = subprocess.run(
            fd_cmd,
            capture_output=True,
            text=True,
            timeout=30,
        )

        if not fd_result.stdout.strip():
            return "No files found matching the file pattern."

        files = fd_result.stdout.strip().split("\n")

        # Search content with ripgrep in found files
        rg_cmd.extend(files[:max_results])

        rg_result = subprocess.run(
            rg_cmd,
            capture_output=True,
            text=True,
            timeout=30,
        )

        if rg_result.returncode == 0:
            output = rg_result.stdout.strip()
            if len(files) > max_results:
                output += f"\n\n... searched {max_results} of {len(files)} files (truncated)"
            return output if output else "No content matches found."
        elif rg_result.returncode == 1:
            return "No content matches found in the files."
        else:
            return f"Error: {rg_result.stderr}"

    except subprocess.TimeoutExpired:
        return "Error: Command timed out after 30 seconds"
    except Exception as e:
        return f"Error: {e}"


def run_fd_exec(
    command: str,
    pattern: str = "",
    path: str = ".",
    file_type: str | None = None,
    extension: str | None = None,
    hidden: bool = False,
    no_ignore: bool = False,
    max_files: int = 100,
) -> str:
    """Execute a command on files found by fd (replacement for find -exec)."""
    # Build fd command
    fd_cmd = build_fd_command(
        pattern=pattern,
        path=path,
        file_type=file_type,
        extension=extension,
        hidden=hidden,
        no_ignore=no_ignore,
    )

    try:
        # Get file list
        fd_result = subprocess.run(
            fd_cmd,
            capture_output=True,
            text=True,
            timeout=30,
        )

        if not fd_result.stdout.strip():
            return "No files found."

        files = fd_result.stdout.strip().split("\n")[:max_files]

        # Execute command on each file
        results = []
        for file in files:
            cmd = command.replace("{}", file)
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=10,
            )
            if result.stdout or result.stderr:
                results.append(f"{file}:\n{result.stdout}{result.stderr}")

        if results:
            output = "\n\n".join(results)
            if len(files) == max_files:
                output += f"\n\n... processed {max_files} files (limit reached)"
            return output
        else:
            return f"Command executed on {len(files)} files (no output)"

    except Exception as e:
        return f"Error: {e}"


def find_recent_files(
    path: str = ".",
    hours: int = 24,
    file_type: str | None = None,
    extension: str | None = None,
    max_results: int = 50,
) -> str:
    """Find recently modified files using fd."""
    # Build fd command with change-newer-than
    cmd = [FD_CMD, "--changed-within", f"{hours}h"]

    if file_type:
        cmd.extend(["--type", file_type])
    if extension:
        cmd.extend(["--extension", extension])

    cmd.append(path)

    return run_fd(cmd, max_results)


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available fd tools."""
    tools = [
        Tool(
            name="fd_search",
            description="⚡ FAST FILE SEARCH: 5-10x faster than 'find' - Use this for ALL file/directory searches. "
            "Parallel execution with smart defaults (.gitignore respected automatically). "
            "WHEN TO USE: Anytime you think 'find' or need to locate files by name/pattern/type. "
            "Quick examples: Python files? → extension='py' | Test files? → pattern='test_.*' | Directories? → type='d'. "
            "Replaces: find, locate commands. This is your go-to tool for file discovery.",
            inputSchema={
                "type": "object",
                "properties": {
                    "pattern": {
                        "type": "string",
                        "description": "Search pattern (regex). Leave empty to list all files.",
                    },
                    "path": {
                        "type": "string",
                        "description": "Directory to search in. Defaults to current directory.",
                        "default": ".",
                    },
                    "type": {
                        "type": "string",
                        "enum": ["f", "d", "l", "x", "e", "s", "p"],
                        "description": "Filter by type: f=file, d=directory, l=symlink, x=executable, e=empty, s=socket, p=pipe",
                    },
                    "extension": {
                        "type": "string",
                        "description": "Filter by file extension (e.g., 'py', 'js', 'txt')",
                    },
                    "hidden": {
                        "type": "boolean",
                        "description": "Include hidden files and directories",
                        "default": False,
                    },
                    "no_ignore": {
                        "type": "boolean",
                        "description": "Don't respect .gitignore and other ignore files",
                        "default": False,
                    },
                    "max_depth": {
                        "type": "integer",
                        "description": "Maximum search depth",
                    },
                    "exclude": {
                        "type": "string",
                        "description": "Exclude entries matching this glob pattern",
                    },
                    "case_sensitive": {
                        "type": "boolean",
                        "description": "Use case-sensitive search",
                        "default": False,
                    },
                    "absolute_path": {
                        "type": "boolean",
                        "description": "Return absolute paths instead of relative",
                        "default": False,
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of results to return",
                        "default": 100,
                    },
                },
                "required": [],
            },
        ),
        Tool(
            name="fd_search_content",
            description="🔍 BLAZING CONTENT SEARCH: Lightning-fast code search using fd+ripgrep (10-100x faster than find -exec grep). "
            "WHEN TO USE: Searching for text/code patterns across multiple files. This is THE tool for 'grep in files'. "
            "One-shot operation: filters files AND searches content simultaneously. "
            "Example: Find 'TODO' in Python → search_pattern='TODO', extension='py' | Find imports → search_pattern='import.*React'. "
            "Replaces: find -exec grep, find | xargs grep, recursive grep. Always prefer this over bash grep commands.",
            inputSchema={
                "type": "object",
                "properties": {
                    "search_pattern": {
                        "type": "string",
                        "description": "Text or regex pattern to search for in file contents (required)",
                    },
                    "file_pattern": {
                        "type": "string",
                        "description": "Limit to files matching this name pattern (e.g., 'test_*', '*.config.*')",
                        "default": "",
                    },
                    "path": {
                        "type": "string",
                        "description": "Directory to search in",
                        "default": ".",
                    },
                    "extension": {
                        "type": "string",
                        "description": "Filter by file extension (e.g., 'py', 'js', 'rs')",
                    },
                    "type": {
                        "type": "string",
                        "enum": ["f", "d", "l", "x"],
                        "description": "Filter by type: f=file (default), d=directory, l=symlink, x=executable",
                    },
                    "hidden": {
                        "type": "boolean",
                        "description": "Include hidden files",
                        "default": False,
                    },
                    "no_ignore": {
                        "type": "boolean",
                        "description": "Don't respect .gitignore files",
                        "default": False,
                    },
                    "case_sensitive": {
                        "type": "boolean",
                        "description": "Use case-sensitive search",
                        "default": False,
                    },
                    "context_lines": {
                        "type": "integer",
                        "description": "Number of context lines to show around matches",
                        "default": 0,
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of files to search",
                        "default": 100,
                    },
                },
                "required": ["search_pattern"],
            },
        ),
        Tool(
            name="fd_exec",
            description="⚙️ FAST BULK OPERATIONS: Execute commands on multiple files (faster & safer than find -exec). "
            "WHEN TO USE: Need to run a command on many files matching a pattern (format, count, process, etc.). "
            "Use {} as filename placeholder. Built-in safety limits prevent runaway operations. "
            "Examples: Count lines in Python files → command='wc -l {}', extension='py' | Format JS → command='prettier {}', extension='js'. "
            "Replaces: find -exec, find | xargs. Modern replacement for batch file operations.",
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "Command to execute on each file. Use {} as placeholder for filename (required)",
                    },
                    "pattern": {
                        "type": "string",
                        "description": "Search pattern to filter files (regex)",
                        "default": "",
                    },
                    "path": {
                        "type": "string",
                        "description": "Directory to search in",
                        "default": ".",
                    },
                    "type": {
                        "type": "string",
                        "enum": ["f", "d", "l", "x"],
                        "description": "Filter by type: f=file, d=directory, l=symlink, x=executable",
                    },
                    "extension": {
                        "type": "string",
                        "description": "Filter by file extension",
                    },
                    "hidden": {
                        "type": "boolean",
                        "description": "Include hidden files",
                        "default": False,
                    },
                    "no_ignore": {
                        "type": "boolean",
                        "description": "Don't respect .gitignore",
                        "default": False,
                    },
                    "max_files": {
                        "type": "integer",
                        "description": "Maximum number of files to process",
                        "default": 100,
                    },
                },
                "required": ["command"],
            },
        ),
        Tool(
            name="fd_recent_files",
            description="🕐 RECENT CHANGES FINDER: Instantly find recently modified files (faster than find -mtime). "
            "WHEN TO USE: Investigating recent changes, debugging 'what changed?', reviewing work, finding active files. "
            "Time-based filtering with simple hour parameter. "
            "Examples: Last 2 hours → hours=2 | Today's work → hours=24 | Recent Python changes → hours=24, extension='py'. "
            "Replaces: find -mtime, find -newermt. Essential for tracking codebase activity.",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Directory to search in",
                        "default": ".",
                    },
                    "hours": {
                        "type": "integer",
                        "description": "Find files modified within this many hours",
                        "default": 24,
                    },
                    "type": {
                        "type": "string",
                        "enum": ["f", "d", "l", "x"],
                        "description": "Filter by type: f=file, d=directory, l=symlink, x=executable",
                    },
                    "extension": {
                        "type": "string",
                        "description": "Filter by file extension",
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of results",
                        "default": 50,
                    },
                },
                "required": [],
            },
        ),
        Tool(
            name="fd_count",
            description="📊 FAST FILE COUNTER: Quickly count files matching patterns (faster than find | wc -l). "
            "WHEN TO USE: Getting file counts, analyzing codebase size, inventory checks. "
            "Examples: Count Python files → extension='py' | Count all files → type='f' | Count in directory → path='src/'. "
            "Replaces: find | wc -l. Simple, fast, accurate.",
            inputSchema={
                "type": "object",
                "properties": {
                    "pattern": {
                        "type": "string",
                        "description": "Search pattern (regex)",
                    },
                    "path": {
                        "type": "string",
                        "description": "Directory to search in",
                        "default": ".",
                    },
                    "type": {
                        "type": "string",
                        "enum": ["f", "d", "l", "x", "e"],
                        "description": "Filter by type",
                    },
                    "extension": {
                        "type": "string",
                        "description": "Filter by extension",
                    },
                    "hidden": {
                        "type": "boolean",
                        "default": False,
                    },
                },
                "required": [],
            },
        ),
    ]

    # Only include fd_search_content if ripgrep is available
    if not RG_CMD:
        tools = [t for t in tools if t.name != "fd_search_content"]

    return tools


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Execute fd tool."""
    if name == "fd_search":
        cmd = build_fd_command(
            pattern=arguments.get("pattern", ""),
            path=arguments.get("path", "."),
            file_type=arguments.get("type"),
            extension=arguments.get("extension"),
            hidden=arguments.get("hidden", False),
            no_ignore=arguments.get("no_ignore", False),
            max_depth=arguments.get("max_depth"),
            exclude=arguments.get("exclude"),
            case_sensitive=arguments.get("case_sensitive", False),
            absolute_path=arguments.get("absolute_path", False),
        )
        max_results = arguments.get("max_results", 100)
        output = run_fd(cmd, max_results)
        return [TextContent(type="text", text=output)]

    elif name == "fd_search_content":
        output = run_fd_with_content_search(
            search_pattern=arguments["search_pattern"],
            file_pattern=arguments.get("file_pattern", ""),
            path=arguments.get("path", "."),
            extension=arguments.get("extension"),
            file_type=arguments.get("type"),
            hidden=arguments.get("hidden", False),
            no_ignore=arguments.get("no_ignore", False),
            case_sensitive=arguments.get("case_sensitive", False),
            context_lines=arguments.get("context_lines", 0),
            max_results=arguments.get("max_results", 100),
        )
        return [TextContent(type="text", text=output)]

    elif name == "fd_exec":
        output = run_fd_exec(
            command=arguments["command"],
            pattern=arguments.get("pattern", ""),
            path=arguments.get("path", "."),
            file_type=arguments.get("type"),
            extension=arguments.get("extension"),
            hidden=arguments.get("hidden", False),
            no_ignore=arguments.get("no_ignore", False),
            max_files=arguments.get("max_files", 100),
        )
        return [TextContent(type="text", text=output)]

    elif name == "fd_recent_files":
        output = find_recent_files(
            path=arguments.get("path", "."),
            hours=arguments.get("hours", 24),
            file_type=arguments.get("type"),
            extension=arguments.get("extension"),
            max_results=arguments.get("max_results", 50),
        )
        return [TextContent(type="text", text=output)]

    elif name == "fd_count":
        cmd = build_fd_command(
            pattern=arguments.get("pattern", ""),
            path=arguments.get("path", "."),
            file_type=arguments.get("type"),
            extension=arguments.get("extension"),
            hidden=arguments.get("hidden", False),
        )
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            lines = result.stdout.strip().split("\n") if result.stdout.strip() else []
            count = len([l for l in lines if l])
            return [TextContent(type="text", text=f"Found {count} matches")]
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {e}")]

    return [TextContent(type="text", text=f"Unknown tool: {name}")]


async def run_server():
    """Run the MCP server with stdio transport."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


def main():
    """Entry point for the MCP server."""
    if not FD_CMD:
        print("Error: fd/fdfind not found. Please install fd-find.", file=__import__("sys").stderr)
        __import__("sys").exit(1)

    asyncio.run(run_server())


if __name__ == "__main__":
    main()
