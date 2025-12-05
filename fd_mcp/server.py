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


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available fd tools."""
    return [
        Tool(
            name="fd_search",
            description="Search for files and directories using fd (fast find alternative). "
            "Supports regex patterns, file type filtering, and respects .gitignore by default.",
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
            name="fd_count",
            description="Count files matching a pattern using fd.",
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
