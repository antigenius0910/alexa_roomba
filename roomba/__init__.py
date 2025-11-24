"""
Roomba Control Package

A modular Python interface for controlling iRobot Create/Roomba robots via serial communication.

This package provides:
- Command opcodes for the Open Interface protocol
- Sensor data structures and constants
- Music/MIDI note definitions
- Utility functions for data manipulation
- Main robot control interface (Create class)

Example:
    from roomba import Create
    from roomba.commands import SAFE_MODE

    robot = Create('/dev/ttyUSB0')
    robot.toSafeMode()
    robot.go(30, 0)  # Move forward at 30 cm/s
    robot.close()
"""

# Import all public constants and classes from submodules
from .commands import *
from .sensors import *
from .music import *
from .utils import mode_to_string, _bit_of_byte
from .robot import Create

__version__ = '2.0.0'
__author__ = 'Zach Dodds, Sean Luke, James O\'Beirne, Martin Schaef'

# Define public API
__all__ = [
    # Main robot class
    'Create',

    # Command constants (from commands.py)
    'START', 'BAUD', 'CONTROL', 'SAFE', 'FULL', 'POWER',
    'SPOT', 'CLEAN', 'COVER', 'MAX', 'DEMO',
    'DRIVE', 'DRIVEDIRECT', 'MOTORS', 'LEDS',
    'SONG', 'PLAY', 'SENSORS', 'QUERYLIST', 'STREAM',
    'FORCESEEKINGDOCK', 'SCRIPT', 'ENDSCRIPT',
    'WAITDIST', 'WAITANGLE', 'PAUSERESUME',
    'OFF_MODE', 'PASSIVE_MODE', 'SAFE_MODE', 'FULL_MODE',

    # Sensor constants (from sensors.py)
    'BUMPS_AND_WHEEL_DROPS', 'WALL_IR_SENSOR', 'CLIFF_LEFT',
    'CLIFF_FRONT_LEFT', 'CLIFF_FRONT_RIGHT', 'CLIFF_RIGHT',
    'VIRTUAL_WALL', 'DISTANCE', 'ANGLE', 'CHARGING_STATE',
    'VOLTAGE', 'CURRENT', 'BATTERY_TEMP', 'BATTERY_CHARGE',
    'BATTERY_CAPACITY', 'WALL_SIGNAL', 'ENCODER_LEFT', 'ENCODER_RIGHT',
    'LIGHTBUMP', 'LIGHTBUMP_LEFT', 'LIGHTBUMP_FRONT_LEFT',
    'LIGHTBUMP_CENTER_LEFT', 'LIGHTBUMP_CENTER_RIGHT',
    'LIGHTBUMP_FRONT_RIGHT', 'LIGHTBUMP_RIGHT',
    'POSE', 'LEFT_BUMP', 'RIGHT_BUMP',
    'SENSOR_DATA_WIDTH', 'WHEEL_SPAN', 'WHEEL_DIAMETER',
    'SensorFrame',

    # Music constants (from music.py)
    'REST', 'c4', 'd4', 'e4', 'f4', 'g4', 'a4', 'b4',
    'c5', 'd5', 'e5', 'f5', 'g5', 'a5', 'b5',
    'c6', 'd6', 'e6', 'f6',
    'MEASURE', 'HALF', 'QUARTER', 'EIGHTH', 'SIXTEENTH',
    'MEASURE_TIME',

    # Utility functions
    'mode_to_string',
]
