# Alexa Roomba Examples

This directory contains a comprehensive collection of examples demonstrating various capabilities of the Alexa Roomba project, from basic robot control to advanced autonomous behaviors and IoT integration.

## 📚 Table of Contents

- [Quick Start](#quick-start)
- [Basic Examples](#basic-examples)
- [Advanced Examples](#advanced-examples)
- [Integration Examples](#integration-examples)
- [Demo Scripts](#demo-scripts)
- [Learning Path](#learning-path)

---

## Quick Start

All examples require the robot to be connected via serial port. Make sure your configuration is set up:

```bash
# Create and configure .env file (if not already done)
cp ../.env.example ../.env
nano ../.env  # Set ROOMBA_PORT to your serial port

# Install dependencies
pip install -r ../requirements.txt

# Run any example
python simple_movement.py
```

---

## Basic Examples

### 1. Simple Movement (`simple_movement.py`)

**Skill Level:** Beginner
**Concepts:** Basic robot control, movement commands

Demonstrates fundamental robot control including forward movement, rotation, and curved paths.

```bash
python simple_movement.py
```

**What You'll Learn:**
- Connecting to the robot
- Basic movement commands (go, stop)
- Safe mode operation

---

### 2. Sensor Reading (`sensor_reading.py`)

**Skill Level:** Beginner
**Concepts:** Sensor data acquisition, real-time monitoring

Continuously reads and displays various sensor values including battery, cliff sensors, encoders, and proximity sensors.

```bash
python sensor_reading.py
```

**What You'll Learn:**
- Reading sensor packets
- Battery monitoring
- Cliff and proximity detection
- Encoder values for odometry

---

### 3. Music Playback (`play_music.py`)

**Skill Level:** Beginner
**Concepts:** MIDI control, robot entertainment features

Demonstrates the robot's music capabilities by playing melodies using MIDI notes.

```bash
python play_music.py
```

**What You'll Learn:**
- MIDI note definitions
- Song composition
- Playing melodies on the robot

---

## Advanced Examples

### 4. Wall Following Algorithm (`wall_following.py`)

**Skill Level:** Intermediate
**Concepts:** Reactive control, sensor fusion, state machines, autonomous navigation

Implements a sophisticated wall-following algorithm using proportional control and a state machine architecture.

```bash
python wall_following.py
```

**Key Features:**
- **Proportional Control:** Maintains constant distance from wall
- **State Machine:** Seeking, Following, and Bumped states
- **Reactive Behavior:** Real-time sensor-based decision making
- **Obstacle Recovery:** Automatic bump detection and avoidance

**What You'll Learn:**
- PID-like proportional control
- Behavior-based robotics
- State machine design
- Reactive control loops

**Technical Highlights:**
```python
# Proportional control calculation
error = TARGET_WALL_SIGNAL - current_wall_signal
spin_correction = KP * error
```

---

### 5. Autonomous Cleaning (`autonomous_cleaning.py`)

**Skill Level:** Advanced
**Concepts:** Coverage path planning, behavior-based architecture, multi-sensor fusion

Demonstrates intelligent room coverage using spiral pattern movement combined with obstacle avoidance and cliff detection.

```bash
python autonomous_cleaning.py
```

**Key Features:**
- **Spiral Coverage Pattern:** Expanding spiral for maximum area coverage
- **Priority-Based Behaviors:** Safety (cliffs) > Obstacles (bumps) > Coverage
- **Obstacle Avoidance:** Intelligent bump-and-turn reactions
- **Safety Mechanisms:** Emergency cliff detection and avoidance
- **Statistics Tracking:** Monitors coverage time and obstacle encounters

**What You'll Learn:**
- Coverage path planning algorithms
- Behavior-based architecture (subsumption architecture concepts)
- Multi-sensor integration
- Priority-based decision making

**Behavior Priority:**
1. **Cliff Detection** (Highest - Safety)
2. **Bump Reaction** (Obstacle Avoidance)
3. **Spiral Pattern** (Default Cleaning)

---

## Integration Examples

### 6. Alexa Voice Control (`alexa_voice_control.py`)

**Skill Level:** Intermediate
**Concepts:** IoT integration, voice-activated control, REST API concepts, UPnP

Complete Alexa Smart Home integration using Fauxmo to emulate a Belkin WeMo device.

```bash
python alexa_voice_control.py
```

**Voice Commands:**
- *"Alexa, turn on [device name]"* - Start cleaning
- *"Alexa, turn off [device name]"* - Stop cleaning
- *"Alexa, set [device name] to 75 percent"* - Set cleaning intensity

**Setup:**
1. Start the script
2. Say: *"Alexa, discover my devices"*
3. Wait for discovery to complete
4. Use voice commands

**What You'll Learn:**
- IoT device emulation
- UPnP/SSDP protocols
- REST API concepts
- Asynchronous event handling
- Voice UI design

**Technical Highlights:**
- Fauxmo library for Alexa integration
- Threading for concurrent operation
- State management for robot control
- Statistics tracking

---

### 7. Sensor Monitoring Dashboard (`sensor_dashboard.py`)

**Skill Level:** Advanced
**Concepts:** Full-stack development, real-time data streaming, web development

Real-time web dashboard for monitoring robot sensors using Flask and Server-Sent Events (SSE).

```bash
python sensor_dashboard.py
```

Then open your browser to: `http://localhost:5000`

**Key Features:**
- **Real-Time Updates:** Live sensor data via Server-Sent Events
- **Visual Interface:** Clean, responsive web dashboard
- **Multiple Sensors:** Battery, proximity, cliffs, bumps, encoders
- **Historical Data:** Time-series data collection for charting
- **REST API:** JSON API endpoint for integration

**What You'll Learn:**
- Flask web framework
- Server-Sent Events (SSE) for real-time updates
- REST API design
- Front-end development (HTML/CSS/JavaScript)
- Data visualization concepts
- Concurrent sensor monitoring (threading)

**API Endpoints:**
- `GET /` - Dashboard HTML interface
- `GET /api/sensors` - JSON sensor data
- `GET /stream` - SSE stream for real-time updates

**Technical Stack:**
- **Backend:** Flask (Python)
- **Real-time:** Server-Sent Events
- **Frontend:** Vanilla JavaScript, CSS3
- **Threading:** Background sensor monitoring

---

## Demo Scripts

### 8. Video Demonstration (`video_demo.py`)

**Skill Level:** All Levels
**Concepts:** Structured demonstration, portfolio presentation

Comprehensive demonstration script perfect for recording portfolio videos or giving live presentations.

```bash
python video_demo.py
```

**Interactive Mode:** Pauses between demonstrations
**Continuous Mode:** Runs all demos automatically

**Demonstration Flow:**
1. **System Initialization** - Connection and setup
2. **Basic Movement** - Forward, rotate, turn
3. **Sensor Monitoring** - Battery, proximity, bumps
4. **Music Playback** - MIDI melodies
5. **Wall Following** - Reactive control demo
6. **Spiral Cleaning** - Coverage pattern demo

**Perfect For:**
- Portfolio video creation
- Live demonstrations
- Feature showcases
- Technical presentations

---

## Learning Path

### Beginner Track
Start here if you're new to robotics or Python:

1. `simple_movement.py` - Learn basic robot control
2. `sensor_reading.py` - Understand sensor data
3. `play_music.py` - Explore entertainment features

### Intermediate Track
Continue with these for more advanced concepts:

4. `wall_following.py` - Learn reactive control and state machines
5. `alexa_voice_control.py` - Explore IoT integration

### Advanced Track
Master these for full-stack and autonomous systems:

6. `autonomous_cleaning.py` - Behavior-based architecture
7. `sensor_dashboard.py` - Full-stack development

### Portfolio Preparation

8. `video_demo.py` - Create professional demonstrations

---

## Technical Concepts Covered

### Robotics
- ✅ Basic movement control
- ✅ Sensor data acquisition and processing
- ✅ Reactive control (proportional control)
- ✅ State machines
- ✅ Behavior-based architecture
- ✅ Coverage path planning
- ✅ Obstacle avoidance
- ✅ Multi-sensor fusion

### Software Engineering
- ✅ Object-oriented design
- ✅ Modular architecture
- ✅ Error handling and recovery
- ✅ Logging and debugging
- ✅ Threading and concurrency
- ✅ Configuration management

### Integration & IoT
- ✅ IoT device emulation (UPnP/SSDP)
- ✅ Voice control integration (Alexa)
- ✅ REST API design
- ✅ Real-time data streaming (SSE)
- ✅ Web dashboard development

### Full-Stack Development
- ✅ Backend (Flask/Python)
- ✅ Frontend (HTML/CSS/JavaScript)
- ✅ Real-time communication
- ✅ API design
- ✅ Data visualization

---

## Hardware Requirements

- iRobot Create/Roomba with Open Interface
- USB-to-Serial adapter (or built-in serial port)
- Power source for the robot

For voice control:
- Amazon Echo or Alexa-enabled device
- Both devices on same network

---

## Troubleshooting

### Serial Port Issues
```bash
# Linux: Check port permissions
ls -l /dev/ttyUSB0
sudo usermod -a -G dialout $USER

# macOS: List available ports
ls /dev/tty.usb*

# Find your port
python -c "import serial.tools.list_ports; print([p.device for p in serial.tools.list_ports.comports()])"
```

### Alexa Discovery Issues
1. Ensure Alexa and robot are on same network
2. Check firewall settings (port 52000)
3. Say "Alexa, forget all devices" and rediscover
4. Restart the service and try again

### Dashboard Not Loading
1. Check if Flask is installed: `pip list | grep Flask`
2. Ensure port 5000 is not in use: `lsof -i :5000`
3. Check firewall allows localhost connections
4. Try accessing from different browser

---

## Additional Resources

- [Main README](../README.md) - Project overview and setup
- [Deployment Guide](../DEPLOYMENT.md) - Production deployment
- [Hardware Setup](../HARDWARE_SETUP.md) - Battery tap guide
- [iRobot Open Interface Spec](https://www.irobot.com/about-irobot/stem/create-2) - Official documentation

---

## Contributing

Have an interesting example to add? Contributions are welcome!

1. Fork the repository
2. Create your example script
3. Add documentation to this README
4. Submit a pull request

**Example Template:**
- Clear docstring with description
- Logging for debugging
- Error handling
- Comments explaining key concepts
- Example usage in `if __name__ == "__main__"`

---

## License

MIT License - See [LICENSE](../LICENSE) for details

---

**Created for portfolio demonstration and educational purposes.**
*Showcasing robotics, IoT integration, and full-stack development skills.*
