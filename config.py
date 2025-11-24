"""
Configuration settings for Roomba control application.

This module centralizes all configuration parameters for easier management
and deployment across different environments. Supports both Python defaults
and .env file overrides.
"""

import logging
import os
from pathlib import Path

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
        print(f"Loaded configuration from {env_path}")
except ImportError:
    # python-dotenv not installed, use environment variables only
    pass

# Serial communication settings
DEFAULT_PORT = os.getenv('ROOMBA_PORT', '/dev/ttyUSB0')
DEFAULT_BAUD_RATE = int(os.getenv('ROOMBA_BAUD_RATE', '115200'))
SERIAL_TIMEOUT = 0.5  # Serial read timeout in seconds

# Alternative ports for different platforms
PORT_RASPBERRYPI = '/dev/ttyUSB0'
PORT_MACOS = '/dev/tty.usbserial'
PORT_WINDOWS = 'COM3'

# Robot operating modes
DEFAULT_MODE = os.getenv('DEFAULT_MODE', 'SAFE_MODE')

# Alexa/Fauxmo settings
FAUXMO_DEVICE_NAME = os.getenv('FAUXMO_DEVICE_NAME', "Stardust Destroyer")
FAUXMO_PORT = int(os.getenv('FAUXMO_PORT', '52000'))
FAUXMO_DEBUG = os.getenv('FAUXMO_DEBUG', 'true').lower() == 'true'

# Logging configuration
LOG_LEVEL_STR = os.getenv('LOG_LEVEL', 'INFO')
LOG_LEVEL = getattr(logging, LOG_LEVEL_STR.upper(), logging.INFO)
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_FILE = os.getenv('LOG_FILE', None)

# Installation directory (auto-detect if not set)
INSTALL_DIR = os.getenv('INSTALL_DIR', str(Path(__file__).parent.absolute()))

# Python executable (auto-detect if not set)
PYTHON_EXEC = os.getenv('PYTHON_EXEC', 'python3')

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
            try:
                with open('/proc/device-tree/model', 'r') as f:
                    if 'Raspberry Pi' in f.read():
                        return PORT_RASPBERRYPI
            except:
                pass
        return DEFAULT_PORT
    elif system == 'Darwin':  # macOS
        return PORT_MACOS
    elif system == 'Windows':
        return PORT_WINDOWS
    else:
        return DEFAULT_PORT


def print_config():
    """Print current configuration (useful for debugging)."""
    print("=" * 60)
    print("Alexa Roomba Configuration")
    print("=" * 60)
    print(f"Serial Port:      {DEFAULT_PORT}")
    print(f"Baud Rate:        {DEFAULT_BAUD_RATE}")
    print(f"Device Name:      {FAUXMO_DEVICE_NAME}")
    print(f"Fauxmo Port:      {FAUXMO_PORT}")
    print(f"Operating Mode:   {DEFAULT_MODE}")
    print(f"Log Level:        {LOG_LEVEL_STR}")
    print(f"Install Dir:      {INSTALL_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    # When run directly, print configuration
    print_config()
