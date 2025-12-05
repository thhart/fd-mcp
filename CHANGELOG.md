# Changelog

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
