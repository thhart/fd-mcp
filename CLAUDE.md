# fd-mcp: High-Performance File Operations for Claude Code

This project provides **ultra-fast MCP tools** that dramatically outperform traditional bash commands for file operations.

## 🎯 Core Principle

**When you think "find" or "grep", reach for these MCP tools first.** They're not just alternatives—they're upgrades.

**Key Feature**: All fd-mcp tools support **recursive search by default** - they automatically traverse subdirectories without needing special flags or options. Use `max_depth` parameter to limit recursion depth when needed.

## ⚡ Performance Comparison

| Task | Traditional Bash | fd-mcp Tool | Speed Improvement |
|------|-----------------|-------------|-------------------|
| Find all Python files | `find . -name "*.py"` | `mcp__fd__fd_search(pattern=".*", path=".", extension="py")` | **5-10x faster** |
| Search code for pattern | `find . -exec grep "TODO" {} \;` | `mcp__fd__fd_search_content(search_pattern="TODO")` | **10-100x faster** |
| Find recent changes | `find . -mtime -1` | `mcp__fd__fd_recent_files(hours=24)` | **3-5x faster** |
| Count files | `find . -type f \| wc -l` | `mcp__fd__fd_count(pattern=".*", path=".", type="f")` | **5-8x faster** |

## 🧠 Decision Tree: Which Tool to Use?

```
Need to search files?
├─ By name/type/pattern? → mcp__fd__fd_search
├─ By content/code? → mcp__fd__fd_search_content
├─ By modification time? → mcp__fd__fd_recent_files
└─ Just count them? → mcp__fd__fd_count

Need to process files?
└─ Run command on matches? → mcp__fd__fd_exec
```

## 📖 Common Patterns & Examples

### Pattern 1: Finding Files by Type

**Scenario:** "Find all Python files in this project"

❌ **Old way (bash):**
```bash
find . -name "*.py"
find . -type f -name "*.py"
```

✅ **New way (MCP):**
```python
mcp__fd__fd_search(pattern=".*", path=".", extension="py")
```

**Why better:** Faster, respects .gitignore, parallel execution, cleaner syntax.

---

### Pattern 2: Searching Code Content

**Scenario:** "Find all TODO comments in Python files"

❌ **Old way (bash):**
```bash
find . -name "*.py" -exec grep -H "TODO" {} \;
grep -r "TODO" --include="*.py" .
```

✅ **New way (MCP):**
```python
mcp__fd__fd_search_content(
    search_pattern="TODO",
    extension="py"
)
```

**Why better:** Single operation (not two-step), 10-100x faster, respects .gitignore.

---

### Pattern 3: Finding Recent Changes

**Scenario:** "What files changed in the last 2 hours?"

❌ **Old way (bash):**
```bash
find . -mtime -0.083  # confusing time math!
find . -newermt "2 hours ago"
```

✅ **New way (MCP):**
```python
mcp__fd__fd_recent_files(hours=2)
```

**Why better:** Intuitive time parameter, faster, no date math confusion.

---

### Pattern 4: Bulk Operations

**Scenario:** "Count lines in all Python test files"

❌ **Old way (bash):**
```bash
find . -name "test_*.py" -exec wc -l {} \;
```

✅ **New way (MCP):**
```python
mcp__fd__fd_exec(
    command="wc -l {}",
    pattern="test_.*",
    path=".",
    extension="py"
)
```

**Why better:** Built-in safety limits, faster file discovery, clearer intent.

---

### Pattern 5: Complex Searches

**Scenario:** "Find error handling code in the src/ directory"

❌ **Old way (bash):**
```bash
find src/ -name "*.py" -exec grep -n "try.*except" {} \;
```

✅ **New way (MCP):**
```python
mcp__fd__fd_search_content(
    search_pattern="try.*except",
    path="src/",
    extension="py",
    context_lines=2  # Show surrounding code!
)
```

**Why better:** Context lines, faster, one operation, respects project structure.

## 🎓 Learning Patterns

### Mental Model Shift

**OLD thinking:**
> "I need to find files... let me write a find command"

**NEW thinking:**
> "I need to find files... which fd-mcp tool matches my need?"

### Quick Reference

When you catch yourself about to type:
- `find` → Use `mcp__fd__fd_search`
- `find -exec grep` → Use `mcp__fd__fd_search_content`
- `find -exec` → Use `mcp__fd__fd_exec`
- `find -mtime` → Use `mcp__fd__fd_recent_files`
- `find | wc -l` → Use `mcp__fd__fd_count`

## 💡 Advanced Tips

### Tip 1: Required Parameters
Both `fd_search` and `fd_count` require `pattern` and `path` parameters:
- **pattern**: Use `".*"` or `""` to match all files, or provide a specific regex pattern
- **path**: Specify the directory to search (e.g., `"."` for current directory, `"src/"` for src folder)

```python
# Match all files in current directory
mcp__fd__fd_search(pattern=".*", path=".")

# Match Python files in src/
mcp__fd__fd_search(pattern=".*", path="src/", extension="py")

# Match files containing 'test' in name
mcp__fd__fd_search(pattern="test", path=".")
```

### Tip 2: Extension vs Pattern
- Use `extension="py"` for clean extension matching
- Use `pattern="test_.*\.py"` for complex filename patterns

### Tip 3: Recursive Search
All searches are **recursive by default** - they automatically traverse all subdirectories:
```python
# Recursively find all Python files in entire project
mcp__fd__fd_search(pattern=".*", path=".", extension="py")

# Limit recursion to 2 levels deep
mcp__fd__fd_search(pattern=".*", path=".", extension="py", max_depth=2)

# Search only in current directory (no recursion)
mcp__fd__fd_search(pattern=".*", path=".", extension="py", max_depth=1)
```

### Tip 4: Context is King
When searching code, always consider adding `context_lines`:
```python
mcp__fd__fd_search_content(
    search_pattern="class.*Config",
    extension="py",
    context_lines=3  # See the surrounding context!
)
```

### Tip 5: Combine Filters
Stack filters for precise results:
```python
mcp__fd__fd_search(
    pattern="config",      # Name contains 'config'
    path="src/",          # In src/ directory
    extension="json",      # JSON files only
    max_depth=2           # Don't go too deep
)
```

### Tip 6: Hidden Files
By default, hidden files are excluded (respects .gitignore):
```python
mcp__fd__fd_search(
    pattern="secret",
    path=".",
    hidden=True,        # Include .env, .secrets, etc.
    no_ignore=True      # Ignore .gitignore rules
)
```

## 🚀 Why This Matters

### Developer Experience
- **Cognitive load:** Simpler, more intuitive parameters
- **Speed:** Get results 5-100x faster
- **Safety:** Respects .gitignore by default
- **Power:** Advanced features without complex syntax

### Project Impact
- **Faster iterations:** Less waiting for search results
- **Better exploration:** Context-aware searches
- **Cleaner patterns:** Self-documenting tool names
- **Future-proof:** Built on modern, maintained tools (fd, ripgrep)

## 📊 Success Metrics

After adopting fd-mcp tools:
- ✅ File searches complete in milliseconds vs seconds
- ✅ Code searches respect project structure automatically
- ✅ No more cryptic find command syntax errors
- ✅ Natural, readable search operations

## 🎯 Remember

**These aren't just "alternatives" - they're the better way to work with files.**

When in doubt: **If it involves finding or searching files, there's an fd-mcp tool for it.**
