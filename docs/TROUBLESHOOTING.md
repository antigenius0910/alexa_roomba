# Troubleshooting Guide

Comprehensive troubleshooting guide for common issues with the Alexa Roomba project.

## Table of Contents

- [Quick Diagnostics](#quick-diagnostics)
- [Connection Issues](#connection-issues)
- [Alexa Integration Issues](#alexa-integration-issues)
- [Robot Behavior Issues](#robot-behavior-issues)
- [Hardware Issues](#hardware-issues)
- [Software Issues](#software-issues)
- [Performance Issues](#performance-issues)
- [Debugging Tools](#debugging-tools)
- [Getting Help](#getting-help)

---

## Quick Diagnostics

### System Health Check

Run these commands to check system status:

```bash
# 1. Check if service is running
systemctl status roomba

# 2. Check recent logs
tail -50 logs/roomba_$(date +%Y%m%d).log

# 3. Check serial port
ls -l /dev/ttyUSB*

# 4. Test Python imports
python3 -c "import serial, roomba; print('OK')"

# 5. Check network connectivity
ping -c 3 8.8.8.8
```

### Quick Tests

```python
# Test 1: Basic connection
from roomba import Create
robot = Create('/dev/ttyUSB0')
robot.printSensors()
robot.close()

# Test 2: Movement
from roomba import Create, SAFE_MODE
import time
robot = Create('/dev/ttyUSB0', startingMode=SAFE_MODE)
robot.go(10, 0)
time.sleep(1)
robot.stop()
robot.close()
```

---

## Connection Issues

### Serial Port Not Found

**Symptom:**
```
FileNotFoundError: [Errno 2] No such file or directory: '/dev/ttyUSB0'
```

**Diagnosis:**
```bash
# List all serial devices
ls -l /dev/tty* | grep -E '(USB|ACM|AMA)'

# Check dmesg for USB events
dmesg | grep -i usb | tail -20
```

**Solutions:**

1. **Wrong port name**
   ```bash
   # Find actual port
   python3 -c "import serial.tools.list_ports; print([p.device for p in serial.tools.list_ports.comports()])"

   # Update config
   nano .env
   # Set: ROOMBA_PORT=/dev/ttyUSB0  (or your actual port)
   ```

2. **USB cable not connected**
   - Check physical connection
   - Try different USB port
   - Check cable integrity

3. **USB-to-Serial driver not loaded**
   ```bash
   # Check loaded drivers
   lsmod | grep -E '(ftdi|pl2303|ch341)'

   # Load driver if needed (example for FTDI)
   sudo modprobe ftdi_sio
   ```

---

### Permission Denied

**Symptom:**
```
PermissionError: [Errno 13] Permission denied: '/dev/ttyUSB0'
```

**Diagnosis:**
```bash
# Check port permissions
ls -l /dev/ttyUSB0

# Check your groups
groups $USER
```

**Solutions:**

1. **Add user to dialout group**
   ```bash
   sudo usermod -a -G dialout $USER

   # Log out and back in (or reboot)
   # Verify:
   groups $USER | grep dialout
   ```

2. **Temporary fix (for testing)**
   ```bash
   sudo chmod 666 /dev/ttyUSB0
   # Note: This resets on reboot
   ```

3. **Permanent udev rule**
   ```bash
   # Create rule file
   sudo nano /etc/udev/rules.d/99-roomba.rules

   # Add this line:
   SUBSYSTEM=="tty", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6001", MODE="0666"

   # Reload rules
   sudo udevadm control --reload-rules
   sudo udevadm trigger
   ```

---

### Connection Timeout

**Symptom:**
```
TimeoutError: Robot not responding
```

**Diagnosis:**
```bash
# Test serial connection directly
python3 << EOF
import serial
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
ser.write(bytes([128]))  # START command
response = ser.read(1)
print(f"Response: {response}")
ser.close()
EOF
```

**Solutions:**

1. **Robot not powered on**
   - Press Clean button
   - Check battery level
   - Listen for startup beep

2. **Wrong baud rate**
   ```python
   # Try different baud rates
   for baud in [115200, 57600, 19200]:
       try:
           robot = Create('/dev/ttyUSB0', baudrate=baud)
           print(f"Success at {baud}")
           break
       except:
           print(f"Failed at {baud}")
   ```

3. **Cable wiring issue**
   - Verify TX/RX not swapped
   - Check GND connection
   - Test with multimeter

4. **Robot in wrong mode**
   ```python
   # Reset robot
   robot = Create('/dev/ttyUSB0')
   robot.sendCommand(RESET)
   time.sleep(2)
   robot.sendCommand(START)
   ```

---

## Alexa Integration Issues

### Alexa Can't Discover Device

**Symptom:**
Alexa says "I couldn't find any devices"

**Diagnosis:**
```bash
# 1. Check if Fauxmo is running
ps aux | grep fauxmo

# 2. Check if port is listening
netstat -ln | grep 52000

# 3. Check network connectivity
ping $(echo $ALEXA_IP)  # Your Echo's IP

# 4. Test SSDP manually
python3 << EOF
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', 1900))
print("Listening for SSDP...")
data, addr = sock.recvfrom(1024)
print(f"Received from {addr}: {data}")
EOF
```

**Solutions:**

1. **Device and Echo on different networks**
   ```bash
   # Check your IP
   ip addr show wlan0 | grep inet

   # Check Echo IP (from Alexa app)
   # They must be on same subnet (e.g., 192.168.1.x)
   ```

2. **Firewall blocking UPnP/SSDP**
   ```bash
   # Temporarily disable firewall (testing only!)
   sudo ufw disable

   # If this fixes it, add rules:
   sudo ufw allow 1900/udp
   sudo ufw allow 52000/tcp
   sudo ufw enable
   ```

3. **Service not running**
   ```bash
   # Start service
   systemctl start roomba

   # Check status
   systemctl status roomba

   # View logs
   journalctl -u roomba -f
   ```

4. **Wrong device name**
   ```bash
   # Check config
   python3 -c "from config import FAUXMO_DEVICE_NAME; print(FAUXMO_DEVICE_NAME)"

   # Say exact name to Alexa
   "Alexa, discover devices"
   "Alexa, turn on [exact device name]"
   ```

5. **Multiple devices with same name**
   ```bash
   # Alexa app → Devices → Forget all devices
   # Then rediscover
   ```

---

### Alexa Discovery Succeeds But Commands Fail

**Symptom:**
Alexa discovers device but says "Device is not responding"

**Diagnosis:**
```bash
# Check service logs
tail -f logs/roomba_*.log

# Test HTTP endpoint manually
curl -X POST http://localhost:52000/upnp/control/basicevent1 \
  -H "Content-Type: text/xml" \
  -d '<s:Envelope><s:Body><u:SetBinaryState><BinaryState>1</BinaryState></u:SetBinaryState></s:Body></s:Envelope>'
```

**Solutions:**

1. **Serial port issue**
   - See [Connection Issues](#connection-issues) section
   - Verify robot responds to commands

2. **Exception in callback**
   ```bash
   # Enable debug logging
   nano .env
   # Set: LOG_LEVEL=DEBUG

   # Restart and check logs
   systemctl restart roomba
   journalctl -u roomba -f
   ```

3. **Robot in wrong mode**
   ```python
   # Ensure robot starts in correct mode
   robot = Create(port, startingMode=SAFE_MODE)
   ```

---

## Robot Behavior Issues

### Robot Doesn't Move

**Symptom:**
Commands sent but robot doesn't respond

**Diagnosis:**
```python
# Check if robot accepts commands
from roomba import Create, SAFE_MODE
robot = Create('/dev/ttyUSB0', startingMode=SAFE_MODE)

# Check mode
robot.sensors([OI_MODE])
mode = robot.sensord.get(OI_MODE)
print(f"Mode: {mode}")  # Should be 2 (SAFE) or 3 (FULL)

# Try movement
robot.go(10, 0)
time.sleep(2)
robot.stop()
```

**Solutions:**

1. **Robot in Passive Mode**
   ```python
   # Switch to Safe Mode
   robot.toSafeMode()
   time.sleep(0.5)
   robot.go(10, 0)
   ```

2. **Wheels lifted (wheel drop sensors)**
   ```python
   # Check wheel drop sensors
   robot.sensors([BUMPS_AND_WHEEL_DROPS])
   drops = robot.sensord[BUMPS_AND_WHEEL_DROPS]

   if drops & 0x0C:  # Wheel drop bits
       print("Wheel is lifted!")
       # Put robot on ground
   ```

3. **Battery too low**
   ```python
   # Check battery
   robot.sensors([BATTERY_CHARGE, BATTERY_CAPACITY])
   charge = robot.sensord[BATTERY_CHARGE]
   capacity = robot.sensord[BATTERY_CAPACITY]
   pct = (charge / capacity * 100)
   print(f"Battery: {pct:.1f}%")

   if pct < 10:
       print("Battery too low, charge robot")
   ```

4. **Safe mode cliff sensor triggering**
   ```python
   # Check cliff sensors
   robot.sensors([CLIFF_LEFT, CLIFF_FRONT_LEFT, CLIFF_FRONT_RIGHT, CLIFF_RIGHT])

   if any([robot.sensord[s] for s in [CLIFF_LEFT, CLIFF_FRONT_LEFT, CLIFF_FRONT_RIGHT, CLIFF_RIGHT]]):
       print("Cliff detected! Move robot away from edge")
       # Or use Full Mode (dangerous!)
       robot.toFullMode()
   ```

---

### Erratic Movement

**Symptom:**
Robot moves unpredictably or in wrong direction

**Diagnosis:**
```python
# Test basic commands
robot.go(20, 0)   # Should go straight forward
time.sleep(2)
robot.stop()

robot.go(-20, 0)  # Should go straight backward
time.sleep(2)
robot.stop()

robot.go(0, 50)   # Should spin clockwise
time.sleep(2)
robot.stop()
```

**Solutions:**

1. **Calibration needed**
   ```python
   # Adjust calibration in config.py
   WHEEL_SPAN_MM = 235.0  # Measure your robot
   WHEEL_DIAMETER_MM = 72.0
   ANGULAR_ERROR_FACTOR = 360.0 / 450.0  # Adjust based on testing
   ```

2. **Velocity too high**
   ```python
   # Reduce speed
   robot.go(10, 0)  # Slower, more controlled
   ```

3. **Sensor interference**
   - Check for obstacles
   - Clean sensors
   - Verify sensor readings

---

### Music Not Playing

**Symptom:**
`playSong()` called but no sound

**Diagnosis:**
```python
# Test simple beep
from roomba.music import c5, QUARTER
robot.playSong([(c5, QUARTER)])
time.sleep(2)
```

**Solutions:**

1. **Volume too low**
   - No volume control in OI protocol
   - Sound output fixed by hardware
   - Move closer to hear

2. **Invalid note values**
   ```python
   # Ensure valid MIDI notes (31-127)
   from roomba.music import *

   # Good
   song = [(c5, QUARTER), (d5, QUARTER)]

   # Bad
   song = [(200, QUARTER)]  # Invalid MIDI note!
   ```

3. **Song too long**
   ```python
   # Maximum 16 notes per song
   song = [(c5, QUARTER)] * 16  # OK
   song = [(c5, QUARTER)] * 20  # TOO LONG!
   ```

4. **Robot busy**
   ```python
   # Stop movement before playing
   robot.stop()
   time.sleep(0.2)
   robot.playSong(melody)
   ```

---

## Hardware Issues

### Power Issues

**Symptom:**
Raspberry Pi or robot loses power unexpectedly

**Diagnosis:**
```bash
# Check voltage
vcgencmd measure_volts
vcgencmd get_throttled

# Check power supply current
# Should be at least 2A for Pi Zero W
```

**Solutions:**

1. **Insufficient current from DC-DC converter**
   - Verify converter rated for 3A+
   - Check for overheating
   - Add heat sink if needed

2. **Battery tap connection loose**
   - Check solder joints
   - Verify crimp connections
   - Measure voltage at converter input (should be ~14.4V)

3. **Robot battery depleted**
   - Charge robot
   - Check battery health
   - Replace if old/damaged

4. **Voltage drop under load**
   - Add capacitors near converter output
   - Use shorter/thicker wires
   - Upgrade to better converter

---

### Serial Communication Errors

**Symptom:**
Intermittent communication failures or corrupted data

**Diagnosis:**
```python
# Test continuous communication
for i in range(100):
    try:
        robot.sensors([BATTERY_CHARGE])
        battery = robot.sensord.get(BATTERY_CHARGE, -1)
        if battery < 0:
            print(f"Failed at iteration {i}")
        if i % 10 == 0:
            print(f"Success: {i}/100")
    except Exception as e:
        print(f"Error at {i}: {e}")
```

**Solutions:**

1. **Loose connections**
   - Check all connections
   - Resolder if needed
   - Use strain relief

2. **Electrical noise**
   - Add ferrite beads to USB cable
   - Keep cable away from motors
   - Add pull-up resistors on TX/RX

3. **Ground loop**
   - Ensure single ground point
   - Check for voltage on GND line
   - Use isolated converter if needed

4. **Cable too long**
   - Keep USB cable < 2 meters
   - Use shielded cable
   - Add signal repeater if needed

---

## Software Issues

### Import Errors

**Symptom:**
```
ModuleNotFoundError: No module named 'roomba'
ImportError: No module named 'serial'
```

**Solutions:**

```bash
# 1. Check Python version
python3 --version  # Should be 3.7+

# 2. Check if virtual environment is activated
which python3
# Should be: /home/pi/alexa_roomba/venv/bin/python3

# 3. Activate venv if needed
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Verify installations
pip list | grep -E '(serial|roomba)'

# 6. Add project to Python path (if not using venv)
export PYTHONPATH=/home/pi/alexa_roomba:$PYTHONPATH
```

---

### Service Won't Start

**Symptom:**
```
systemctl start roomba
Job for roomba.service failed
```

**Diagnosis:**
```bash
# Check service status
systemctl status roomba -l

# Check service logs
journalctl -u roomba -n 50

# Test script manually
cd /home/pi/alexa_roomba
./roomba-start.sh
```

**Solutions:**

1. **Path issues in service file**
   ```bash
   # Edit service file
   sudo nano /etc/systemd/system/roomba.service

   # Ensure absolute paths:
   ExecStart=/home/pi/alexa_roomba/roomba-start.sh
   WorkingDirectory=/home/pi/alexa_roomba

   # Reload systemd
   sudo systemctl daemon-reload
   ```

2. **Script not executable**
   ```bash
   chmod +x roomba-start.sh
   chmod +x install.sh
   ```

3. **Missing .env file**
   ```bash
   # Create from template
   cp .env.example .env
   nano .env  # Configure
   ```

4. **Python errors on startup**
   ```bash
   # Run script with full output
   bash -x ./roomba-start.sh
   ```

---

### Configuration Not Loading

**Symptom:**
Changes to `.env` not taking effect

**Solutions:**

```bash
# 1. Verify .env file location
ls -la .env

# 2. Check file format (no spaces around =)
cat .env
# Good: ROOMBA_PORT=/dev/ttyUSB0
# Bad:  ROOMBA_PORT = /dev/ttyUSB0

# 3. Restart service
systemctl restart roomba

# 4. Test config loading
python3 -c "from config import print_config; print_config()"

# 5. Check for syntax errors
python3 << EOF
from dotenv import load_dotenv
load_dotenv('.env')
import os
print(os.getenv('ROOMBA_PORT'))
EOF
```

---

## Performance Issues

### High CPU Usage

**Symptom:**
Python process using excessive CPU

**Diagnosis:**
```bash
# Monitor CPU
top -p $(pgrep -f example-minimal)

# Profile code
python3 -m cProfile example-minimal.py
```

**Solutions:**

1. **Sensor polling too frequent**
   ```python
   # Bad: Polling in tight loop
   while True:
       robot.sensors()  # No delay!

   # Good: Reasonable polling rate
   while True:
       robot.sensors()
       time.sleep(0.1)  # 10 Hz
   ```

2. **Excessive logging**
   ```bash
   # Reduce log level
   nano .env
   # Set: LOG_LEVEL=WARNING
   ```

3. **Network traffic**
   - Check for excessive SSDP traffic
   - Monitor with: `tcpdump -i wlan0 port 1900`

---

### Memory Leaks

**Symptom:**
Memory usage grows over time

**Diagnosis:**
```bash
# Monitor memory
watch -n 5 'ps aux | grep python3 | grep -v grep'

# Check for leaks
python3 -m memory_profiler example-minimal.py
```

**Solutions:**

1. **Sensor dictionary growing**
   ```python
   # Ensure dictionary cleared
   robot.sensord.clear()
   ```

2. **Log files too large**
   ```bash
   # Add log rotation
   sudo nano /etc/logrotate.d/roomba

   # Add:
   /home/pi/alexa_roomba/logs/*.log {
       daily
       rotate 7
       compress
       delaycompress
       missingok
       notifempty
   }
   ```

---

## Debugging Tools

### Enable Debug Logging

```bash
# Set debug level in .env
echo "LOG_LEVEL=DEBUG" >> .env

# Restart service
systemctl restart roomba

# Tail logs
tail -f logs/roomba_$(date +%Y%m%d).log
```

### Serial Port Debugging

```bash
# Monitor serial traffic
sudo cat /dev/ttyUSB0 | hexdump -C

# Use screen for interactive testing
screen /dev/ttyUSB0 115200
# Type: 128 (START command, as ASCII or hex)
```

### Network Debugging

```bash
# Monitor SSDP traffic
sudo tcpdump -i wlan0 -n port 1900 -vv

# Monitor HTTP traffic
sudo tcpdump -i wlan0 -n port 52000 -vv -A

# Check open ports
netstat -tuln | grep -E '(1900|52000)'
```

### Python Debugging

```python
# Add to code for breakpoint
import pdb; pdb.set_trace()

# Or use logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Print serial data
def debug_write(data):
    print(f"TX: {data.hex()}")
    ser.write(data)

def debug_read(n):
    data = ser.read(n)
    print(f"RX: {data.hex()}")
    return data
```

---

## Getting Help

### Before Asking for Help

Collect this information:

1. **System Info**
   ```bash
   uname -a
   python3 --version
   pip list | grep -E '(serial|requests)'
   ```

2. **Error Messages**
   ```bash
   # Full error output
   systemctl status roomba -l
   tail -100 logs/roomba_*.log
   ```

3. **Configuration**
   ```bash
   # Sanitized config (remove passwords!)
   cat .env | grep -v PASSWORD
   python3 -c "from config import print_config; print_config()"
   ```

4. **Test Results**
   - Output from Quick Tests section
   - Serial port test results
   - Network connectivity tests

### Where to Get Help

1. **GitHub Issues**
   - https://github.com/antigenius0910/alexa_roomba/issues
   - Search existing issues first
   - Provide system info and error logs

2. **Documentation**
   - [API Reference](API.md)
   - [Architecture](ARCHITECTURE.md)
   - [Hardware Setup](HARDWARE_SETUP.md)

3. **Community Resources**
   - iRobot Create forums
   - Raspberry Pi forums
   - Python Serial communication guides

---

## Common Error Messages Reference

| Error | Likely Cause | Solution |
|-------|-------------|----------|
| `Permission denied: '/dev/ttyUSB0'` | Not in dialout group | Add user to dialout group |
| `No such file or directory: '/dev/ttyUSB0'` | Wrong port or not connected | Check port with `ls /dev/tty*` |
| `Robot not responding` | Power/connection issue | Check power, cables, robot on |
| `Module not found` | Missing dependencies | `pip install -r requirements.txt` |
| `Address already in use` | Port conflict | Kill existing process |
| `Timeout reading from serial` | Communication issue | Check baud rate, cables |
| `Device is not responding` (Alexa) | Serial port or callback error | Check logs, test serial |
| `Invalid argument` | Wrong parameter type | Check API docs for correct types |
| `Wheel drop` | Robot lifted | Place on flat surface |
| `No module named roomba` | Path issue | Activate venv or set PYTHONPATH |

---

**Last Updated:** 2024
**For More Help:** See [Getting Help](#getting-help) section
