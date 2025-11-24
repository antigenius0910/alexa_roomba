## Alexa Roomba

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

Voice-controlled Roomba via Amazon Echo with musical flair.

After you tell Alexa "turn on stardust destroyer," your Roomba will start singing "The Imperial March" and begin cleaning! This project combines IoT, robotics, and embedded systems programming to create a unique smart home experience.

### Demo Video

https://user-images.githubusercontent.com/5915590/138384009-169e9dc4-5142-4027-aa18-df4c367915f5.mp4

---

## Features

- 🎙️ **Voice Control**: Integrate Roomba with Alexa for hands-free cleaning
- 🎵 **Musical Robot**: Play custom MIDI songs through Roomba's speaker
- 🤖 **Serial Protocol**: Direct control via iRobot Open Interface protocol
- 📊 **Sensor Access**: Read real-time data from bumpers, cliffs, battery, and more
- 🏗️ **Modular Architecture**: Clean, maintainable code structure
- 🔧 **Hardware Integration**: Custom battery tap and embedded Raspberry Pi

## Tech Stack

- **Python 3.7+** - Modern, type-safe code
- **pyserial** - Serial communication with Roomba
- **UPnP/SSDP** - Device discovery for Alexa integration
- **Raspberry Pi Zero W** - Embedded controller
- **iRobot Open Interface** - Low-level robot control protocol

---

## Hardware Setup

**📋 [Complete Hardware Setup Guide →](HARDWARE_SETUP.md)**

This project requires hardware assembly inside your Roomba. The setup guide includes:
- ✅ Detailed component list with specifications
- ✅ **Step-by-step battery tap instructions with photos**
- ✅ Wiring diagrams and connection points
- ✅ DC-DC converter setup and voltage testing
- ✅ Raspberry Pi mounting and serial cable connection
- ✅ Troubleshooting guide

**Quick Hardware Summary:**
- iRobot Roomba (500/600/700/800 series)
- Raspberry Pi Zero W
- DC-DC Converter (14.4V → 5V)
- USB-to-Serial cable
- Amazon Echo device

---

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/antigenius0910/alexa_roomba.git
cd alexa_roomba

# Create a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

#### 1. Test Robot Connection

```python
from roomba import Create, SAFE_MODE

robot = Create('/dev/ttyUSB0', startingMode=SAFE_MODE)
robot.printSensors()  # Display all sensor data
robot.close()
```

#### 2. Simple Movement

```python
from roomba import Create
import time

robot = Create('/dev/ttyUSB0')
robot.go(20, 0)  # Move forward at 20 cm/s
time.sleep(2.0)
robot.stop()
robot.close()
```

#### 3. Play Music

```python
from roomba import Create
from roomba.music import c5, d5, e5, QUARTER

robot = Create('/dev/ttyUSB0')
melody = [(c5, QUARTER), (d5, QUARTER), (e5, QUARTER)]
robot.playSong(melody)
robot.close()
```

### Alexa Integration

```bash
# Run the Alexa integration
python example-minimal.py

# Say to your Echo:
# "Alexa, discover my devices"
# Then: "Alexa, turn on stardust destroyer"
```

---

## Project Structure

```
alexa_roomba/
├── roomba/                  # Core robot control package
│   ├── __init__.py         # Package initialization
│   ├── commands.py         # Command byte constants
│   ├── sensors.py          # Sensor definitions
│   ├── music.py            # MIDI note constants
│   ├── utils.py            # Helper functions
│   └── robot.py            # Main Create class
├── examples/               # Example scripts
│   ├── simple_movement.py  # Basic movement demo
│   ├── play_music.py       # Music playback demo
│   └── sensor_reading.py   # Sensor data demo
├── config.py               # Configuration settings
├── create.py               # Legacy compatibility layer
├── fauxmo.py               # WeMo emulation for Alexa
├── debounce_handler.py     # Multi-Echo handler
└── example-minimal.py      # Minimal Alexa example
```

---

## API Documentation

### Create Class

The main interface for robot control:

```python
from roomba import Create, SAFE_MODE

# Initialize robot
robot = Create(port='/dev/ttyUSB0', startingMode=SAFE_MODE)

# Movement
robot.go(velocity_cm_s, spin_velocity)  # Move with velocity and spin
robot.stop()                             # Stop all movement

# Sensors
robot.sensors([WALL_SIGNAL, BATTERY_CHARGE])  # Read specific sensors
robot.printSensors()                          # Print all sensor data

# Music
robot.setSong(song_number, note_list)   # Define a song
robot.playSong(note_list)               # Play a song immediately

# Modes
robot.toSafeMode()                      # Enter safe mode
robot.toFullMode()                      # Enter full mode

# Cleanup
robot.close()                           # Close serial connection
```

See [examples/](examples/) directory for complete working examples.

---

## Configuration

Edit `config.py` to customize settings:

```python
# Serial port configuration
DEFAULT_PORT = '/dev/ttyUSB0'  # Linux
# DEFAULT_PORT = '/dev/tty.usbserial'  # macOS
# DEFAULT_PORT = 'COM3'  # Windows

# Alexa device settings
FAUXMO_DEVICE_NAME = "Stardust Destroyer"
FAUXMO_PORT = 52000

# Robot physical parameters
WHEEL_SPAN_MM = 235.0
WHEEL_DIAMETER_MM = 72.0
```

---

## Systemd Service (Auto-start on Boot)

Create a systemd service for automatic startup:

```bash
sudo cp roomba.service /etc/systemd/system/
sudo systemctl enable roomba.service
sudo systemctl start roomba.service
```

Service file example:

```ini
[Unit]
Description=Roomba keepalive daemon
Wants=network-online.target
After=network.target

[Service]
Type=forking
ExecStart=/home/pi/alexa_roomba/roomba-start.sh
StandardOutput=console

[Install]
WantedBy=multi-user.target
```

---

## Lessons Learned & Technical Challenges

### 1. Battery Tap Power Solution
Safely tapping into the Roomba's 14.4V battery required careful voltage regulation. The DC-DC converter needed proper heat dissipation and capacitor placement to prevent voltage spikes during motor startup.

### 2. Serial Protocol Reverse Engineering
Implementing the iRobot Open Interface protocol required understanding two's complement arithmetic, byte packing, and timing-sensitive command sequences. See [PYTHON3_MIGRATION.md](PYTHON3_MIGRATION.md) for details on the bytes handling migration.

### 3. UPnP Device Emulation
Emulating a WeMo device for Alexa discovery involved implementing SSDP multicast listening and HTTP response handling with proper UPnP headers.

### 4. Embedded System Constraints
Running on Raspberry Pi Zero W required optimizing for limited CPU and memory, implementing efficient polling loops, and handling serial timeouts gracefully.

---

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## Credits & References

- Original concept: [Hacking the Amazon Echo (Instructables)](http://www.instructables.com/id/Hacking-the-Amazon-Echo/) by [FabricateIO](http://fabricate.io)
- **Authors**: Zach Dodds, Sean Luke, James O'Beirne, Martin Schaef
- **iRobot Open Interface**: [Official Documentation](https://www.irobot.com/about-irobot/stem/create-2)

### Key Code Sections

- Alexa integration: [fauxmo.py#L315](https://github.com/antigenius0910/alexa_roomba/blob/master/fauxmo.py#L315)
- Imperial March playback: [create.py#L1474](https://github.com/antigenius0910/alexa_roomba/blob/master/create.py#L1474)

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

You are free to use, modify, and distribute this project for any purpose, including commercial use, as long as you include the original copyright notice.
