# Legacy Code

This directory contains legacy code that is no longer actively maintained but preserved for historical reference and backwards compatibility.

## Files in This Directory

### `example-mqtt.py`
**Status:** Deprecated
**Alternative:** Use `examples/alexa_voice_control.py` for IoT integration

MQTT-based example for integrating with MQTT brokers. This was an alternative integration method before the Alexa voice control became the primary interface.

**Why Deprecated:**
- Less user-friendly than voice control
- Requires additional MQTT broker setup
- Not actively maintained

---

### `CHIP_name_port_gpio.py`
**Status:** Hardware-specific legacy code
**Platform:** Next Thing Co. C.H.I.P. (discontinued)

GPIO mapping and configuration for the C.H.I.P. single-board computer. This was used when C.H.I.P. was a viable Raspberry Pi alternative.

**Why Deprecated:**
- C.H.I.P. hardware is no longer manufactured
- Raspberry Pi is now the recommended platform
- No active development or testing

---

### `RPi_name_port_gpio.py`
**Status:** Hardware-specific legacy code
**Platform:** Raspberry Pi

GPIO pin mapping utilities for Raspberry Pi. Contains helpers for GPIO configuration that were used in earlier versions.

**Why Deprecated:**
- GPIO control is now handled via serial interface
- Direct GPIO manipulation not needed for current architecture
- Functionality replaced by modular `roomba/` package

---

### `debounce_handler.py`
**Status:** Deprecated utility
**Alternative:** Built-in handling in modern code

Debounce handler for managing multiple Amazon Echo devices sending simultaneous commands.

**Why Deprecated:**
- Edge case that rarely occurred in practice
- Modern Alexa infrastructure handles this better
- Added unnecessary complexity to codebase

---

## Should You Use These Files?

**Short answer:** Probably not.

These files are kept for:
1. **Historical Reference** - Understanding project evolution
2. **Hardware Compatibility** - Supporting discontinued platforms
3. **Alternative Approaches** - Learning different integration methods

## Modern Alternatives

| Legacy File | Modern Alternative | Reason to Switch |
|-------------|-------------------|------------------|
| `example-mqtt.py` | `examples/alexa_voice_control.py` | Better UX, voice control |
| `CHIP_name_port_gpio.py` | Use Raspberry Pi | Hardware availability |
| `RPi_name_port_gpio.py` | `roomba/` package | Better architecture |
| `debounce_handler.py` | Built-in Alexa handling | Unnecessary complexity |

## Need Help?

If you need to use any of these legacy files:

1. Check if a modern alternative exists first
2. Review the main [README.md](../README.md) for current approach
3. See [examples/](../examples/) for up-to-date code
4. Open an issue if you have questions

---

**Note:** These files are provided as-is with no guarantee of functionality. They may not work with current dependencies or hardware configurations.
