# Hardware Setup Guide

## Overview
This guide details the hardware setup for controlling an iRobot Roomba 880 via Amazon Echo using a Raspberry Pi Zero W.

## Hardware Components

### Required Components

| Component | Specification | Purpose |
|-----------|--------------|---------|
| **Roomba** | iRobot Roomba 880 | Robot vacuum to be controlled |
| **Raspberry Pi** | Raspberry Pi Zero W | Main controller running Python scripts |
| **DC-DC Converter** | 5V Step-Down Converter (14.4V → 5V) | Powers Raspberry Pi from Roomba battery |
| **USB-to-Serial Cable** | FTDI or similar, 3.3V logic level | Serial communication with Roomba |
| **Power Wires** | 22-24 AWG, Red/Black pair | Connect Roomba battery to converter |
| **Amazon Echo** | Any Echo device | Voice control interface |

### Component Details

#### Roomba 880 Specifications
- **Model**: iRobot Roomba 880
- **Battery**: 14.4V Lithium-Ion (3000mAh typical)
- **Serial Port**: Mini-DIN 7-pin connector
- **Communication**: 115200 baud, 8N1

#### Raspberry Pi Zero W
- **GPIO**: 40-pin header
- **Connectivity**: Built-in WiFi (required for Alexa communication)
- **Power**: 5V @ 500mA minimum
- **USB**: Micro USB for power and peripherals

#### DC-DC Converter
- **Input**: 14.4V (Roomba battery)
- **Output**: 5V @ 1A minimum (for Pi Zero W)
- **Type**: Step-down buck converter
- **Efficiency**: >85% recommended

## Wiring Diagram

### Power Circuit
```
Roomba Battery (14.4V)
    │
    ├─── Red Wire (+) ────┐
    │                      │
    └─── Black Wire (-) ───┼─── DC-DC Converter (Input)
                           │
                    DC-DC Converter
                      (14.4V → 5V)
                           │
    ┌──────────────────────┼─── Red Wire (+5V)
    │                      │
    │                      └─── Black Wire (GND)
    │
Raspberry Pi Zero W
  (5V Power via GPIO or Micro USB)
```

### Serial Communication
```
Roomba Mini-DIN Connector ←→ USB-to-Serial Cable ←→ Raspberry Pi USB Port

Pin Configuration:
- Pin 1: Vpwr (14.4V) - Not used
- Pin 3: RXD - Connect to Serial TX
- Pin 4: TXD - Connect to Serial RX
- Pin 6: GND - Connect to Serial GND
- Pin 7: BRC (Baud Rate Change) - Optional
```

## Step-by-Step Assembly

### Step 1: Prepare the Roomba
1. **Remove the cargo bay handle** - This provides space for mounting the Pi
2. **Access the Mini-DIN serial port** - Located under the handle area
3. **Note the battery voltage** - 14.4V nominal (verify with multimeter)

### Step 2: Install DC-DC Converter
1. **Connect input wires to Roomba battery**:
   - Red wire → Battery positive terminal
   - Black wire → Battery negative terminal

2. **Set output voltage**:
   - Adjust potentiometer to exactly 5.0V (measure with multimeter)
   - ⚠️ **Warning**: Verify 5V output BEFORE connecting to Pi

3. **Secure the converter**:
   - Use double-sided tape or velcro
   - Ensure it won't interfere with Roomba's movement

### Step 3: Mount Raspberry Pi Zero W
1. **Position the Pi** in the cargo bay (see Image 2)
2. **Connect power**:
   - Option A: Solder wires to GPIO pins 2 (+5V) and 6 (GND)
   - Option B: Use micro USB power connector
3. **Secure the Pi** with mounting tape or custom bracket

### Step 4: Connect Serial Cable
1. **Plug USB-to-Serial cable** into Roomba's Mini-DIN port
2. **Connect USB end** to Raspberry Pi's USB port
3. **Verify connection**:
   ```bash
   ls /dev/ttyUSB0  # Should show the serial device
   ```

### Step 5: Configure Raspberry Pi
1. **Install Raspberry Pi OS Lite**
2. **Enable WiFi** for Alexa connectivity:
   ```bash
   sudo raspi-config
   # Network Options → Wi-Fi
   ```
3. **Install required packages**:
   ```bash
   sudo apt-get update
   sudo apt-get install python3 python3-pip python3-serial
   ```

## Pin Connections Reference

### Roomba Mini-DIN 7-Pin Layout
```
     5   6   7
   3   4
 1       2

Pin 1: Vpwr (14.4V)
Pin 2: Vpwr (14.4V)
Pin 3: RXD (Receive Data)
Pin 4: TXD (Transmit Data)
Pin 5: BRC (Baud Rate Change)
Pin 6: GND
Pin 7: GND
```

