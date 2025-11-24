# Deployment Guide

Complete guide for deploying Alexa Roomba in production environments.

---

## Table of Contents

1. [Quick Install](#quick-install)
2. [Manual Installation](#manual-installation)
3. [Configuration](#configuration)
4. [Systemd Service Setup](#systemd-service-setup)
5. [Troubleshooting](#troubleshooting)
6. [Update & Maintenance](#update--maintenance)

---

## Quick Install

The automated installer handles everything for you:

```bash
git clone https://github.com/antigenius0910/alexa_roomba.git
cd alexa_roomba
./install.sh
```

The installer will:
- ✅ Check Python 3.7+ installation
- ✅ Create virtual environment
- ✅ Install dependencies
- ✅ Configure settings interactively
- ✅ Set up systemd service (optional)
- ✅ Check serial port permissions

---

## Manual Installation

### 1. Prerequisites

```bash
# Install Python 3.7+
sudo apt update
sudo apt install python3 python3-pip python3-venv

# Install system dependencies (Raspberry Pi)
sudo apt install python3-dev git

# Add user to dialout group for serial access
sudo usermod -a -G dialout $USER
# Log out and back in for this to take effect
```

### 2. Clone and Setup

```bash
# Clone repository
git clone https://github.com/antigenius0910/alexa_roomba.git
cd alexa_roomba

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
pip install python-dotenv
```

### 3. Configure

```bash
# Copy configuration template
cp .env.example .env

# Edit configuration
nano .env
```

---

## Configuration

### Environment Variables (.env)

```bash
# Serial Port Configuration
ROOMBA_PORT=/dev/ttyUSB0        # Your serial port
ROOMBA_BAUD_RATE=115200         # Usually 115200

# Alexa Device Settings
FAUXMO_DEVICE_NAME="Stardust Destroyer"
FAUXMO_PORT=52000
FAUXMO_DEBUG=true

# Robot Mode
DEFAULT_MODE=SAFE_MODE          # SAFE_MODE or FULL_MODE

# Logging
LOG_LEVEL=INFO                  # DEBUG, INFO, WARNING, ERROR
LOG_FILE=                       # Optional log file path
```

### Platform-Specific Ports

**Linux/Raspberry Pi:**
- USB-to-Serial: `/dev/ttyUSB0`
- Built-in UART: `/dev/ttyAMA0` or `/dev/serial0`

**macOS:**
- `/dev/tty.usbserial`
- `/dev/tty.usbserial-XXXXXXXX`

**Windows:**
- `COM3` (check Device Manager for actual port)

### Finding Your Serial Port

```bash
# Linux: List USB devices
ls /dev/ttyUSB* /dev/ttyAMA*

# macOS: List serial devices
ls /dev/tty.usb*

# Check permissions
ls -l /dev/ttyUSB0
```

---

## Systemd Service Setup

### Automatic Setup (Recommended)

Run the installer with systemd option:

```bash
./install.sh
# Select 'y' when prompted for systemd service
```

### Manual Setup

1. **Update service file with your paths:**

```bash
sed "s|INSTALL_DIR|$PWD|g" roomba.service.template > roomba.service
```

2. **Install service:**

```bash
sudo cp roomba.service /etc/systemd/system/
sudo systemctl daemon-reload
```

3. **Enable and start:**

```bash
# Enable auto-start on boot
sudo systemctl enable roomba.service

# Start service now
sudo systemctl start roomba.service

# Check status
sudo systemctl status roomba.service
```

### Service Management Commands

```bash
# Start service
sudo systemctl start roomba.service

# Stop service
sudo systemctl stop roomba.service

# Restart service
sudo systemctl restart roomba.service

# Check status
sudo systemctl status roomba.service

# View logs
journalctl -u roomba.service -f

# View recent logs
journalctl -u roomba.service --since "1 hour ago"

# Disable auto-start
sudo systemctl disable roomba.service
```

---

## Testing Deployment

### 1. Test Configuration

```bash
# Activate virtual environment
source venv/bin/activate

# Test configuration loading
python config.py
```

### 2. Test Robot Connection

```bash
python -c "from roomba import Create; r = Create('/dev/ttyUSB0'); r.printSensors(); r.close()"
```

### 3. Test Alexa Integration

```bash
# Start service
python example-minimal.py

# In another terminal, check if it's running
ps aux | grep example-minimal

# Say to your Echo:
# "Alexa, discover my devices"
# Then: "Alexa, turn on stardust destroyer"
```

### 4. Test Systemd Service

```bash
# Start via systemd
sudo systemctl start roomba.service

# Check if running
sudo systemctl status roomba.service

# Check logs
tail -f logs/roomba_$(date +%Y%m%d).log
```

---

## Troubleshooting

### Serial Port Access Denied

```bash
# Check current permissions
ls -l /dev/ttyUSB0

# Add user to dialout group
sudo usermod -a -G dialout $USER

# Log out and back in, then verify
groups | grep dialout
```

### Service Won't Start

```bash
# Check service status
sudo systemctl status roomba.service

# View detailed logs
journalctl -u roomba.service -n 50

# Check if port is already in use
lsof | grep /dev/ttyUSB0

# Kill stuck processes
pkill -f "python.*example-minimal"
```

### Alexa Not Discovering Device

1. **Check network connectivity:**
```bash
# Verify Echo and Pi are on same network
ip addr show

# Test UPnP multicast
nc -u 239.255.255.250 1900
```

2. **Check Fauxmo port:**
```bash
# Verify port 52000 is listening
netstat -tulpn | grep 52000
```

3. **Restart discovery:**
- Say: "Alexa, forget all devices"
- Restart the service
- Say: "Alexa, discover my devices"

### Robot Not Responding

```bash
# Test serial communication
python -c "
import serial
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
ser.write(bytes([128]))  # Start command
print('Sent start command')
ser.close()
"

# Check cable connections
# Verify baud rate (should be 115200 for most models)
```

### Logs Location

```bash
# Application logs
tail -f logs/roomba_$(date +%Y%m%d).log

# Systemd logs
journalctl -u roomba.service -f

# All logs in directory
ls -lh logs/
```

---

## Update & Maintenance

### Update Code

```bash
cd /path/to/alexa_roomba

# Stop service
sudo systemctl stop roomba.service

# Pull latest changes
git pull origin master

# Update dependencies
source venv/bin/activate
pip install --upgrade -r requirements.txt

# Restart service
sudo systemctl start roomba.service
```

### Backup Configuration

```bash
# Backup your .env file
cp .env .env.backup

# Backup logs
tar -czf logs_backup_$(date +%Y%m%d).tar.gz logs/
```

### Log Rotation

Add to `/etc/logrotate.d/roomba`:

```
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

## Production Best Practices

1. **Use virtual environment** - Isolate dependencies
2. **Enable systemd service** - Auto-start on boot
3. **Monitor logs** - Set up log rotation
4. **Backup configuration** - Keep `.env` backed up
5. **Update regularly** - Pull latest security fixes
6. **Use SAFE_MODE** - Prevents cliff falls
7. **Test before deploy** - Verify on test system first

---

## Security Considerations

1. **Serial Port Access:**
   - Only add trusted users to `dialout` group
   - Restrict physical access to Raspberry Pi

2. **Network Security:**
   - Use WPA2/WPA3 for WiFi
   - Consider network segmentation (IoT VLAN)
   - Firewall unnecessary ports

3. **File Permissions:**
   - Keep sensitive config files readable only by service user
   - Don't commit `.env` to git (already in `.gitignore`)

---

## Getting Help

If you encounter issues not covered here:

1. Check [GitHub Issues](https://github.com/antigenius0910/alexa_roomba/issues)
2. Review logs with `journalctl -u roomba.service`
3. Run installer again: `./install.sh`
4. See [README.md](README.md) for general documentation

---

## Additional Resources

- [iRobot Open Interface Spec](https://www.irobot.com/about-irobot/stem/create-2)
- [Systemd Service Management](https://www.freedesktop.org/software/systemd/man/systemd.service.html)
- [Python Serial Documentation](https://pyserial.readthedocs.io/)
- [Alexa Smart Home API](https://developer.amazon.com/en-US/docs/alexa/smarthome/understand-the-smart-home-skill-api.html)
