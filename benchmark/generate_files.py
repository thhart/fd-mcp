#!/usr/bin/env python3
"""
Fast file generator for fd-mcp benchmarks
"""
import os
import sys
import argparse
from pathlib import Path


def create_file(filepath, content):
    """Create a file with the given content"""
    with open(filepath, 'w') as f:
        f.write(content)


def main():
    parser = argparse.ArgumentParser(description='Generate benchmark test files')
    parser.add_argument('-n', '--num-files', type=int, default=100000,
                       help='Number of files to generate (default: 100000)')
    args = parser.parse_args()

    file_count = args.num_files

    if file_count < 100:
        print(f"Error: File count must be >= 100")
        sys.exit(1)

    # Setup paths
    script_dir = Path(__file__).parent
    test_data_dir = script_dir / 'test_data'

    print(f"🔧 Setting up benchmark test data...")
    print(f"📊 Target file count: {file_count}")

    # Clean and create directories
    if test_data_dir.exists():
        print("Removing existing test data...")
        import shutil
        shutil.rmtree(test_data_dir)

    dirs = ['src', 'tests', 'docs', 'config', 'scripts', 'lib', 'examples']
    for dir_name in dirs:
        (test_data_dir / dir_name).mkdir(parents=True, exist_ok=True)

    print(f"📁 Creating {file_count} test files...")

    # Calculate file distribution
    py_src_files = int(file_count * 0.15)
    py_helpers = int(file_count * 0.05)
    test_files = int(file_count * 0.15)
    js_components = int(file_count * 0.10)
    js_utils = int(file_count * 0.05)
    json_config = int(file_count * 0.05)
    yaml_config = int(file_count * 0.05)
    docs = int(file_count * 0.10)
    scripts = int(file_count * 0.08)
    py_lib = int(file_count * 0.04)
    js_lib = int(file_count * 0.03)
    examples = int(file_count * 0.10)
    txt_files = int(file_count * 0.03)
    env_files = int(file_count * 0.01)
    readme_files = int(file_count * 0.01)

    total_allocated = (py_src_files + py_helpers + test_files + js_components + js_utils +
                      json_config + yaml_config + docs + scripts + py_lib + js_lib +
                      examples + txt_files + env_files + readme_files)
    remaining = file_count - total_allocated
    legacy_files = int(remaining * 0.6)
    integration_tests = remaining - legacy_files

    count = 0

    # 1. Python source files
    if py_src_files > 0:
        print(f"  Creating Python source files ({py_src_files} files)...")
        for i in range(1, py_src_files + 1):
            create_file(test_data_dir / 'src' / f'module_{i}.py',
                       f"""class Module{i}:
    def __init__(self):
        self.value = {i}

    def process(self):
        return self.value * 2""")
            count += 1

    # 2. Python helpers
    if py_helpers > 0:
        print(f"  Creating Python helper files ({py_helpers} files)...")
        for i in range(1, py_helpers + 1):
            create_file(test_data_dir / 'src' / f'helper_{i}.py',
                       f"""# Helper module {i}
def helper_function_{i}(x):
    # TODO: Implement logic
    return x + {i}

def another_helper(y):
    # FIXME: This needs optimization
    return y * {i}""")
            count += 1

    # 3. Test files
    if test_files > 0:
        print(f"  Creating test files ({test_files} files)...")
        for i in range(1, test_files + 1):
            create_file(test_data_dir / 'tests' / f'test_module_{i}.py',
                       f"""import unittest
from src.module_{i} import Module{i}

class TestModule{i}(unittest.TestCase):
    def test_init(self):
        # TODO: Add more tests
        obj = Module{i}()
        self.assertEqual(obj.value, {i})

    def test_process(self):
        obj = Module{i}()
        result = obj.process()
        self.assertEqual(result, {i} * 2)""")
            count += 1

    # 4. JavaScript components
    if js_components > 0:
        print(f"  Creating JavaScript component files ({js_components} files)...")
        for i in range(1, js_components + 1):
            create_file(test_data_dir / 'src' / f'component_{i}.js',
                       f"""export class Component{i} {{
    constructor() {{
        this.state = {{ value: {i} }};
    }}

    render() {{
        // TODO: Implement render logic
        return this.state.value;
    }}
}}""")
            count += 1

    # 5. JavaScript utilities
    if js_utils > 0:
        print(f"  Creating JavaScript utility files ({js_utils} files)...")
        for i in range(1, js_utils + 1):
            create_file(test_data_dir / 'src' / f'util_{i}.js',
                       f"""// Utility functions
export function calculateValue{i}(x) {{
    // FIXME: Error handling needed
    return x * {i};
}}

export function processData{i}(data) {{
    return data.map(x => x + {i});
}}""")
            count += 1

    # 6. JSON config
    if json_config > 0:
        print(f"  Creating JSON config files ({json_config} files)...")
        for i in range(1, json_config + 1):
            create_file(test_data_dir / 'config' / f'config_{i}.json',
                       f"""{{
  "name": "config_{i}",
  "version": "1.0.{i}",
  "settings": {{
    "enabled": true,
    "value": {i}
  }}
}}""")
            count += 1

    # 7. YAML config
    if yaml_config > 0:
        print(f"  Creating YAML config files ({yaml_config} files)...")
        for i in range(1, yaml_config + 1):
            create_file(test_data_dir / 'config' / f'settings_{i}.yaml',
                       f"""name: settings_{i}
version: 1.0.{i}
settings:
  enabled: true
  value: {i}
  description: 'Configuration file {i}'""")
            count += 1

    # 8. Documentation
    if docs > 0:
        print(f"  Creating documentation files ({docs} files)...")
        for i in range(1, docs + 1):
            create_file(test_data_dir / 'docs' / f'doc_{i}.md',
                       f"""# Documentation {i}

## Overview
This is documentation file number {i}.

## TODO
- Add more examples
- Update API reference
- Fix typos

## Examples
```python
from module_{i} import Module{i}
obj = Module{i}()
result = obj.process()
```

## Notes
FIXME: This section needs review.""")
            count += 1

    # 9. Shell scripts
    if scripts > 0:
        print(f"  Creating shell scripts ({scripts} files)...")
        for i in range(1, scripts + 1):
            script_path = test_data_dir / 'scripts' / f'script_{i}.sh'
            create_file(script_path,
                       f"""#!/bin/bash
# Script {i}
# TODO: Add error handling

function main() {{
    echo "Running script {i}"
    # FIXME: Add validation
    local value={i}
    echo "Value: $value"
}}

main "$@" """)
            script_path.chmod(0o755)
            count += 1

    # 10. Python library
    if py_lib > 0:
        print(f"  Creating Python library files ({py_lib} files)...")
        for i in range(1, py_lib + 1):
            create_file(test_data_dir / 'lib' / f'library_{i}.py',
                       f'''"""Library module {i}"""

class Library{i}:
    """TODO: Add class documentation"""

    def __init__(self):
        self.name = 'library_{i}'

    def execute(self):
        # FIXME: Implement logic
        pass''')
            count += 1

    # 11. JavaScript library
    if js_lib > 0:
        print(f"  Creating JavaScript library files ({js_lib} files)...")
        for i in range(1, js_lib + 1):
            create_file(test_data_dir / 'lib' / f'common_{i}.js',
                       f"""/**
 * Common utilities {i}
 * TODO: Add JSDoc comments
 */

export const CONSTANT_{i} = {i};

export function commonFunction{i}() {{
    // FIXME: Add implementation
    return CONSTANT_{i};
}}""")
            count += 1

    # 12. Examples
    if examples > 0:
        print(f"  Creating example files ({examples} files)...")
        for i in range(1, examples + 1):
            create_file(test_data_dir / 'examples' / f'example_{i}.py',
                       f'''#!/usr/bin/env python3
"""Example {i}"""

# TODO: Add more examples

def example_{i}():
    """
    Example function {i}
    FIXME: Add proper error handling
    """
    value = {i}
    result = value * 2
    print(f"Result: {{result}}")
    return result

if __name__ == '__main__':
    example_{i}()''')
            count += 1

    # 13. Text files
    if txt_files > 0:
        print(f"  Creating text data files ({txt_files} files)...")
        for i in range(1, txt_files + 1):
            create_file(test_data_dir / 'src' / f'data_{i}.txt',
                       f"""Data file {i}
This is a text file with some content.
TODO: Process this data
Line {i}
FIXME: Review content""")
            count += 1

    # 14. Env files
    if env_files > 0:
        print(f"  Creating environment files ({env_files} files)...")
        for i in range(1, env_files + 1):
            create_file(test_data_dir / 'config' / f'env_{i}.env',
                       f"""# Environment {i}
VAR_{i}=value_{i}
DEBUG=true
# TODO: Add more variables""")
            count += 1

    # 15. README files
    if readme_files > 0:
        print(f"  Creating README files ({readme_files} files)...")
        for i in range(1, readme_files + 1):
            create_file(test_data_dir / 'docs' / f'README_{i}.md',
                       f"""# README {i}

Project documentation {i}.

## TODO
- Complete documentation
- Add examples""")
            count += 1

    # 16. Legacy files
    if legacy_files > 0:
        print(f"  Creating legacy Python files ({legacy_files} files)...")
        for i in range(1, legacy_files + 1):
            create_file(test_data_dir / 'src' / f'legacy_{i}.py',
                       f"""# Legacy code {i}
# DEPRECATED: This module is deprecated
# TODO: Remove in next version

def old_function_{i}():
    return {i}""")
            count += 1

    # 17. Integration tests
    if integration_tests > 0:
        print(f"  Creating integration test files ({integration_tests} files)...")
        for i in range(1, integration_tests + 1):
            create_file(test_data_dir / 'tests' / f'integration_test_{i}.py',
                       f"""# Integration test {i}
# TODO: Add more test cases

def test_integration_{i}():
    assert True  # FIXME: Real test needed""")
            count += 1

    print()
    print("✅ Setup complete!")
    print(f"📊 Created {count} files in {test_data_dir}")
    print()

    # Verify file count
    import subprocess
    result = subprocess.run(['find', str(test_data_dir), '-type', 'f'],
                          capture_output=True, text=True)
    actual_count = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0

    if actual_count == file_count:
        print(f"✓ File count verification: {actual_count} files (matches target)")
    else:
        print(f"⚠ File count verification: {actual_count} files (target was {file_count})")

    print()
    print("File distribution:")

    # Count by extension
    for ext, name in [('*.py', 'Python files'), ('*.js', 'JavaScript files'),
                      ('*.json', 'JSON files'), ('*.yaml', 'YAML files'),
                      ('*.md', 'Markdown files'), ('*.sh', 'Shell scripts'),
                      ('*.txt', 'Text files'), ('*.env', 'Env files')]:
        result = subprocess.run(['find', str(test_data_dir), '-type', 'f', '-name', ext],
                              capture_output=True, text=True)
        ext_count = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
        print(f"  {name:20s} {ext_count}")

    print()
    print("Ready to run benchmarks with: ./run_benchmark.sh")


if __name__ == '__main__':
    main()
