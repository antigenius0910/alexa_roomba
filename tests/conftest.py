"""
Pytest configuration and shared fixtures.

This module provides fixtures for testing without actual hardware:
- Mock serial ports
- Sample sensor data
- Test configurations
"""

import pytest
from unittest.mock import Mock, MagicMock
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture
def mock_serial():
    """
    Mock serial port for testing without hardware.

    Returns:
        Mock: Configured mock serial object
    """
    serial_mock = Mock()
    serial_mock.is_open = True
    serial_mock.write = Mock(return_value=None)
    serial_mock.read = Mock(return_value=b'\x00')
    serial_mock.close = Mock()
    serial_mock.in_waiting = 0
    serial_mock.timeout = 0.5
    serial_mock.baudrate = 115200
    serial_mock.port = '/dev/ttyUSB0'
    return serial_mock


@pytest.fixture
def sample_sensor_data():
    """
    Sample sensor data for testing.

    Returns:
        dict: Dictionary of sensor ID to value mappings
    """
    from roomba.sensors import (
        BATTERY_CHARGE, BATTERY_CAPACITY, VOLTAGE,
        WALL_SIGNAL, BUMPS_AND_WHEEL_DROPS,
        CLIFF_LEFT, ENCODER_LEFT, ENCODER_RIGHT
    )

    return {
        BATTERY_CHARGE: 2500,
        BATTERY_CAPACITY: 3000,
        VOLTAGE: 15000,
        WALL_SIGNAL: 50,
        BUMPS_AND_WHEEL_DROPS: 0,
        CLIFF_LEFT: 0,
        ENCODER_LEFT: 1000,
        ENCODER_RIGHT: 1005,
    }


@pytest.fixture
def mock_create_instance(mock_serial, monkeypatch):
    """
    Create a Create instance with mocked serial port.

    Args:
        mock_serial: Mock serial fixture
        monkeypatch: Pytest monkeypatch fixture

    Returns:
        Create: Create instance with mocked serial
    """
    # Mock serial.Serial to return our mock
    def mock_serial_class(*args, **kwargs):
        return mock_serial

    monkeypatch.setattr('serial.Serial', mock_serial_class)

    # Import after patching
    from roomba import Create, PASSIVE_MODE

    robot = Create.__new__(Create)
    robot.ser = mock_serial
    robot.sensord = {}
    robot.mode = PASSIVE_MODE
    robot.opcodes = {}

    return robot


@pytest.fixture
def temp_config_file(tmp_path):
    """
    Create temporary .env file for config testing.

    Args:
        tmp_path: Pytest temporary directory

    Returns:
        Path: Path to temporary .env file
    """
    config_file = tmp_path / ".env"
    config_content = """
# Test configuration
ROOMBA_PORT=/dev/ttyUSB0
ROOMBA_BAUD_RATE=115200
FAUXMO_DEVICE_NAME=Test Device
FAUXMO_PORT=52000
LOG_LEVEL=DEBUG
"""
    config_file.write_text(config_content.strip())
    return config_file
