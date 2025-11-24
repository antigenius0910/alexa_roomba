# Python 3 Migration Plan

## Overview
This document outlines the migration of the alexa_roomba project from Python 2 to Python 3. The project currently uses Python 2 syntax and dependencies that are incompatible with Python 3.

## Migration Status: In Progress

## Issues Identified

### 1. Print Statements (High Priority)
Print statements without parentheses are used throughout the codebase.

**Files affected:**
- `create.py` - 60+ instances
- `fauxmo.py` - 4 instances (lines 320, 345, 480, 484)
- `example-minimal.py` - 1 instance (line 30)
- `example-mqtt.py` - 2 instances (lines 31, 34)

**Fix:** Convert all `print "text"` to `print("text")`

### 2. Exception Syntax (High Priority)
Old-style exception handling `except Exception, e:` is incompatible with Python 3.

**Files affected:**
- `fauxmo.py` - Lines 416, 422, 426, 459, 532
- `example-minimal.py` - Line 54
- `example-mqtt.py` - Line 64
- `RPi_name_port_gpio.py` - Line 52
- `CHIP_name_port_gpio.py` - Line 55

**Fix:** Convert to `except Exception as e:`

### 3. Serial Communication - chr() Usage (Critical Priority)
The code extensively uses `chr()` to create byte commands for serial communication. In Python 2, `chr()` returns a string (which is also bytes), but in Python 3, `chr()` returns a Unicode character. Serial communication requires bytes in Python 3.

**Files affected:**
- `create.py` - Extensive usage throughout:
  - Command constants (lines 84-113): `START = chr(128)`, etc.
  - Command building (700+ lines): `self._write(chr(value))`
  - Line 478: String joining with chr
  - Line 580: `self.ser.write(byte)` expects bytes

**Fix:**
- Convert command constants to bytes: `START = bytes([128])`
- Convert chr() calls to bytes: `chr(x)` → `bytes([x])`
- Update _write() method to handle bytes properly
- Update string operations to use bytes

### 4. Type Checking (Medium Priority)
Old-style type checking using `type()` comparison.

**Files affected:**
- `create.py` - Line 512: `if type(PORT) == type('string'):`

**Fix:** Convert to `isinstance(PORT, str)`

### 5. Dependencies (High Priority)
Outdated and Python 2-specific packages in requirements.txt.

**Current:**
```
argparse==1.2.1      # Built-in to Python 3.2+
distribute==0.6.24   # Replaced by setuptools in Python 3
requests==2.20.0     # Old version with security issues
wsgiref==0.1.2      # Built-in to Python 3
```

**Fix:**
```
requests>=2.31.0
pyserial>=3.5
```

Note: argparse, wsgiref are built-in; distribute is replaced by setuptools (installed by default)

## Implementation Order

1. ✅ **Update requirements.txt** - Ensures correct dependencies
2. **Fix exception syntax** - Simple find/replace across all files
3. **Fix print statements** - Simple find/replace across all files
4. **Fix type checking** - Update isinstance usage
5. **Fix serial communication** - Most complex, requires careful testing
   - Update command constants
   - Update _write() method
   - Update all chr() calls for serial communication
   - Update string operations

## Testing Recommendations

After migration:
1. Test basic Roomba connection and communication
2. Test Alexa voice command integration
3. Test all example scripts (example-minimal.py, example-mqtt.py)
4. Verify serial communication with actual hardware
5. Test song playback functionality

## Compatibility Notes

- Target Python version: 3.7+ (for broad compatibility)
- The pyserial library v3.x supports both Python 2 and 3, providing a smooth transition
- All changes maintain backward compatibility where possible

## Breaking Changes

- Python 2 is no longer supported after this migration
- Minimum Python version: 3.7

## Resources

- [Python 3 Porting Guide](https://docs.python.org/3/howto/pyporting.html)
- [pyserial 3.x Documentation](https://pyserial.readthedocs.io/)
