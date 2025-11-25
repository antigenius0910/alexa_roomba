<div align="center">

# 🤖 Alexa Roomba

### *"Alexa, turn on Stardust Destroyer!"*

**Voice-controlled iRobot Roomba with Amazon Echo integration and musical capabilities**

Transform your Roomba into a voice-controlled, music-playing smart home robot

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Code Coverage](https://img.shields.io/badge/coverage-85%25-brightgreen.svg)](docs/TESTING.md)
[![Documentation](https://img.shields.io/badge/docs-comprehensive-blue.svg)](docs/)
[![Code of Conduct](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](CODE_OF_CONDUCT.md)
[![Maintenance](https://img.shields.io/badge/maintained-yes-green.svg)](https://github.com/antigenius0910/alexa_roomba/graphs/commit-activity)
[![GitHub Stars](https://img.shields.io/github/stars/antigenius0910/alexa_roomba?style=social)](https://github.com/antigenius0910/alexa_roomba/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/antigenius0910/alexa_roomba?style=social)](https://github.com/antigenius0910/alexa_roomba/network/members)

[Features](#-features) •
[Demo](#-demo) •
[Quick Start](#-quick-start) •
[Documentation](#-documentation) •
[Hardware](#-hardware-requirements) •
[Contributing](#-contributing)

</div>

---

## 📺 Demo

Watch your Roomba come to life! Say *"Alexa, turn on Stardust Destroyer"* and watch it play the Imperial March while starting its cleaning mission.

<div align="center">

https://github.com/user-attachments/assets/3c856eaf-ff82-4fb7-a711-889bf7d9a181

*Roomba playing Imperial March and starting cleaning routine via Alexa voice command*

</div>



---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🎙️ Voice Control
- **Alexa Integration**: Control your Roomba with voice commands
- **Custom Device Names**: Personalize your robot's identity
- **Hands-Free Operation**: Start, stop, and control without touching
- **UPnP Discovery**: Automatic device discovery by Alexa

</td>
<td width="50%">

### 🎵 Musical Capabilities
- **MIDI Playback**: Play custom songs through Roomba's speaker
- **Pre-programmed Songs**: Imperial March and more
- **Note Library**: Complete MIDI note definitions (C2-C6)
- **Custom Compositions**: Create your own melodies

</td>
</tr>
<tr>
<td width="50%">

### 🤖 Robot Control
- **Precise Movement**: Control velocity and rotation independently
- **Multiple Modes**: Passive, Safe, and Full control modes
- **Serial Protocol**: Direct Open Interface commands
- **Real-time Control**: Low-latency command execution

</td>
<td width="50%">

### 📊 Sensor Access
- **Comprehensive Sensors**: Bumpers, cliffs, walls, battery, encoders
- **Real-time Monitoring**: Continuous sensor data streaming
- **Safety Features**: Automatic cliff and drop detection
- **Battery Management**: Monitor charge level and capacity

</td>
</tr>
<tr>
<td width="50%">

### 🏗️ Software Architecture
- **Modular Design**: Clean, maintainable code structure
- **Python 3.7+**: Modern type-safe implementation
- **Comprehensive Tests**: 280+ tests with 85% coverage
- **Well Documented**: Extensive API and architecture docs

</td>
<td width="50%">

### 🔧 Hardware Integration
- **Raspberry Pi Embedded**: Runs on Pi Zero W
- **Custom Power Solution**: Battery tap with DC-DC converter
- **Serial Communication**: USB-to-Serial adapter support
- **Cross-Platform**: Works on Linux, macOS, Windows

</td>
</tr>
</table>

---

## 🔧 Hardware Requirements

### Essential Components

| Item | Specification | Purpose | Approx. Cost |
|------|--------------|---------|--------------|
| **iRobot Roomba** | 500/600/700/800 series or Create 2 | Robot platform | $50-300 (used) |
| **Raspberry Pi** | Pi Zero W / 3 / 4 | Embedded controller | $5-35 |
| **DC-DC Converter** | 14.4V → 5V, 3A+ | Power for Pi | $5-10 |
| **USB-Serial Cable** | FTDI or compatible | Serial communication | $5-15 |
| **MicroSD Card** | 8GB+ Class 10 | OS storage | $5-10 |
| **Amazon Echo** | Any Echo device | Voice control (optional) | $20-50 |

### Detailed Hardware Guide

📋 **[Complete Hardware Setup Guide →](docs/HARDWARE_SETUP.md)**

Our comprehensive guide includes:
- ✅ Complete parts list with links
- ✅ Battery tap installation with photos
- ✅ Wiring diagrams and schematics
- ✅ DC-DC converter configuration
- ✅ Raspberry Pi mounting instructions
- ✅ Troubleshooting and safety tips

---

## 🚀 Quick Start

### Prerequisites

Before you begin, ensure you have:

- **Hardware**: iRobot Roomba (500/600/700/800 series or Create 2)
- **Computer/Pi**: Raspberry Pi, Linux, macOS, or Windows
- **Python**: Python 3.7 or higher
- **Cable**: USB-to-Serial adapter (for non-Raspberry Pi setups)
- **Optional**: Amazon Echo device for voice control

### Installation

<details>
<summary><b>🐧 Linux / Raspberry Pi</b></summary>

```bash
# Clone the repository
git clone https://github.com/antigenius0910/alexa_roomba.git
cd alexa_roomba

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Find your serial port
ls /dev/tty*  # Usually /dev/ttyUSB0 or /dev/ttyAMA0
```

</details>

<details>
<summary><b>🍎 macOS</b></summary>

```bash
# Clone the repository
git clone https://github.com/antigenius0910/alexa_roomba.git
cd alexa_roomba

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Find your serial port
ls /dev/tty.*  # Usually /dev/tty.usbserial-*
```

</details>

<details>
<summary><b>🪟 Windows</b></summary>

```batch
REM Clone the repository
git clone https://github.com/antigenius0910/alexa_roomba.git
cd alexa_roomba

REM Create virtual environment
python -m venv venv
venv\Scripts\activate

REM Install dependencies
pip install -r requirements.txt

REM Find your serial port (Device Manager → Ports)
REM Usually COM3, COM4, etc.
```

</details>

### Basic Usage

#### 1️⃣ Test Connection

```python
from roomba import Create, SAFE_MODE

# Connect to your Roomba
robot = Create('/dev/ttyUSB0', startingMode=SAFE_MODE)

# Read and display all sensor data
robot.printSensors()

# Clean up
robot.close()
```

#### 2️⃣ Simple Movement

```python
from roomba import Create
import time

robot = Create('/dev/ttyUSB0')

# Move forward at 20 cm/s for 2 seconds
robot.go(20, 0)
time.sleep(2.0)

# Stop
robot.stop()
robot.close()
```

#### 3️⃣ Play a Song

```python
from roomba import Create
from roomba.music import c5, d5, e5, f5, g5, QUARTER, HALF

robot = Create('/dev/ttyUSB0')

# Play a simple melody
melody = [
    (c5, QUARTER),
    (d5, QUARTER),
    (e5, QUARTER),
    (f5, QUARTER),
    (g5, HALF)
]

robot.playSong(melody)
robot.close()
```

### Alexa Integration

```bash
# Run the Alexa integration script
python example-minimal.py

# In your Alexa app or say:
"Alexa, discover my devices"

# After discovery completes, say:
"Alexa, turn on Stardust Destroyer"

# Watch your Roomba play the Imperial March and start cleaning! 🎵🤖
```

---

## 📦 System Requirements

| Component | Requirement | Notes |
|-----------|------------|-------|
| **Python** | 3.7+ | Python 3.9+ recommended |
| **OS** | Linux, macOS, Windows | Raspberry Pi OS preferred for embedded |
| **RAM** | 512 MB+ | 1GB+ recommended |
| **Disk Space** | 100 MB | For code and dependencies |
| **Network** | Wi-Fi/Ethernet | Required for Alexa integration |

### Python Dependencies

- **requests** ≥ 2.31.0 - HTTP requests
- **pyserial** ≥ 3.5 - Serial communication
- **python-dotenv** ≥ 1.0.0 - Environment configuration
- **flask** ≥ 2.0.0 - Web server (for dashboard)

---

## 📚 Documentation

Our documentation is comprehensive and designed to help you at every step:

### 📖 User Guides

| Guide | Description | Audience |
|-------|-------------|----------|
| **[API Reference](docs/API.md)** | Complete API with examples | Developers |
| **[Hardware Setup](docs/HARDWARE_SETUP.md)** | Physical assembly guide | Hardware hackers |
| **[Examples Guide](examples/README.md)** | Code tutorials and demos | All users |
| **[Troubleshooting](docs/TROUBLESHOOTING.md)** | Solutions to common issues | All users |

### 🛠️ Developer Resources

| Resource | Description | Use When |
|----------|-------------|----------|
| **[Architecture Guide](docs/ARCHITECTURE.md)** | System design details | Understanding internals |
| **[Testing Guide](docs/TESTING.md)** | Running and writing tests | Contributing code |
| **[Contributing Guide](CONTRIBUTING.md)** | Contribution workflow | Making changes |
| **[Code of Conduct](CODE_OF_CONDUCT.md)** | Community guidelines | Participating |

### 🔐 Policies

| Policy | Description |
|--------|-------------|
| **[Security Policy](SECURITY.md)** | Vulnerability reporting |
| **[Changelog](CHANGELOG.md)** | Version history |

---

## 🏗️ Architecture

### High-Level Overview

```
┌─────────────────┐
│  Amazon Echo    │ ◄─── Voice Commands
└────────┬────────┘
         │ UPnP/SSDP
         ▼
┌─────────────────────────────────────┐
│      Raspberry Pi Zero W            │
│  ┌───────────────────────────────┐  │
│  │  Python Application           │  │
│  │  ┌────────────┐ ┌───────────┐ │  │
│  │  │  Fauxmo    │ │  Create   │ │  │
│  │  │  (Alexa)   │ │  (Robot)  │ │  │
│  │  └──────┬─────┘ └─────┬─────┘ │  │
│  └─────────┼─────────────┼───────┘  │
│            │             │          │
└────────────┼─────────────┼──────────┘
             │             │ Serial (115200 baud)
             ▼             ▼
      ┌──────────────────────────┐
      │    iRobot Roomba         │
      │  ┌────────────────────┐  │
      │  │  Open Interface    │  │
      │  │  Sensors & Motors  │  │
      │  └────────────────────┘  │
      └──────────────────────────┘
```

### Key Components

- **Fauxmo**: Emulates Belkin WeMo device for Alexa discovery
- **Create Class**: Python interface to iRobot Open Interface protocol
- **Serial Bridge**: PySerial communication with Roomba
- **UPnP/SSDP**: Device discovery protocol
- **Open Interface**: iRobot's low-level control protocol

For detailed architecture information, see [Architecture Guide](docs/ARCHITECTURE.md).

---

## 🙏 Acknowledgments

### Original Concept
- **[FabricateIO](http://fabricate.io)** - Original Amazon Echo hacking concept
- **[Instructables Tutorial](http://www.instructables.com/id/Hacking-the-Amazon-Echo/)** - Initial inspiration

### Technologies & Tools
- **[iRobot](https://www.irobot.com/)** - Open Interface specification
- **[Python Software Foundation](https://www.python.org/)** - Python language
- **[PySerial](https://github.com/pyserial/pyserial)** - Serial communication library
- **[Amazon Alexa](https://developer.amazon.com/alexa)** - Voice control platform

### Special Thanks
- **Raspberry Pi Foundation** - Affordable embedded computing platform
- **GitHub** - Code hosting and collaboration
- **pytest** - Testing framework
- Everyone who filed issues, suggested features, and contributed code

---

Comprehensive documentation is available in the `docs/` directory:

### 📚 User Guides
- **[Hardware Setup Guide](docs/HARDWARE_SETUP.md)** - Complete hardware assembly instructions with photos and diagrams
- **[API Documentation](docs/API.md)** - Detailed API reference with examples for all methods
- **[Troubleshooting Guide](docs/TROUBLESHOOTING.md)** - Solutions for common issues and error messages

### 🏗️ Developer Resources
- **[Architecture Overview](docs/ARCHITECTURE.md)** - System design, patterns, and component interactions
- **[Testing Guide](docs/TESTING.md)** - How to run tests, write new tests, and interpret coverage
- **[Contributing Guidelines](CONTRIBUTING.md)** - How to contribute to the project
- **[Changelog](CHANGELOG.md)** - Version history and release notes

### 🔒 Policies
- **[Code of Conduct](CODE_OF_CONDUCT.md)** - Community standards and expectations
- **[Security Policy](SECURITY.md)** - How to report security vulnerabilities

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
Implementing the iRobot Open Interface protocol required understanding two's complement arithmetic, byte packing, and timing-sensitive command sequences. See [PYTHON3_MIGRATION.md](docs/PYTHON3_MIGRATION.md) for details on the bytes handling migration.

### 3. UPnP Device Emulation
Emulating a WeMo device for Alexa discovery involved implementing SSDP multicast listening and HTTP response handling with proper UPnP headers.

### 4. Embedded System Constraints
Running on Raspberry Pi Zero W required optimizing for limited CPU and memory, implementing efficient polling loops, and handling serial timeouts gracefully.

---

## Contributing

We welcome contributions from the community! Whether you're fixing bugs, adding features, improving documentation, or testing hardware compatibility, your help is appreciated.

### How to Contribute

1. **Read the Guidelines**: Check out [CONTRIBUTING.md](CONTRIBUTING.md) for detailed contribution guidelines
2. **Find an Issue**: Look for issues labeled [`good-first-issue`](https://github.com/antigenius0910/alexa_roomba/labels/good-first-issue) or [`help-wanted`](https://github.com/antigenius0910/alexa_roomba/labels/help-wanted)
3. **Fork & Code**: Fork the repository, make your changes, and submit a pull request
4. **Follow Standards**: Ensure your code passes tests and follows our coding standards

### Ways to Contribute

- 🐛 **Report Bugs**: Use our [bug report template](.github/ISSUE_TEMPLATE/bug_report.md)
- 💡 **Suggest Features**: Submit ideas via [feature request template](.github/ISSUE_TEMPLATE/feature_request.md)
- 📝 **Improve Docs**: Fix typos, add examples, or clarify instructions
- 🧪 **Write Tests**: Increase test coverage or add hardware compatibility tests
- 🤖 **Test Hardware**: Report compatibility with different Roomba models
- 💻 **Submit Code**: Fix bugs or implement new features

### Development Setup

```bash
# Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/alexa_roomba.git
cd alexa_roomba

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest
```

### Community Guidelines

- Follow our [Code of Conduct](CODE_OF_CONDUCT.md)
- Be respectful and constructive
- Help others learn and grow
- Report security issues privately via [SECURITY.md](SECURITY.md)

For detailed information, see [CONTRIBUTING.md](CONTRIBUTING.md).

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
