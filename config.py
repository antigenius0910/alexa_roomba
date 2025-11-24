"""
Configuration settings for Roomba control application.

This module centralizes all configuration parameters for easier management
and deployment across different environments.
"""

import logging

# Serial communication settings
DEFAULT_PORT = '/dev/ttyUSB0'  # Default serial port (Linux)
DEFAULT_BAUD_RATE = 115200     # Default baud rate for communication
SERIAL_TIMEOUT = 0.5           # Serial read timeout in seconds

# Alternative ports for different platforms
PORT_RASPBERRYPI = '/dev/ttyUSB0'
PORT_MACOS = '/dev/tty.usbserial'
PORT_WINDOWS = 'COM3'

# Robot operating modes
DEFAULT_MODE = 'SAFE_MODE'  # Start in safe mode by default

# Alexa/Fauxmo settings
FAUXMO_DEVICE_NAME = "Stardust Destroyer"
FAUXMO_PORT = 52000
FAUXMO_DEBUG = True

# Logging configuration
LOG_LEVEL = logging.INFO
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_FILE = None  # Set to a file path to enable file logging

# Robot physical parameters (can be calibrated for specific robot)
WHEEL_SPAN_MM = 235.0      # Distance between wheels
WHEEL_DIAMETER_MM = 72.0   # Wheel diameter
ANGULAR_ERROR_FACTOR = 360.0 / 450.0  # Calibration factor for turning

# Movement limits (safety bounds)
MAX_VELOCITY_CM_S = 50     # Maximum velocity in cm/s
MAX_SPIN_VELOCITY = 100    # Maximum spin velocity

# Timing constants
COMMAND_DELAY = 0.3        # Delay between commands in seconds
STARTUP_DELAY = 0.5        # Delay after initialization


def configure_logging(level=LOG_LEVEL, log_file=LOG_FILE):
    """
    Configure logging for the application.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path for log output
    """
    handlers = [logging.StreamHandler()]
    if log_file:
        handlers.append(logging.FileHandler(log_file))

    logging.basicConfig(
        level=level,
        format=LOG_FORMAT,
        handlers=handlers
    )


def get_platform_port():
    """
    Attempt to detect the appropriate serial port for the current platform.

    Returns:
        str: Detected or default port path
    """
    import platform
    import os

    system = platform.system()

    if system == 'Linux':
        # Check for Raspberry Pi
        if os.path.exists('/proc/device-tree/model'):
            with open('/proc/device-tree/model', 'r') as f:
                if 'Raspberry Pi' in f.read():
                    return PORT_RASPBERRYPI
        return DEFAULT_PORT
    elif system == 'Darwin':  # macOS
        return PORT_MACOS
    elif system == 'Windows':
        return PORT_WINDOWS
    else:
        return DEFAULT_PORT
