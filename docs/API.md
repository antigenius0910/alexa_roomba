# API Reference

Complete API documentation for the Alexa Roomba project.

## Table of Contents

- [Create Class](#create-class)
  - [Initialization](#initialization)
  - [Movement Methods](#movement-methods)
  - [Sensor Methods](#sensor-methods)
  - [Music Methods](#music-methods)
  - [Mode Methods](#mode-methods)
  - [Utility Methods](#utility-methods)
- [Constants](#constants)
  - [Commands](#commands)
  - [Sensors](#sensors)
  - [Music Notes](#music-notes)
  - [Robot Modes](#robot-modes)
- [Configuration](#configuration)
- [Utility Functions](#utility-functions)

---

## Create Class

The main interface for controlling the iRobot Create/Roomba robot.

### Initialization

#### `Create(port, startingMode=PASSIVE_MODE)`

Initialize connection to the robot.

**Parameters:**
- `port` (str): Serial port path
  - Linux: `/dev/ttyUSB0`
  - macOS: `/dev/tty.usbserial`
  - Windows: `COM3`
- `startingMode` (int, optional): Initial robot mode
  - `PASSIVE_MODE` (default): Sensors only, no movement
  - `SAFE_MODE`: Full control with cliff/wheel drop protection
  - `FULL_MODE`: Complete control, no safety features

**Returns:** `Create` instance

**Raises:**
- `serial.SerialException`: If unable to open serial port
- `Exception`: If robot doesn't respond to initialization

**Example:**
```python
from roomba import Create, SAFE_MODE

# Safe mode (recommended)
robot = Create('/dev/ttyUSB0', startingMode=SAFE_MODE)

# Passive mode (sensors only)
robot = Create('/dev/ttyUSB0')

# Full mode (no safety features)
robot = Create('/dev/ttyUSB0', startingMode=FULL_MODE)
```

**Notes:**
- Always call `close()` when done
- Use `SAFE_MODE` for autonomous behaviors
- `FULL_MODE` disables cliff sensors - use with caution!

---

### Movement Methods

#### `go(velocity, spin_velocity=0)`

Move the robot with specified velocity and spin rate.

**Parameters:**
- `velocity` (int): Forward velocity in cm/s
  - Range: -50 to 50
  - Positive: forward, Negative: backward
- `spin_velocity` (int, optional): Rotation velocity
  - Range: -100 to 100
  - Positive: clockwise, Negative: counter-clockwise

**Returns:** None

**Example:**
```python
# Move forward at 20 cm/s
robot.go(20)

# Move backward at 15 cm/s
robot.go(-15)

# Spin in place clockwise
robot.go(0, 50)

# Move forward while turning (arc)
robot.go(20, 30)
```

**Notes:**
- Velocities are approximate based on calibration
- Actual speed may vary with battery level
- Robot will continue moving until `stop()` is called

---

#### `stop()`

Stop all robot movement immediately.

**Parameters:** None

**Returns:** None

**Example:**
```python
robot.go(20, 0)
time.sleep(2.0)
robot.stop()
```

**Notes:**
- Always call before reading sensors for accurate data
- Automatically called by `close()`

---

#### `Drive(velocity_high, velocity_low, radius_high, radius_low)`

Low-level drive command using raw iRobot protocol bytes.

**Parameters:**
- `velocity_high` (int): High byte of velocity (mm/s)
- `velocity_low` (int): Low byte of velocity
- `radius_high` (int): High byte of turn radius (mm)
- `radius_low` (int): Low byte of turn radius

**Returns:** None

**Example:**
```python
# Straight forward at 200 mm/s
robot.Drive(0, 200, 128, 0)

# Use go() instead - it's much easier!
robot.go(20, 0)  # Equivalent and simpler
```

**Notes:**
- **Prefer `go()` method** - handles byte conversion automatically
- Only use for advanced control scenarios
- See iRobot OI spec for byte encoding details

---

### Sensor Methods

#### `sensors(sensor_list=[])`

Read sensor data from the robot.

**Parameters:**
- `sensor_list` (list, optional): List of sensor IDs to read
  - Empty list reads all sensors (default)
  - Specific IDs for targeted reads

**Returns:**
- `dict`: Sensor values keyed by sensor ID
- Values stored in `robot.sensord` attribute

**Example:**
```python
from roomba.sensors import BATTERY_CHARGE, WALL_SIGNAL, BUMPS_AND_WHEEL_DROPS

# Read specific sensors
robot.sensors([BATTERY_CHARGE, WALL_SIGNAL])

# Access values
battery = robot.sensord[BATTERY_CHARGE]
wall = robot.sensord[WALL_SIGNAL]

# Read all sensors
robot.sensors()
```

**Available Sensors:**
See [Sensors Constants](#sensors) section for complete list.

**Notes:**
- Stop robot before reading for accurate data
- Some sensors only available in certain modes
- Battery sensors always available

---

#### `printSensors()`

Print formatted output of all sensor values.

**Parameters:** None

**Returns:** None

**Example:**
```python
robot.printSensors()
```

**Output:**
```
Bump Left: 0
Bump Right: 0
Wall: 0
Cliff Left: 0
...
Battery Charge: 2500 mAh
Battery Capacity: 3000 mAh
```

**Notes:**
- Useful for debugging
- Automatically calls `sensors()` first

---

### Music Methods

#### `setSong(songNum, noteList)`

Define a song in robot's memory.

**Parameters:**
- `songNum` (int): Song slot number (0-15)
- `noteList` (list): List of (note, duration) tuples
  - `note` (int): MIDI note number (31-127)
  - `duration` (int): Duration in 1/64ths of a second

**Returns:** None

**Example:**
```python
from roomba.music import c5, d5, e5, QUARTER, HALF

# Define a simple melody
song = [
    (c5, QUARTER),
    (d5, QUARTER),
    (e5, HALF)
]

robot.setSong(0, song)
```

**Notes:**
- Maximum 16 notes per song
- Maximum 16 songs can be stored
- Songs persist until robot power cycled

---

#### `playSong(noteList)`

Play a song immediately (defines and plays in slot 0).

**Parameters:**
- `noteList` (list): List of (note, duration) tuples

**Returns:** None

**Example:**
```python
from roomba.music import c5, d5, e5, f5, g5, QUARTER

scale = [
    (c5, QUARTER),
    (d5, QUARTER),
    (e5, QUARTER),
    (f5, QUARTER),
    (g5, QUARTER)
]

robot.playSong(scale)
```

**Notes:**
- Convenience method combining `setSong(0, ...)` and `PlaySong(0)`
- Overwrites song slot 0
- Blocks until song finishes playing

---

#### `PlaySong(songNum)`

Play a previously defined song.

**Parameters:**
- `songNum` (int): Song slot number (0-15)

**Returns:** None

**Example:**
```python
# Define songs in different slots
robot.setSong(0, happy_melody)
robot.setSong(1, sad_melody)

# Play them later
robot.PlaySong(0)  # Play happy melody
time.sleep(3)
robot.PlaySong(1)  # Play sad melody
```

---

### Mode Methods

#### `toSafeMode()`

Switch robot to Safe Mode.

**Parameters:** None

**Returns:** None

**Example:**
```python
robot.toSafeMode()
```

**Safe Mode Features:**
- Full control of robot
- Cliff sensors active (prevents falls)
- Wheel drop sensors active (prevents getting stuck)
- **Recommended for autonomous behaviors**

---

#### `toFullMode()`

Switch robot to Full Mode.

**Parameters:** None

**Returns:** None

**Example:**
```python
robot.toFullMode()
```

**Full Mode Features:**
- Complete control of robot
- **All safety features disabled**
- Can drive off cliffs
- Can continue when lifted

**Warning:** Use with extreme caution!

---

#### `toPassiveMode()`

Switch robot to Passive Mode.

**Parameters:** None

**Returns:** None

**Example:**
```python
robot.toPassiveMode()
```

**Passive Mode Features:**
- Sensor reading only
- No movement control
- Cannot send drive commands
- Useful for monitoring without interference

---

### Utility Methods

#### `close()`

Close the serial connection and clean up.

**Parameters:** None

**Returns:** None

**Example:**
```python
try:
    robot = Create('/dev/ttyUSB0')
    robot.go(20, 0)
    time.sleep(2)
finally:
    robot.close()  # Always close!
```

**Notes:**
- **Always call when done** to prevent serial port locks
- Automatically stops robot movement
- Use in `finally` block to ensure cleanup

---

## Constants

### Commands

Command byte constants for low-level control.

```python
from roomba.commands import *

START         # Start OI communication
RESET         # Reset robot
STOP          # Stop OI communication
BAUD          # Change baud rate
SAFE          # Enter safe mode
FULL          # Enter full mode
SPOT          # Start spot cleaning
CLEAN         # Start normal cleaning
MAX           # Start max cleaning
POWER         # Power down
SENSORS       # Request sensor data
DRIVE         # Send drive command
DRIVE_DIRECT  # Direct wheel control
LED           # Control LEDs
SONG          # Define song
PLAY_SONG     # Play defined song
```

**Usage:**
```python
# Most users don't need these directly
# Use Create class methods instead

# Low-level example (not recommended):
robot.sendCommand(START)
robot.sendCommand(SAFE)
```

---

### Sensors

Sensor packet IDs for reading robot state.

```python
from roomba.sensors import *

# Bumpers and drops
BUMPS_AND_WHEEL_DROPS    # Bump and wheel drop sensors
WALL                     # Wall sensor
CLIFF_LEFT               # Left cliff sensor
CLIFF_FRONT_LEFT         # Front left cliff sensor
CLIFF_FRONT_RIGHT        # Front right cliff sensor
CLIFF_RIGHT              # Right cliff sensor

# Virtual wall
VIRTUAL_WALL             # Virtual wall detected

# Overcurrent
WHEEL_OVERCURRENTS       # Wheel motor overcurrent

# Dirt detection
DIRT_DETECT              # Dirt detect sensor

# Infrared
INFRARED_CHAR_OMNI       # Infrared character (omni)
INFRARED_CHAR_LEFT       # Infrared character (left)
INFRARED_CHAR_RIGHT      # Infrared character (right)

# Buttons
BUTTONS                  # Button states

# Distance and angle
DISTANCE                 # Distance traveled (mm)
ANGLE                    # Angle rotated (degrees)

# Charging
CHARGING_STATE           # Charging state
VOLTAGE                  # Battery voltage (mV)
CURRENT                  # Battery current (mA)
TEMPERATURE              # Battery temperature (°C)
BATTERY_CHARGE           # Battery charge (mAh)
BATTERY_CAPACITY         # Battery capacity (mAh)

# Wall signal
WALL_SIGNAL              # Wall sensor signal strength

# Cliff signals
CLIFF_LEFT_SIGNAL        # Left cliff signal
CLIFF_FRONT_LEFT_SIGNAL  # Front left cliff signal
CLIFF_FRONT_RIGHT_SIGNAL # Front right cliff signal
CLIFF_RIGHT_SIGNAL       # Right cliff signal

# Motor currents
LEFT_MOTOR_CURRENT       # Left wheel motor current
RIGHT_MOTOR_CURRENT      # Right wheel motor current

# Encoders
ENCODER_LEFT             # Left wheel encoder counts
ENCODER_RIGHT            # Right wheel encoder counts

# Light bumpers
LIGHT_BUMPER             # Light bumper sensors
LIGHT_BUMP_LEFT          # Left light bumper
LIGHT_BUMP_FRONT_LEFT    # Front left light bumper
LIGHT_BUMP_CENTER_LEFT   # Center left light bumper
LIGHT_BUMP_CENTER_RIGHT  # Center right light bumper
LIGHT_BUMP_FRONT_RIGHT   # Front right light bumper
LIGHT_BUMP_RIGHT         # Right light bumper

# Mode
OI_MODE                  # Current OI mode

# Song
SONG_NUMBER              # Currently playing song
SONG_PLAYING             # Song playing status
```

**Usage:**
```python
from roomba.sensors import BATTERY_CHARGE, WALL_SIGNAL

robot.sensors([BATTERY_CHARGE, WALL_SIGNAL])
battery = robot.sensord[BATTERY_CHARGE]
wall = robot.sensord[WALL_SIGNAL]

print(f"Battery: {battery} mAh")
print(f"Wall distance: {wall}")
```

---

### Music Notes

MIDI note constants for music playback.

**Note Format:** `{note}{octave}`

```python
from roomba.music import *

# Example notes
c4, d4, e4, f4, g4, a4, b4  # Middle C octave
c5, d5, e5, f5, g5, a5, b5  # Octave above middle C

# Note durations (in 1/64ths of a second)
MEASURE = 160    # Full measure
HALF = 80        # Half note
QUARTER = 40     # Quarter note
EIGHTH = 20      # Eighth note
SIXTEENTH = 10   # Sixteenth note
```

**Available Notes:**
- Octaves 2-6 supported
- Notes: C, C#, D, D#, E, F, F#, G, G#, A, A#, B
- Sharps indicated by trailing 's' (e.g., `cs4` for C#4)

**Usage:**
```python
from roomba.music import c5, d5, e5, QUARTER, HALF

melody = [
    (c5, QUARTER),
    (d5, QUARTER),
    (e5, HALF)
]

robot.playSong(melody)
```

---

### Robot Modes

Operation mode constants.

```python
from roomba import *

PASSIVE_MODE = 1  # Sensors only, no control
SAFE_MODE = 2     # Full control with safety features
FULL_MODE = 3     # Complete control, no safety

OFF_MODE = 0      # Robot not responding (error state)
```

**Mode Comparison:**

| Feature | Passive | Safe | Full |
|---------|---------|------|------|
| Sensor Reading | ✅ | ✅ | ✅ |
| Movement Control | ❌ | ✅ | ✅ |
| Cliff Detection | N/A | ✅ | ❌ |
| Wheel Drop Detection | N/A | ✅ | ❌ |
| Can Fall Off Table | N/A | ❌ | ✅ |

**Usage:**
```python
from roomba import Create, SAFE_MODE

# Initialize in safe mode
robot = Create('/dev/ttyUSB0', startingMode=SAFE_MODE)

# Switch modes later
robot.toFullMode()  # Disable safety
robot.toSafeMode()  # Re-enable safety
```

---

## Configuration

Configuration module for robot settings.

```python
from config import *

# Serial settings
DEFAULT_PORT          # Default serial port
DEFAULT_BAUD_RATE     # Serial baud rate (115200)
SERIAL_TIMEOUT        # Read timeout (0.5s)

# Platform-specific ports
PORT_RASPBERRYPI      # Raspberry Pi default
PORT_MACOS            # macOS default
PORT_WINDOWS          # Windows default

# Robot modes
DEFAULT_MODE          # Default operating mode

# Alexa settings
FAUXMO_DEVICE_NAME    # Device name for Alexa
FAUXMO_PORT           # UPnP port (52000)
FAUXMO_DEBUG          # Debug logging

# Logging
LOG_LEVEL             # Logging level
LOG_FORMAT            # Log message format
LOG_FILE              # Optional log file path

# Physical parameters
WHEEL_SPAN_MM         # Distance between wheels (235mm)
WHEEL_DIAMETER_MM     # Wheel diameter (72mm)
ANGULAR_ERROR_FACTOR  # Turn angle calibration

# Movement limits
MAX_VELOCITY_CM_S     # Maximum velocity (50 cm/s)
MAX_SPIN_VELOCITY     # Maximum spin rate (100)

# Timing
COMMAND_DELAY         # Delay between commands (0.3s)
STARTUP_DELAY         # Initialization delay (0.5s)
```

**Functions:**

#### `configure_logging(level, log_file=None)`

Configure application logging.

**Parameters:**
- `level`: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `log_file` (optional): Path to log file

**Example:**
```python
from config import configure_logging
import logging

configure_logging(level=logging.DEBUG, log_file='robot.log')
```

---

#### `get_platform_port()`

Auto-detect appropriate serial port for current platform.

**Returns:** `str` - Detected port path

**Example:**
```python
from config import get_platform_port

port = get_platform_port()
robot = Create(port)
```

---

#### `print_config()`

Print current configuration values.

**Example:**
```python
from config import print_config

print_config()
```

**Output:**
```
============================================================
Alexa Roomba Configuration
============================================================
Serial Port:      /dev/ttyUSB0
Baud Rate:        115200
Device Name:      Stardust Destroyer
Fauxmo Port:      52000
Operating Mode:   SAFE_MODE
Log Level:        INFO
Install Dir:      /home/pi/alexa_roomba
============================================================
```

---

## Utility Functions

Helper functions from `roomba.utils`.

#### `mode_to_string(mode)`

Convert mode number to readable string.

**Parameters:**
- `mode` (int): Mode constant

**Returns:** `str` - Mode name

**Example:**
```python
from roomba.utils import mode_to_string
from roomba import SAFE_MODE

mode_name = mode_to_string(SAFE_MODE)
print(mode_name)  # "SAFE_MODE"
```

---

#### `_bit_of_byte(byte, bit)`

Extract specific bit from byte.

**Parameters:**
- `byte` (int): Byte value
- `bit` (int): Bit position (0-7)

**Returns:** `bool` - Bit value

**Example:**
```python
from roomba.utils import _bit_of_byte

# Check if right bump is active
bumps = robot.sensord[BUMPS_AND_WHEEL_DROPS]
right_bump = _bit_of_byte(bumps, 0)
```

**Note:** Usually not needed - use sensor values directly.

---

## Error Handling

Common exceptions and how to handle them.

### `serial.SerialException`

Raised when serial port cannot be opened.

**Causes:**
- Port doesn't exist
- Port in use by another process
- Insufficient permissions

**Solution:**
```python
import serial
from roomba import Create

try:
    robot = Create('/dev/ttyUSB0')
except serial.SerialException as e:
    print(f"Cannot open port: {e}")
    print("Check port path and permissions")
```

---

### `TimeoutError`

Raised when robot doesn't respond.

**Causes:**
- Robot powered off
- Wrong baud rate
- Loose cable connection

**Solution:**
```python
try:
    robot = Create('/dev/ttyUSB0')
    robot.sensors()
except TimeoutError:
    print("Robot not responding")
    print("Check power and connections")
```

---

## Best Practices

### 1. Always Use Context Managers or Finally Blocks

```python
# Good: Using finally
try:
    robot = Create('/dev/ttyUSB0')
    robot.go(20, 0)
finally:
    robot.close()

# Better: Could create context manager wrapper
```

### 2. Stop Before Reading Sensors

```python
# Good
robot.stop()
time.sleep(0.1)  # Brief settle time
robot.sensors()

# Bad
robot.go(20, 0)
robot.sensors()  # Inaccurate while moving!
```

### 3. Use Safe Mode for Autonomous Behaviors

```python
# Good: Safe mode prevents accidents
robot = Create('/dev/ttyUSB0', startingMode=SAFE_MODE)

# Risky: Full mode disables safety
robot = Create('/dev/ttyUSB0', startingMode=FULL_MODE)
```

### 4. Handle Sensor Errors Gracefully

```python
from roomba.sensors import BATTERY_CHARGE

robot.sensors([BATTERY_CHARGE])

# Good: Use .get() with default
battery = robot.sensord.get(BATTERY_CHARGE, 0)

# Bad: Direct access can raise KeyError
battery = robot.sensord[BATTERY_CHARGE]
```

---

## Complete Example

Putting it all together:

```python
"""
Complete example demonstrating API usage.
"""

import time
import logging
from roomba import Create, SAFE_MODE
from roomba.sensors import BATTERY_CHARGE, WALL_SIGNAL, BUMPS_AND_WHEEL_DROPS
from roomba.music import c5, d5, e5, QUARTER
from config import DEFAULT_PORT, configure_logging

# Configure logging
configure_logging(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Main program."""
    robot = None

    try:
        # Initialize
        logger.info(f"Connecting to robot on {DEFAULT_PORT}")
        robot = Create(DEFAULT_PORT, startingMode=SAFE_MODE)

        # Read sensors
        robot.sensors([BATTERY_CHARGE, WALL_SIGNAL])
        battery = robot.sensord.get(BATTERY_CHARGE, 0)
        logger.info(f"Battery: {battery} mAh")

        # Play startup sound
        startup = [(c5, QUARTER), (d5, QUARTER), (e5, QUARTER)]
        robot.playSong(startup)
        time.sleep(2)

        # Move forward
        logger.info("Moving forward")
        robot.go(20, 0)
        time.sleep(2)

        # Check for obstacles
        robot.stop()
        robot.sensors([BUMPS_AND_WHEEL_DROPS])
        bumps = robot.sensord.get(BUMPS_AND_WHEEL_DROPS, 0)

        if bumps & 0x03:  # Any bump
            logger.warning("Obstacle detected!")
            robot.go(-10, 0)  # Back up
            time.sleep(1)
            robot.go(0, 50)   # Turn
            time.sleep(1)

        # Stop
        robot.stop()
        logger.info("Demo complete")

    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
    finally:
        if robot:
            robot.close()
            logger.info("Connection closed")

if __name__ == "__main__":
    main()
```

---

## See Also

- [ARCHITECTURE.md](ARCHITECTURE.md) - System design overview
- [Examples Directory](../examples/) - Working code examples
- [Hardware Setup](HARDWARE_SETUP.md) - Hardware assembly
- [Deployment Guide](DEPLOYMENT.md) - Production deployment

---

**API Version:** 2.0.0
**Last Updated:** 2024
**Python Version:** 3.7+
