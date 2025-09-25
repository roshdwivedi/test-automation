# Browser Option Conflict Fix

## Problem
The original command using `--browser=firefox` was causing a conflict:
```
ArgumentError: argument --browser: conflicting option string: --browser
```

This error occurred because both your custom `conftest.py` and the `pytest-playwright` plugin were trying to register the same `--browser` command line option.

## Solution
Changed the custom browser option from `--browser` to `--browser-type` to avoid conflicts.

## Updated Commands

### Old Command (causing conflicts):
```bash
pytest tests/ -m smoke -v --tb=short --browser=firefox
```

### New Command (conflict-free):
```bash
pytest tests/ -m smoke -v --tb=short --browser-type=firefox
```

## Supported Browser Types
- `--browser-type=chromium` (default)
- `--browser-type=firefox`
- `--browser-type=webkit`

## CI/CD Pipeline Updates

Update your GitHub Actions or other CI/CD configuration files to use the new option name:

### Before:
```yaml
- name: Run smoke tests
  run: pytest tests/ -m smoke -v --tb=short --browser=firefox
```

### After:
```yaml
- name: Run smoke tests
  run: pytest tests/ -m smoke -v --tb=short --browser-type=firefox
```

## Benefits
- ✅ No conflicts with pytest-playwright or other plugins
- ✅ Works in any environment (local, CI/CD, Docker, etc.)
- ✅ Maintains all existing functionality
- ✅ Clean, simple implementation

## Files Modified
- `conftest.py` - Updated to use `--browser-type` instead of `--browser`

The custom async fixtures (`browser`, `context`, `page`, `authenticated_page`) remain unchanged and work exactly as before.