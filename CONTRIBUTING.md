# Contributing Guide

Thank you for your interest in contributing to Media Duplicate Finder!

## Getting Started

### 1. Fork and Clone
```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR-USERNAME/media-duplicate-finder.git
cd media-duplicate-finder
```

### 2. Set Up Development Environment
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development tools (optional)
pip install black pylint pytest
```

### 3. Create a Branch
```bash
git checkout -b feature/your-feature-name
# or for bug fixes:
git checkout -b fix/bug-description
```

## Code Style

### Follow PEP 8
- Use 4 spaces for indentation
- Max line length: 88 characters (Black standard)
- Use meaningful variable names

### Docstring Format
```python
def my_function(param1: str, param2: int) -> dict:
    """
    Brief description of what the function does.
    
    Longer description if needed, explaining the algorithm
    or important implementation details.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        dict: Description of return value
        
    Raises:
        ValueError: When something goes wrong
    """
```

### Comment Format
```python
# Use comments for "why", not "what"
# Good
dark_ratio = dark_count / len(THUMB_SAMPLE_POSITIONS)

# Bad
ratio = count / positions  # Calculate ratio
```

### Type Hints
Always include type hints:
```python
def good_function(items: list, count: int) -> tuple:
    pass

# Not ideal
def bad_function(items, count):
    pass
```

## Making Changes

### Code Organization
```
main.py
├── Imports
├── Configuration (CONFIG section)
├── Shared Helpers (HELPERS section)
├── Video Logic (VIDEO section)
├── Image Logic (IMAGE section)
├── Scan & Find (SCAN section)
└── GUI (GUI section)
```

### Adding Features
1. **Update relevant section** in main.py
2. **Add comprehensive docstrings**
3. **Test thoroughly** with various inputs
4. **Update documentation** (README, CONFIG_REFERENCE, etc.)
5. **Add comments** explaining complex logic

### Bug Fixes
1. **Identify root cause** before fixing
2. **Add test case** that reproduces the bug
3. **Fix only the bug** - don't refactor unrelated code
4. **Verify fix** with multiple scenarios

## Testing

### Manual Testing
```bash
# Test video scanning
python main.py
# Select folder with videos, run scan

# Test image scanning
python main.py
# Select folder with images, run scan

# Test deletion
python main.py
# Mark and delete some files
```

### Test Scenarios
- [ ] Empty folder
- [ ] Single file
- [ ] Large folder (100+ files)
- [ ] Mixed videos and images
- [ ] Videos with dark frames
- [ ] Corrupted media files
- [ ] Network drive (if applicable)
- [ ] Long file paths (>260 chars on Windows)

### Performance Testing
```bash
# Time a scan
import time
start = time.time()
# Run scan
end = time.time()
print(f"Scan took {end - start:.2f} seconds")
```

## Pull Request Process

### Before Submitting
1. **Update documentation**
   - README.md (if major feature)
   - CONFIG_REFERENCE.md (if new config options)
   - QUICKSTART.md (if user-facing change)
   - Add docstrings to all functions

2. **Run code checks**
   ```bash
   # Format code
   black main.py
   
   # Check for issues
   pylint main.py  # Warnings are OK, errors are not
   ```

3. **Test thoroughly**
   - Multiple folder types
   - Different file sizes
   - Edge cases

4. **Keep commits clean**
   - One feature per commit
   - Meaningful commit messages
   ```
   ✅ Good: "Add support for HEIC images"
   ❌ Bad: "fixes stuff" or "WIP"
   ```

### Submitting PR
1. Push your branch to GitHub
2. Create Pull Request
3. Fill out PR template with:
   - What problem does this solve?
   - How was it tested?
   - Are there breaking changes?
   - Screenshots/demo (if applicable)

### PR Review
- Respond to comments promptly
- Request re-review after changes
- Be respectful and collaborative

## Areas for Contribution

### High Priority
- [ ] Performance optimization
- [ ] Better error handling
- [ ] Additional file format support
- [ ] Configuration UI
- [ ] Cross-platform testing

### Medium Priority
- [ ] Advanced duplicate detection algorithms
- [ ] Batch processing
- [ ] Export/import features
- [ ] Dark mode variations
- [ ] Internationalization

### Lower Priority
- [ ] Custom color themes
- [ ] Advanced sorting options
- [ ] Database caching for large libraries

## Documentation

### Update README.md when
- Adding major features
- Changing how something works
- Adding new configuration options

### Update CONFIG_REFERENCE.md when
- Adding configuration constants
- Changing default values
- Adding new tuning recommendations

### Update QUICKSTART.md when
- Changing UI flow
- Adding new workflows
- Simplifying common tasks

### Update TROUBLESHOOTING.md when
- Discovering new issues
- Finding better solutions
- Adding platform-specific fixes

## Reporting Bugs

### Good Bug Report
```
Title: Videos not detected in MKV containers

Description:
When scanning a folder with .mkv video files, they are not detected 
by the application.

Expected: .mkv files should appear in results
Actual: Folder contains 5 .mkv files but none appear in scan

Steps to reproduce:
1. Create a folder with test.mkv file
2. Click Browse and select folder
3. Click Start Scan
4. .mkv file is not in results

Environment:
- OS: Windows 11
- Python: 3.11.0
- opencv-python: 4.8.0
```

### Bad Bug Report
```
Title: App doesn't work

Description:
The app won't find my videos

(Not enough information to reproduce)
```

## Feature Requests

### Good Feature Request
```
Title: Add recursive subfolder scanning depth limit

Currently the app scans infinitely deep. For very large folder
hierarchies (network shares), this can be slow. Add an optional
configuration option to limit scan depth.

Example use case:
- User has \media\movies\unwatched\2024\january\week1\...
- They want to scan only 2 levels deep (\media\movies\unwatched)

Suggested implementation:
- Add MAX_RECURSION_DEPTH configuration
- Check depth in scan_folder() function
```

## Development Tips

### Debugging
```python
# Add print statements
print(f"Debug: {variable_name} = {variable_value}")

# Or use pdb
import pdb; pdb.set_trace()
```

### Performance Profiling
```python
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()
# Code to profile
profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats()
```

### Common Mistakes
- ❌ Using `==` for file comparison (use `os.path.samefile()`)
- ❌ Not handling exceptions (wrapped try/except everywhere)
- ❌ Hardcoding paths (use `os.path.join()` for cross-platform)
- ❌ Blocking UI thread (use threading for I/O)
- ❌ Not updating docs (always update when changing code)

## Release Process (Maintainers)

1. Update version in code
2. Update CHANGELOG.md
3. Create release on GitHub
4. Tag with version number

## Questions?

- Check existing issues: https://github.com/project/issues
- Review documentation: README.md, CONFIG_REFERENCE.md
- Look at similar code in the repository
- Ask in PR or issue comments

## Recognition

Contributors will be:
- Mentioned in CHANGELOG.md
- Added to CONTRIBUTORS.md
- Credited in release notes

Thank you for helping make Media Duplicate Finder better! 🎉
