---
description: Search for code patterns using fd-mcp content search
---

Search for code patterns across the codebase using mcp__fd__fd_search_content.

Ask the user what pattern they want to search for, and optionally which file types to search in.

Then use mcp__fd__fd_search_content with:
- search_pattern: the pattern provided by user
- extension: file type if specified (e.g., "py", "js", "md")
- context_lines: 2 (to show surrounding code)

This is 10-100x faster than find -exec grep and shows context around matches.
