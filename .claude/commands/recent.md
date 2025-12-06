---
description: Show recently modified files using fd-mcp
---

Show files that were recently modified in this project.

Use mcp__fd__fd_recent_files with hours=24 to show files changed in the last 24 hours.

Ask the user if they want a different time range or specific file types. You can filter by extension if needed.

This is much faster than find -mtime and uses intuitive time parameters (hours instead of confusing day fractions).
