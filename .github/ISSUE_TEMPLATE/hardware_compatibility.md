---
name: 🤖 Hardware Compatibility Report
about: Report compatibility with specific hardware configurations
title: '[Hardware] '
labels: hardware, compatibility
assignees: ''

---

## Hardware Configuration

**Roomba Model:**
- [ ] Roomba 500 series
- [ ] Roomba 600 series
- [ ] Roomba 700 series
- [ ] Roomba 800 series
- [ ] Roomba 900 series
- [ ] Create 2
- [ ] Other: [specify]

**Serial Adapter:**
- Manufacturer: [e.g., FTDI, Prolific]
- Model: [e.g., FT232RL]
- Connection Type: [e.g., USB-to-Serial, Bluetooth, Direct DIN]
- Product Link: [if available]

**Host System:**
- Device: [e.g., Raspberry Pi 4, Desktop PC, Laptop]
- OS: [e.g., Raspberry Pi OS, Ubuntu 20.04, macOS 12.0]
- Python Version: [e.g., 3.9.5]

## Compatibility Status

**Does the hardware work with this project?**
- [ ] ✅ Fully working
- [ ] ⚠️ Partially working (some features don't work)
- [ ] ❌ Not working

## Working Features

List which features work with this hardware:

- [ ] Basic movement (go, stop)
- [ ] Sensor reading
- [ ] Music playback
- [ ] Mode switching (passive, safe, full)
- [ ] Bump detection
- [ ] Cliff detection
- [ ] Wall following
- [ ] Battery monitoring
- [ ] Alexa integration
- [ ] Other: [specify]

## Issues Encountered

**Problems or Limitations:**

Describe any issues you encountered:

1. Issue description
2. Error messages (if any)
3. Workarounds (if any)

## Configuration Details

**Serial Port Settings:**
- Port: [e.g., /dev/ttyUSB0]
- Baud Rate: [e.g., 115200]
- Timeout: [e.g., 1 second]

**Special Configuration:**

```python
# If you needed special configuration
from roomba import Create

robot = Create(
    port='/dev/ttyUSB0',
    baudrate=115200,
    # other settings...
)
```

## Connection Notes

**Physical Connection:**
- How did you connect the serial adapter to the Roomba?
- Any special cables or adapters needed?
- Pin connections (if using direct DIN connection):

```
DIN Pin -> Adapter Pin
1 (RXD) -> TX
2 (TXD) -> RX
6 (GND) -> GND
7 (VCC) -> 5V (optional)
```

## Performance Notes

**Performance Observations:**
- Command latency: [e.g., < 50ms, noticeable delay]
- Sensor read frequency: [e.g., 10 Hz, slower than expected]
- Reliability: [e.g., stable for hours, occasional disconnects]

## Testing Performed

Describe what testing you did:

- [ ] Basic movement test
- [ ] Extended operation (hours)
- [ ] All sensor types
- [ ] Music playback
- [ ] Alexa voice commands
- [ ] Multiple start/stop cycles
- [ ] Other: [specify]

## Logs

**Startup Logs:**
```
Paste startup logs here
```

**Error Logs (if any):**
```
Paste error logs here
```

## Photos (Optional)

If helpful, include photos of:
- Physical setup
- Serial adapter connection
- DIN connector (if using)
- Complete system setup

## Additional Information

**Useful Details:**
- Purchase date of Roomba: [approximate]
- Firmware version (if known): [e.g., from info screen]
- Any modifications to Roomba: [e.g., battery replacement]

**Would you recommend this configuration?**
- [ ] Yes, worked great
- [ ] Yes, with caveats (explain below)
- [ ] No, too many issues

**Additional Comments:**

Add any other relevant information about this hardware configuration.

## Checklist

- [ ] I have read the [HARDWARE_SETUP.md](../HARDWARE_SETUP.md) guide
- [ ] I have provided complete hardware information
- [ ] I have included configuration details
- [ ] I have tested multiple features
- [ ] I have included relevant logs or error messages
