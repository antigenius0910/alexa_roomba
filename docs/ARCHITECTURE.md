# System Architecture

This document provides a comprehensive overview of the Alexa Roomba system architecture, design decisions, and technical implementation details.

## Table of Contents

- [System Overview](#system-overview)
- [Architecture Diagram](#architecture-diagram)
- [Component Architecture](#component-architecture)
- [Communication Protocols](#communication-protocols)
- [Data Flow](#data-flow)
- [Design Patterns](#design-patterns)
- [Hardware Architecture](#hardware-architecture)
- [Software Stack](#software-stack)
- [Deployment Architecture](#deployment-architecture)
- [Security Considerations](#security-considerations)
- [Performance Optimization](#performance-optimization)
- [Design Decisions](#design-decisions)

---

## System Overview

The Alexa Roomba project is a distributed embedded system that enables voice-controlled robotic vacuum cleaning through integration with Amazon's Alexa ecosystem.

### High-Level Components

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   Amazon    │  Voice  │  Raspberry   │ Serial  │   iRobot    │
│    Echo     │ ──────> │   Pi Zero    │ ──────> │   Roomba    │
│   Device    │  WiFi   │  Controller  │  UART   │   Robot     │
└─────────────┘         └──────────────┘         └─────────────┘
       │                        │                        │
       │                        │                        │
   UPnP/SSDP              Python Runtime           Robot Firmware
   Discovery              Fauxmo Server            OI Protocol
```

### System Characteristics

- **Type:** Distributed embedded IoT system
- **Architecture:** Event-driven, reactive control
- **Communication:** Serial (UART), Network (UPnP/SSDP)
- **Deployment:** Single-board computer (Raspberry Pi Zero W)
- **Power:** Parasitic from robot battery (14.4V → 5V conversion)

---

## Architecture Diagram

### Layer Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Application Layer                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │    Voice     │  │  Autonomous  │  │     Web      │     │
│  │   Control    │  │  Behaviors   │  │  Dashboard   │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                            │
┌─────────────────────────────────────────────────────────────┐
│                     Integration Layer                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Fauxmo     │  │    Flask     │  │   Threading  │     │
│  │  (UPnP/SSDP) │  │  (HTTP/SSE)  │  │   Manager    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                            │
┌─────────────────────────────────────────────────────────────┐
│                      Business Logic Layer                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │    Roomba    │  │   Behavior   │  │    Sensor    │     │
│  │   Package    │  │   Control    │  │  Processing  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                            │
┌─────────────────────────────────────────────────────────────┐
│                     Hardware Abstraction Layer               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Create     │  │   PySerial   │  │     UART     │     │
│  │    Class     │  │   Library    │  │   Driver     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                            │
┌─────────────────────────────────────────────────────────────┐
│                        Hardware Layer                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Raspberry   │  │  DC-DC       │  │   iRobot     │     │
│  │  Pi Zero W   │  │  Converter   │  │   Create     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

---

## Component Architecture

### 1. Core Robot Control (`roomba/` package)

**Purpose:** Low-level robot communication and control abstraction

**Components:**

```
roomba/
├── __init__.py         # Public API exports
├── commands.py         # Command byte constants (28 commands)
├── sensors.py          # Sensor definitions (50+ sensors)
├── music.py            # MIDI note constants (40+ notes)
├── utils.py            # Utility functions (bit ops, conversions)
└── robot.py            # Create class wrapper
```

**Responsibilities:**
- Serial communication management
- Protocol byte encoding/decoding
- Sensor data parsing
- Movement command generation
- Music composition
- Mode management

**Key Classes:**
- `Create`: Main robot control interface
- `SensorFrame`: Sensor data container

---

### 2. Legacy Compatibility Layer (`create.py`)

**Purpose:** Maintain backwards compatibility with original codebase

**Structure:**
- Monolithic 1600+ line file
- Contains original `Create` class implementation
- Includes all sensors, commands, and utilities
- Used by `example-minimal.py` for Alexa integration

**Design Decision:**
- Kept intact to avoid breaking existing integrations
- New code should use `roomba/` package instead
- Will be deprecated in future versions

---

### 3. IoT Integration Layer (`fauxmo.py`)

**Purpose:** Emulate Belkin WeMo device for Alexa discovery

**Architecture:**

```python
class fauxmo:
    """UPnP/SSDP server for Alexa device emulation"""

    Components:
    - SSDP Multicast Listener (UDP 1900)
    - HTTP Server (TCP, dynamic port)
    - Device Description XML Generator
    - Event Notification Handler
```

**Protocol Implementation:**

1. **SSDP Discovery (Multicast)**
   ```
   Client (Alexa) → Multicast: M-SEARCH request
   Server (Fauxmo) → Unicast: Device announcement
   ```

2. **Device Description (HTTP)**
   ```
   Client → GET /setup.xml
   Server → Device metadata XML
   ```

3. **Control (HTTP)**
   ```
   Client → POST /upnp/control/basicevent1
   Server → SOAP response
   ```

**Threading Model:**
- Main thread: SSDP listener
- Worker threads: HTTP request handlers
- Event callbacks: User-defined device actions

---

### 4. Configuration Management (`config.py`)

**Purpose:** Centralized configuration with environment variable support

**Architecture:**

```python
Configuration Sources (Priority Order):
1. Environment Variables (.env file)
2. Python Defaults (fallback)

Features:
- Platform detection (Linux/macOS/Windows)
- Auto-port discovery
- Logging configuration
- Physical calibration parameters
```

**Configuration Categories:**

| Category | Settings | Source |
|----------|----------|--------|
| Serial | Port, baud rate, timeout | Environment/Platform |
| Robot | Mode, physical params | Hardcoded/Calibrated |
| Alexa | Device name, port | Environment |
| Logging | Level, format, file | Environment |
| Install | Paths, executables | Auto-detected |

---

### 5. Application Examples

**Purpose:** Demonstrate capabilities and provide templates

**Categories:**

1. **Basic Examples** (Beginner)
   - `simple_movement.py`: Movement API
   - `sensor_reading.py`: Sensor access
   - `play_music.py`: Music playback

2. **Advanced Examples** (Intermediate/Advanced)
   - `wall_following.py`: Reactive control + state machine
   - `autonomous_cleaning.py`: Behavior-based architecture
   - `sensor_dashboard.py`: Full-stack web application

3. **Integration Examples**
   - `alexa_voice_control.py`: Complete IoT integration
   - `example-minimal.py`: Minimal Alexa example

4. **Demo Scripts**
   - `video_demo.py`: Structured demonstration

---

## Communication Protocols

### 1. iRobot Open Interface (OI) Protocol

**Type:** Bidirectional serial protocol (UART)
**Baud Rate:** 115200 bps (default)
**Data Format:** 8N1 (8 data bits, no parity, 1 stop bit)

**Command Structure:**

```
┌────────────┬────────────┬────────────┬─────────────┐
│  Opcode    │  Data 0    │  Data 1    │   Data N    │
│  (1 byte)  │  (varies)  │  (varies)  │   (varies)  │
└────────────┴────────────┴────────────┴─────────────┘
```

**Example - Drive Command:**

```
Opcode: 137 (DRIVE)
Data 0-1: Velocity (mm/s, signed 16-bit)
Data 2-3: Radius (mm, signed 16-bit)

Hex: 89 00 C8 80 00
Meaning: Drive straight at 200 mm/s
```

**Sensor Protocol:**

```
Request:  [142] [Packet ID]
Response: [Packet Data] (varies by sensor)

Example:
Request:  [142] [25]       # Battery charge
Response: [09] [C4]        # 2500 mAh
```

**Key Characteristics:**
- Command-response model
- Fixed command opcodes
- Big-endian byte order
- Two's complement for signed values
- No checksum (reliability via UART)

---

### 2. UPnP/SSDP Protocol

**Type:** Device discovery and control protocol
**Transport:** UDP (discovery), HTTP (control)

**Discovery Flow:**

```
1. Alexa broadcasts M-SEARCH:
   MULTICAST UDP → 239.255.255.250:1900

2. Fauxmo responds:
   UNICAST UDP → Alexa IP:ephemeral port

3. Alexa fetches device description:
   HTTP GET → Fauxmo IP:port/setup.xml

4. Alexa sends control commands:
   HTTP POST → Fauxmo IP:port/upnp/control/basicevent1
```

**M-SEARCH Request:**
```http
M-SEARCH * HTTP/1.1
HOST: 239.255.255.250:1900
MAN: "ssdp:discover"
MX: 3
ST: urn:Belkin:device:**
```

**Response:**
```http
HTTP/1.1 200 OK
CACHE-CONTROL: max-age=86400
EXT:
LOCATION: http://192.168.1.100:52000/setup.xml
SERVER: FauxMo/1.0 UPnP/1.0
ST: urn:Belkin:device:**
USN: uuid:Socket-1_0-12345678::urn:Belkin:device:**
```

---

### 3. HTTP/Server-Sent Events (SSE)

**Type:** Real-time web communication
**Use Case:** Sensor dashboard

**Architecture:**

```
Client (Browser)                Server (Flask)
       │                                │
       │─── HTTP GET / ────────────────>│ Serve HTML
       │<─────── HTML ──────────────────│
       │                                │
       │─── GET /stream ───────────────>│ Open SSE connection
       │<──── Event: data ──────────────│ Send sensor data
       │<──── Event: data ──────────────│ (every 500ms)
       │<──── Event: data ──────────────│
       │                                │
       │─── GET /api/sensors ──────────>│ REST API call
       │<─────── JSON ──────────────────│ Sensor snapshot
```

**SSE Format:**
```
data: {"battery": {"charge": 2500}, "connected": true}\n\n
```

---

## Data Flow

### Voice Command Flow

```
User Voice → Echo Device
              │
              ├─ Speech Recognition (AWS)
              │
              ├─ Intent Recognition
              │
              ├─ Device Discovery (SSDP)
              │
              ├─ HTTP POST to Fauxmo
              │
              ├─ fauxmo_device.on() callback
              │
              ├─ Robot Command Translation
              │
              ├─ Serial Command (OI Protocol)
              │
              └─> Robot Execution
```

### Sensor Reading Flow

```
Application Request
    │
    ├─> Create.sensors([sensor_ids])
    │
    ├─> Serial Write: [142][id]
    │
    ├─> Serial Read: response bytes
    │
    ├─> Byte Parsing & Decoding
    │
    ├─> Dictionary Population
    │
    └─> Return: robot.sensord
```

### Autonomous Behavior Flow

```
Behavior State Machine
    │
    ├─> Read Sensors
    │    └─> Battery, Cliff, Bump, Wall
    │
    ├─> Behavior Selection (Priority)
    │    ├─ Safety (Cliff) [Highest]
    │    ├─ Obstacle (Bump)
    │    └─ Coverage (Default) [Lowest]
    │
    ├─> Control Calculation
    │    └─> Velocity, Spin
    │
    ├─> Send Drive Command
    │
    └─> Loop (100ms cycle)
```

---

## Design Patterns

### 1. Hardware Abstraction Layer (HAL)

**Pattern:** Abstraction Layer
**Purpose:** Decouple hardware specifics from business logic

```python
# High-level API
robot.go(20, 0)

# Abstracts:
# - Byte encoding
# - Serial communication
# - Protocol details
# - Hardware differences
```

**Benefits:**
- Easy testing (mock serial port)
- Platform independence
- Protocol changes isolated

---

### 2. State Machine Pattern

**Pattern:** Finite State Machine
**Use Case:** Wall following, autonomous behaviors

```python
class WallFollower:
    STATE_SEEKING = "seeking"
    STATE_FOLLOWING = "following"
    STATE_BUMPED = "bumped"

    def run(self):
        while True:
            sensors = self.read_sensors()

            if self.state == STATE_SEEKING:
                self.handle_seeking(sensors)
            elif self.state == STATE_FOLLOWING:
                self.handle_following(sensors)
            elif self.state == STATE_BUMPED:
                self.handle_bumped(sensors)
```

**Benefits:**
- Clear behavior transitions
- Easy to debug
- Maintainable code

---

### 3. Behavior-Based Architecture

**Pattern:** Subsumption Architecture
**Use Case:** Autonomous cleaning

```python
Priority Hierarchy:
1. Safety (Cliff Detection)     [HIGHEST]
2. Obstacle Avoidance (Bumps)
3. Coverage Pattern (Spiral)    [LOWEST]

# Higher priority behaviors suppress lower ones
if cliff_detected():
    handle_cliff()  # Overrides all
elif bump_detected():
    handle_bump()   # Overrides coverage
else:
    execute_spiral()  # Default
```

**Benefits:**
- Reactive and robust
- Emergent behaviors
- Graceful degradation

---

### 4. Observer Pattern

**Pattern:** Pub/Sub via callbacks
**Use Case:** Fauxmo device events

```python
class RoombaDevice(fauxmo_device):
    def on(self):
        # Called when Alexa turns on
        controller.start_cleaning()

    def off(self):
        # Called when Alexa turns off
        controller.stop_cleaning()
```

**Benefits:**
- Loose coupling
- Event-driven architecture
- Easy to extend

---

### 5. Facade Pattern

**Pattern:** Simplified Interface
**Use Case:** `Create` class wraps complex protocol

```python
# Complex protocol:
serial.write([137, 0, 200, 128, 0])  # Drive command

# Simple facade:
robot.go(20, 0)  # Same result
```

---

## Hardware Architecture

### Power System

```
Roomba Battery (14.4V, 3000mAh)
    │
    ├─> Battery Tap (custom)
    │
    ├─> DC-DC Converter (LM2596)
    │    Input: 14.4V DC
    │    Output: 5V DC @ 3A
    │
    ├─> Raspberry Pi Zero W
    │    Power: 5V @ 1-2A
    │    GPIO: 40-pin header
    │
    └─> USB-to-Serial Adapter
         UART: TX, RX, GND
```

### Serial Connection

```
Raspberry Pi          USB-Serial          Roomba
   UART                Adapter         Mini-DIN Port
    │                     │                  │
    ├─ TX (GPIO 14) ─────┼─ TX ─────────────┼─ RX (Pin 3)
    ├─ RX (GPIO 15) ─────┼─ RX ─────────────┼─ TX (Pin 4)
    └─ GND (Pin 6) ──────┼─ GND ────────────┼─ GND (Pin 7)
                                              │
                                              └─ Vpwr (Pin 1, 14.4V)
```

### Network Architecture

```
Home WiFi Network (2.4GHz)
    │
    ├─ Amazon Echo
    │   IP: 192.168.1.50
    │   Role: Voice interface
    │
    └─ Raspberry Pi Zero W
        IP: 192.168.1.100
        Role: Robot controller
        Services:
         - Fauxmo (Port 52000)
         - Flask Dashboard (Port 5000)
         - SSH (Port 22)
```

---

## Software Stack

### System Dependencies

```
Operating System: Raspbian Lite (Debian-based)
Python Runtime: Python 3.7+
Package Manager: pip

Core Libraries:
├── pyserial (3.5+)      # Serial communication
├── requests (2.31+)     # HTTP client
├── python-dotenv (1.0+) # Environment variables
└── flask (2.0+)         # Web framework (optional)

System Services:
├── systemd              # Service management
├── udev                 # Device permissions
└── networking           # WiFi connectivity
```

### File Structure

```
/home/pi/alexa_roomba/
├── roomba/              # Core package
├── examples/            # Example scripts
├── docs/                # Documentation
├── legacy/              # Deprecated code
├── .env                 # Environment config (not in git)
├── config.py            # Configuration module
├── create.py            # Legacy robot control
├── fauxmo.py            # Alexa integration
├── example-minimal.py   # Main entry point
├── install.sh           # Installer script
├── roomba-start.sh      # Service launcher
├── roomba.service       # Systemd unit (generated)
└── requirements.txt     # Python dependencies
```

---

## Deployment Architecture

### Service Architecture

```
systemd (PID 1)
    │
    └─> roomba.service
         │
         ├─> roomba-start.sh (Shell)
         │    │
         │    ├─> Load .env
         │    ├─> Activate venv
         │    └─> Launch Python
         │
         └─> python3 example-minimal.py
              │
              ├─> Fauxmo Server (Main Thread)
              │    └─> UPnP/SSDP Listener
              │
              ├─> HTTP Handlers (Worker Threads)
              │
              └─> Serial Communication
                   └─> /dev/ttyUSB0
```

### Process Management

**PID File:** `/home/pi/alexa_roomba/roomba.pid`
**Log Files:** `/home/pi/alexa_roomba/logs/roomba_YYYYMMDD.log`
**Service Type:** Forking daemon

**Lifecycle:**
1. `systemctl start roomba` → Start service
2. Service starts `roomba-start.sh`
3. Script writes PID file
4. Python process launches
5. Fauxmo begins listening
6. Service ready for commands

**Restart Policy:**
- On failure: Restart after 10s
- On success: Keep running
- On boot: Auto-start

---

## Security Considerations

### 1. Network Security

**Threats:**
- Unauthorized device access
- Command injection
- Network sniffing

**Mitigations:**
- UPnP/SSDP limited to local network
- No authentication required (trust LAN)
- No remote access by default
- Firewall rules recommended

**Recommendations:**
```bash
# Limit to local network only
iptables -A INPUT -p udp --dport 1900 -s 192.168.1.0/24 -j ACCEPT
iptables -A INPUT -p tcp --dport 52000 -s 192.168.1.0/24 -j ACCEPT
```

---

### 2. Serial Communication Security

**Threats:**
- Buffer overflow
- Malformed commands
- Device hijacking

**Mitigations:**
- Input validation in Create class
- Timeout protection
- Exclusive serial port access
- Safe mode by default (prevents damage)

---

### 3. File System Security

**Sensitive Files:**
- `.env` - Contains configuration
- `roomba.pid` - Process ID
- `logs/` - May contain debugging info

**Permissions:**
```bash
chmod 600 .env              # Owner read/write only
chmod 644 roomba-start.sh   # Owner write, all read
chmod 755 install.sh        # Owner write, all execute
```

---

### 4. Privilege Management

**User Permissions:**
- Run as non-root user (`pi`)
- Serial port access via `dialout` group
- No sudo required for operation

```bash
# Add user to dialout group
sudo usermod -a -G dialout pi
```

---

## Performance Optimization

### 1. Serial Communication

**Optimization:** Minimize command latency

```python
# Bad: Multiple small writes
for cmd in commands:
    serial.write(cmd)
    time.sleep(0.1)  # Unnecessary delay

# Good: Batch commands
serial.write(b''.join(commands))
```

**Results:**
- Latency: ~100ms → ~20ms
- Throughput: 10 cmd/s → 50 cmd/s

---

### 2. Sensor Reading

**Optimization:** Read only needed sensors

```python
# Bad: Read all sensors (slow)
robot.sensors()  # Reads 50+ sensors

# Good: Read specific sensors
robot.sensors([BATTERY_CHARGE, WALL_SIGNAL])
```

**Results:**
- Read time: ~500ms → ~50ms
- Allows 20Hz control loops

---

### 3. Threading Model

**Optimization:** Non-blocking I/O

```python
# Fauxmo: Main thread handles SSDP
# Worker threads handle HTTP requests
# Prevents blocking on serial I/O

# Dashboard: Background thread reads sensors
# Main thread serves web requests
# Prevents UI blocking
```

---

### 4. Memory Management

**Constraints:**
- Raspberry Pi Zero W: 512 MB RAM
- Python interpreter: ~50 MB
- Application: ~20 MB

**Optimizations:**
- No large data structures
- Fixed-size sensor dictionary
- Limited log file size
- Minimal dependencies

---

## Design Decisions

### 1. Why Python?

**Pros:**
- Easy serial communication (pyserial)
- Rapid development
- Rich ecosystem
- Good for prototyping

**Cons:**
- Slower than C/C++
- Higher memory usage
- GIL limits threading

**Decision:** Benefits outweigh drawbacks for this application

---

### 2. Why Fauxmo over Official Alexa Skill?

**Pros:**
- No cloud dependency
- Local network only
- Simple setup
- No AWS account needed

**Cons:**
- Limited to on/off/dim commands
- No voice feedback
- Hacky approach

**Decision:** Simplicity and local control preferred

---

### 3. Why Modular Package Structure?

**Pros:**
- Better organization
- Easier testing
- Reusable components
- Clearer dependencies

**Cons:**
- More files
- Import complexity
- Migration effort

**Decision:** Long-term maintainability worth the effort

---

### 4. Why Keep Legacy `create.py`?

**Pros:**
- Backwards compatibility
- Working example reference
- Avoid breaking changes

**Cons:**
- Code duplication
- Confusion for new users
- Technical debt

**Decision:** Pragmatic approach, deprecated gradually

---

## Future Enhancements

### Potential Improvements

1. **WebSocket Communication**
   - Replace SSE with WebSockets
   - Bidirectional control from dashboard
   - Lower latency

2. **MQTT Integration**
   - Publish sensor data to MQTT broker
   - Subscribe to command topics
   - Better IoT ecosystem integration

3. **Computer Vision**
   - Add Raspberry Pi Camera
   - Object detection
   - Visual navigation

4. **SLAM (Simultaneous Localization and Mapping)**
   - Build room map
   - Optimize coverage
   - Path planning

5. **Multi-Robot Coordination**
   - Fleet management
   - Collaborative cleaning
   - Distributed control

---

## Related Documentation

- [API Reference](API.md) - Complete API documentation
- [Hardware Setup](HARDWARE_SETUP.md) - Assembly instructions
- [Deployment Guide](DEPLOYMENT.md) - Production deployment
- [Examples](../examples/README.md) - Code examples

---

**Document Version:** 1.0
**Last Updated:** 2024
**Target Audience:** Developers, System Architects, Technical Reviewers