### Raspberry Pi GPIO (Power Only)
```
Pin 2: 5V Power (DC-DC Converter +)
Pin 6: Ground (DC-DC Converter -)
```

## Serial Port Configuration

### Linux Setup
```bash
# Check if serial device is detected
ls -l /dev/ttyUSB*

# Set permissions (if needed)
sudo usermod -a -G dialout pi

# Test serial communication
sudo minicom -D /dev/ttyUSB0 -b 115200
```

### Python Serial Configuration
```python
import serial

# Open serial connection to Roomba
ROOMBA_PORT = '/dev/ttyUSB0'
robot = serial.Serial(
    port=ROOMBA_PORT,
    baudrate=115200,
    bytesize=8,
    parity='N',
    stopbits=1,
    timeout=1
)
```

## Power Considerations

### Current Draw Estimates
- **Raspberry Pi Zero W**: 150-200mA (idle), 350mA (peak WiFi)
- **USB-Serial Cable**: 20-50mA
- **Total system**: ~400mA @ 5V = 2W

### Battery Runtime
- **Roomba 880 battery**: 3000mAh @ 14.4V = 43.2Wh
- **Pi power consumption**: ~2W
- **Estimated Pi runtime**: 20+ hours (battery permitting)

### Safety Notes
- ⚠️ **Always verify 5V output** before connecting to Pi
- ⚠️ **Use proper wire gauge** (22-24 AWG minimum)
- ⚠️ **Secure all connections** to prevent shorts during movement
- ⚠️ **Monitor temperature** of DC-DC converter during testing

## Testing & Validation

### 1. Power Test
```bash
# On Raspberry Pi
vcgencmd measure_volts
# Should show: volt=5.0V (±0.1V)
```

### 2. Serial Communication Test
```python
# Test script
import serial
import time

ser = serial.Serial('/dev/ttyUSB0', 115200)
ser.write(bytes([128]))  # Start command
time.sleep(0.1)
ser.write(bytes([131]))  # Safe mode
print("Roomba initialized!")
ser.close()
```

### 3. Network Test
```bash
# Verify WiFi connection
ping -c 4 8.8.8.8

# Check for Alexa discovery
python example-minimal.py
# Echo should discover "Stardust Destroyer"
```

## Troubleshooting

### Raspberry Pi Won't Boot
- **Check power voltage**: Must be 5.0V ±0.25V
- **Check current capacity**: DC-DC converter must supply >500mA
- **Check wiring**: Verify polarity (red=+, black=-)

### Serial Connection Failed
- **Check permissions**: `sudo usermod -a -G dialout pi`
- **Verify device**: `ls /dev/ttyUSB*`
- **Check cable**: Test with another USB device
- **Inspect Mini-DIN connector**: Ensure firm connection

### Roomba Not Responding
- **Baud rate**: Verify 115200 (default for Roomba 800 series)
- **Wake Roomba**: Press CLEAN button before sending commands
- **Check battery**: Roomba must have adequate charge
- **Test serial manually**: Use `minicom` to send raw commands

### Alexa Can't Discover Device
- **Network connectivity**: Pi must be on same WiFi as Echo
- **Script running**: Ensure `example-minimal.py` is active
- **Port conflict**: Check if port 52000 is available
- **Firewall**: Disable if testing, or allow UPnP

## Images Reference

See the following images for visual guidance:

- **IMG_9324.jpg**: Overall hardware layout and connections
- **IMG_9325.jpg**: Raspberry Pi Zero W mounting position
- **IMG_9326.jpg**: DC-DC converter installation
- **IMG_9327.jpg**: Roomba 880 model identification

## Safety & Compliance

⚠️ **Important Safety Information**:
- This modification connects to the Roomba's battery
- Improper wiring can damage components or create fire hazard
- Always disconnect battery when working on electronics
- Use insulated tools and proper wire management
- Test all connections with multimeter before powering on

## Next Steps

After completing hardware setup:
1. Follow the software installation guide in README.md
2. Configure the systemd service (roomba-start.sh)
3. Set up Alexa device discovery
4. Test voice commands: "Alexa, turn on Stardust Destroyer"

## Additional Resources

- [iRobot Create 2 OI Spec](https://www.irobotweb.com/~/media/MainSite/PDFs/About/STEM/Create/iRobot_Roomba_600_Open_Interface_Spec.pdf) - Serial protocol documentation
- [Raspberry Pi GPIO Pinout](https://pinout.xyz/) - Complete GPIO reference
- [Fauxmo Documentation](https://github.com/n8henrie/fauxmo) - Emulate WeMo devices for Alexa

---

**Last Updated**: 2024
**Hardware Tested**: Roomba 880 + Raspberry Pi Zero W
**Compatibility**: Should work with Roomba 500/600/700/800 series
