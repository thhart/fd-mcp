# Changelog

## [0.2.2] - 2025-12-06

### Changed
- **Breaking API change**: Made `pattern` and `path` parameters required for `fd_search` and `fd_count` tools
- Updated all documentation examples to include both required parameters
- Pattern parameter now explicitly documented to use `".*"` or `""` for matching all files

### Announced
- **Recursive search support**: All fd-mcp tools support recursive directory traversal by default
- Added `max_depth` parameter documentation for controlling recursion depth
- Highlighted that no special flags are needed for recursive searching (unlike traditional `find -r`)

### Documentation
- Added new "Tip 1: Required Parameters" section in CLAUDE.md with examples
- Added new "Tip 3: Recursive Search" section in CLAUDE.md with depth control examples
- Updated README.md with parameter tables showing required fields
- Updated all code examples across README.md and CLAUDE.md to use required parameters
- Added "Recursive by Default" to feature highlights in README.md

## [0.2.1] - 2025-12-06

### Added
- **Comprehensive CLAUDE.md documentation**: Educational guide with usage patterns, decision trees, and before/after examples
- **Slash commands**: Added `/find-py`, `/search-code`, `/recent`, `/count-files`, and `/demo-mcp` for quick demonstrations
- **Claude Code integration guide**: Enhanced README with best practices, performance comparisons, and tool selection guidance

### Changed
- **Supercharged tool descriptions**: Rewrote all tool descriptions with eye-catching emojis, performance metrics upfront, and clear "WHEN TO USE" sections
- Tool descriptions now lead with benefits (5-10x faster) instead of burying them
- Added psychological triggers and action-oriented language to make tools more discoverable
- Improved discoverability through better formatting and inline examples

### Documentation
- Added performance comparison tables showing concrete speed improvements
- Created decision tree for tool selection
- Added 5 detailed usage patterns with bash vs MCP comparisons
- Included advanced tips and best practices
- Added quick reference guides and mental model shift guidance

## [0.2.0] - 2025-12-06

### Added
- **`fd_search_content` tool**: Search content within files using fd+ripgrep (replaces `find -exec grep`)
- **`fd_exec` tool**: Execute commands on found files (replaces `find -exec` and `find | xargs`)
- **`fd_recent_files` tool**: Find recently modified files (replaces `find -mtime`)
- Ripgrep integration for fast content searching
- Context lines support in content search
- Command execution with placeholder support (`{}`)

### Changed
- Enhanced all tool descriptions to emphasize being preferred alternatives to `find` commands
- Added "PREFERRED ALTERNATIVE to 'find'" to tool descriptions for better Claude Code integration
- Improved README with comprehensive examples and command replacement table
- Better tool discoverability with explicit "Replaces:" statements

### Technical
- Auto-detection of ripgrep (rg) binary
- Graceful fallback when ripgrep is not available (fd_search_content tool disabled)
- Improved error handling for content search operations

## [0.1.0] - 2025-12-05

### Added
- Initial release
- `fd_search` tool: Search files/directories with pattern, type, extension filters
- `fd_count` tool: Count matching files
- Support for hidden files, gitignore bypass, max depth, exclusions
- Auto-detection of fd/fdfind binary
- Result truncation for large result sets
