---
description: Count files by type using fd-mcp
---

Count files in the project by type using mcp__fd__fd_count.

Ask the user what type of files they want to count (e.g., Python, JavaScript, all files).

Then use mcp__fd__fd_count with appropriate parameters:
- extension="py" for Python files
- type="f" for all files
- type="d" for all directories

This is faster than find | wc -l and gives accurate counts respecting .gitignore by default.
