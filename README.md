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

https://user-images.githubusercontent.com/5915590/138384009-169e9dc4-5142-4027-aa18-df4c367915f5.mp4

---

## 📑 Table of Contents

- [✨ Features](#-features)
- [🚀 Quick Start](#-quick-start)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Basic Usage](#basic-usage)
  - [Alexa Integration](#alexa-integration)
- [📦 System Requirements](#-system-requirements)
- [🔧 Hardware Requirements](#-hardware-requirements)
- [📚 Documentation](#-documentation)
- [🏗️ Architecture](#️-architecture)
- [🎯 Use Cases](#-use-cases)
- [🔬 Technical Highlights](#-technical-highlights)
- [❓ FAQ](#-faq)
- [🗺️ Roadmap](#️-roadmap)
- [🤝 Contributing](#-contributing)
- [⭐ Show Your Support](#-show-your-support)
- [📄 License](#-license)
- [🙏 Acknowledgments](#-acknowledgments)

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

## 🎯 Use Cases

### Home Automation
- **Voice-Activated Cleaning**: Start cleaning with Alexa voice commands
- **Scheduled Routines**: Integrate with Alexa routines for automatic scheduling
- **Multi-Room Coordination**: Control multiple Roombas individually

### Education & Learning
- **Robotics Education**: Teach robot control and serial communication
- **IoT Projects**: Demonstrate voice control and smart home integration
- **Python Programming**: Learn Python through practical robotics project

### Research & Development
- **Algorithm Testing**: Test navigation and mapping algorithms
- **Sensor Fusion**: Experiment with sensor data processing
- **Embedded Systems**: Learn embedded Linux on Raspberry Pi

### Entertainment
- **Musical Robot**: Create choreographed cleaning routines with music
- **Party Mode**: Impress guests with voice-controlled robot
- **Demo Platform**: Showcase at maker faires and tech events

---

## 🔬 Technical Highlights

### Serial Communication
- Implements complete iRobot Open Interface specification
- Two's complement arithmetic for signed integers
- Byte packing/unpacking for command encoding
- CRC verification for data integrity

### Voice Control
- UPnP device emulation for Alexa discovery
- SSDP multicast listener for device queries
- HTTP server for control commands
- SSE (Server-Sent Events) for state updates

### Embedded Systems
- Optimized for Raspberry Pi Zero W (limited resources)
- Efficient polling loops with minimal CPU usage
- Graceful serial timeout handling
- Memory-efficient sensor data structures

### Code Quality
- **280+ Tests**: Comprehensive test coverage with pytest
- **Type Hints**: Modern Python 3 type annotations
- **Documentation**: Detailed docstrings and examples
- **Linting**: Flake8 and black code formatting

---

## ❓ FAQ

<details>
<summary><b>Can I use this with Roomba 900 series?</b></summary>

The Roomba 900 series uses a different communication protocol. This project is designed for Roomba 500-800 series and Create 2, which use the Open Interface protocol. Check our [Hardware Compatibility](docs/HARDWARE_SETUP.md#roomba-models) guide for details.

</details>

<details>
<summary><b>Do I need to modify my Roomba hardware?</b></summary>

Yes, you need to install a battery tap and DC-DC converter inside the Roomba to power the Raspberry Pi. Our [Hardware Setup Guide](docs/HARDWARE_SETUP.md) provides detailed instructions with photos. This modification is reversible.

</details>

<details>
<summary><b>Can I run this without Alexa?</b></summary>

Absolutely! The core robot control functionality works independently of Alexa. You can use the Python API directly to control your Roomba via serial communication. Alexa is only needed for voice control features.

</details>

<details>
<summary><b>What serial adapter should I use?</b></summary>

We recommend FTDI-based USB-to-Serial adapters. They have excellent driver support across all platforms. Avoid cheap Prolific (PL2303) clones as they often have driver issues. See our [Hardware Guide](docs/HARDWARE_SETUP.md#serial-adapters) for specific recommendations.

</details>

<details>
<summary><b>Is this safe for my Roomba?</b></summary>

When following our guide properly, yes. The battery tap connection is safe, and the DC-DC converter protects the Raspberry Pi from voltage spikes. Always use proper voltage regulation and follow electrical safety guidelines. See [Safety Notes](docs/HARDWARE_SETUP.md#safety).

</details>

<details>
<summary><b>Can I control multiple Roombas?</b></summary>

Yes! Each Roomba needs its own Raspberry Pi and serial connection. You can run multiple instances of the software with different device names in Alexa (e.g., "Living Room Roomba", "Bedroom Roomba").

</details>

<details>
<summary><b>What's the range of voice control?</b></summary>

The range is determined by your Alexa device's listening range (typically 15-20 feet) and your Wi-Fi network coverage. The Roomba itself must be within Wi-Fi range of your network.

</details>

<details>
<summary><b>Can I add new features?</b></summary>

Yes! The codebase is modular and well-documented. Check our [Contributing Guide](CONTRIBUTING.md) and [Architecture Guide](docs/ARCHITECTURE.md) to get started. We welcome pull requests!

</details>

---

## 🗺️ Roadmap

### ✅ Completed
- [x] Python 3 migration with modern async/await
- [x] Comprehensive test suite (280+ tests)
- [x] Complete documentation (API, Architecture, Troubleshooting)
- [x] Hardware setup guide with photos
- [x] Multiple example scripts and demos
- [x] Packaging for pip installation

### 🚧 In Progress
- [ ] Web dashboard for monitoring and control
- [ ] REST API for third-party integrations
- [ ] MQTT support for home automation platforms

### 🔮 Future Plans
- [ ] Google Home integration
- [ ] HomeKit support
- [ ] Mobile app (iOS/Android)
- [ ] Mapping and navigation visualization
- [ ] Multi-robot coordination
- [ ] Machine learning for optimized cleaning patterns
- [ ] Docker containerization
- [ ] CI/CD pipeline with GitHub Actions

### 💡 Ideas Under Consideration
- [ ] Bluetooth control
- [ ] Camera integration for video streaming
- [ ] Scheduled cleaning with calendar integration
- [ ] Energy usage tracking and optimization
- [ ] Integration with other smart home devices
- [ ] Voice feedback from Roomba (TTS)

Want to contribute to any of these? Check out our [Contributing Guide](CONTRIBUTING.md)!

---

## 🤝 Contributing

We love contributions from the community! Whether you're fixing bugs, adding features, improving docs, or testing hardware, we appreciate your help.

### Quick Contribution Guide

1. **Fork** the repository on GitHub
2. **Clone** your fork locally: `git clone https://github.com/YOUR_USERNAME/alexa_roomba.git`
3. **Create a branch**: `git checkout -b feature/amazing-feature`
4. **Make changes** with tests
5. **Test**: Run `pytest` to ensure all tests pass
6. **Commit**: Use clear commit messages
7. **Push**: `git push origin feature/amazing-feature`
8. **Submit** a Pull Request

### Ways to Contribute

- 🐛 **Report Bugs**: Use our [bug report template](.github/ISSUE_TEMPLATE/bug_report.md)
- 💡 **Request Features**: Use our [feature request template](.github/ISSUE_TEMPLATE/feature_request.md)
- 📝 **Improve Docs**: Fix typos, add examples, clarify instructions
- 🧪 **Write Tests**: Help us reach 100% code coverage
- 🤖 **Test Hardware**: Report compatibility with different Roomba models
- 💻 **Submit Code**: Fix bugs or implement features
- 🌍 **Translate**: Help translate documentation (future)

See our [Contributing Guide](CONTRIBUTING.md) for detailed information.

---

## ⭐ Show Your Support

If you find this project useful, please consider:

- ⭐ **Star this repository** to help others discover it
- 🐛 **Report bugs** to help improve quality
- 💡 **Suggest features** to guide development
- 📝 **Improve documentation** to help future users
- 🤝 **Contribute code** to add new capabilities
- 📢 **Share** with friends and colleagues interested in robotics

**Together we can make voice-controlled robotics accessible to everyone!**

### Statistics

![GitHub stars](https://img.shields.io/github/stars/antigenius0910/alexa_roomba?style=social)
![GitHub forks](https://img.shields.io/github/forks/antigenius0910/alexa_roomba?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/antigenius0910/alexa_roomba?style=social)

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

**TL;DR**: You can use, modify, and distribute this project for any purpose, including commercial use, as long as you include the original copyright notice.

```
MIT License

Copyright (c) 2025 Zach Dodds, Sean Luke, James O'Beirne, Martin Schaef

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---

## 🙏 Acknowledgments

### Original Concept
- **[FabricateIO](http://fabricate.io)** - Original Amazon Echo hacking concept
- **[Instructables Tutorial](http://www.instructables.com/id/Hacking-the-Amazon-Echo/)** - Initial inspiration

### Core Contributors
- **Zach Dodds** - Architecture and robotics algorithms
- **Sean Luke** - Serial protocol implementation
- **James O'Beirne** - Alexa integration and networking
- **Martin Schaef** - Python 3 migration and testing

### Technologies & Tools
- **[iRobot](https://www.irobot.com/)** - Open Interface specification
- **[Python Software Foundation](https://www.python.org/)** - Python language
- **[PySerial](https://github.com/pyserial/pyserial)** - Serial communication library
- **[Amazon Alexa](https://developer.amazon.com/alexa)** - Voice control platform

### Community
- All our [contributors](https://github.com/antigenius0910/alexa_roomba/graphs/contributors) who have helped improve this project
- Everyone who has [starred](https://github.com/antigenius0910/alexa_roomba/stargazers) or [forked](https://github.com/antigenius0910/alexa_roomba/network/members) this repository
- The open-source community for inspiration and support

### Special Thanks
- **Raspberry Pi Foundation** - Affordable embedded computing platform
- **GitHub** - Code hosting and collaboration
- **pytest** - Testing framework
- Everyone who filed issues, suggested features, and contributed code

---

<div align="center">

### 🌟 Built with ❤️ by robotics enthusiasts for the maker community

**[⬆ Back to Top](#-alexa-roomba)**

</div>
