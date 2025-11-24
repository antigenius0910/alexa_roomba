"""
Sensor constants and data structures for iRobot Create/Roomba.

This module defines all sensor packet IDs and provides the SensorFrame class
for organizing sensor data returned from the robot.
"""

import math
from .utils import _toTwosComplement2Bytes

# Sensor packet IDs
BUMPS_AND_WHEEL_DROPS = 7
WALL_IR_SENSOR = 8
CLIFF_LEFT = 9
CLIFF_FRONT_LEFT = 10
CLIFF_FRONT_RIGHT = 11
CLIFF_RIGHT = 12
VIRTUAL_WALL = 13
LSD_AND_OVERCURRENTS = 14
DIRT_DETECTED = 15
INFRARED_BYTE = 17
BUTTONS = 18
DISTANCE = 19
ANGLE = 20
CHARGING_STATE = 21
VOLTAGE = 22
CURRENT = 23
BATTERY_TEMP = 24
BATTERY_CHARGE = 25
BATTERY_CAPACITY = 26
WALL_SIGNAL = 27
CLIFF_LEFT_SIGNAL = 28
CLIFF_FRONT_LEFT_SIGNAL = 29
CLIFF_FRONT_RIGHT_SIGNAL = 30
CLIFF_RIGHT_SIGNAL = 31
CARGO_BAY_DIGITAL_INPUTS = 32
CARGO_BAY_ANALOG_SIGNAL = 33
CHARGING_SOURCES_AVAILABLE = 34
OI_MODE = 35
SONG_NUMBER = 36
SONG_PLAYING = 37
NUM_STREAM_PACKETS = 38
REQUESTED_VELOCITY = 39
REQUESTED_RADIUS = 40
REQUESTED_RIGHT_VELOCITY = 41
REQUESTED_LEFT_VELOCITY = 42
ENCODER_LEFT = 43
ENCODER_RIGHT = 44
LIGHTBUMP = 45
LIGHTBUMP_LEFT = 46
LIGHTBUMP_FRONT_LEFT = 47
LIGHTBUMP_CENTER_LEFT = 48
LIGHTBUMP_CENTER_RIGHT = 49
LIGHTBUMP_FRONT_RIGHT = 50
LIGHTBUMP_RIGHT = 51

# Derived sensor IDs for easy access to specific data
POSE = 100
LEFT_BUMP = 101
RIGHT_BUMP = 102
LEFT_WHEEL_DROP = 103
RIGHT_WHEEL_DROP = 104
CENTER_WHEEL_DROP = 105
LEFT_WHEEL_OVERCURRENT = 106
RIGHT_WHEEL_OVERCURRENT = 107
ADVANCE_BUTTON = 108
PLAY_BUTTON = 109

# Sensor data widths (in bytes) for each sensor packet
SENSOR_DATA_WIDTH = [
    0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2,
    1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 1, 2, 1, 1, 1, 1, 1, 2, 2,
    2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2
]

# Physical constants for odometry calculations
# The original value was 258.0 but adjusted for specific Roomba model
WHEEL_SPAN = 235.0  # Distance between wheels in mm
WHEEL_DIAMETER = 72.0  # Wheel diameter in mm
TICK_PER_REVOLUTION = 508.8  # Encoder ticks per wheel revolution
TICK_PER_MM = TICK_PER_REVOLUTION / (math.pi * WHEEL_DIAMETER)

# Angular error correction factor (calibrated for specific floor type)
# On some floors, a full turn is measured as ~450 degrees instead of 360
ANGULAR_ERROR = 360.0 / 450.0


class SensorFrame:
    """
    Data structure for organizing sensor readings from the Roomba.

    This class acts as a struct whose fields are filled in by sensor queries.
    All fields are initialized to 0 and updated when sensor data is read.
    """

    def __init__(self):
        """Initialize all sensor fields to 0."""
        # Bumps and wheel drops
        self.casterDrop = 0
        self.leftWheelDrop = 0
        self.rightWheelDrop = 0
        self.leftBump = 0
        self.rightBump = 0

        # Cliff sensors
        self.wallSensor = 0
        self.leftCliff = 0
        self.frontLeftCliff = 0
        self.frontRightCliff = 0
        self.rightCliff = 0
        self.virtualWall = 0

        # Motor status
        self.driveLeft = 0
        self.driveRight = 0
        self.mainBrush = 0
        self.vacuum = 0
        self.sideBrush = 0

        # Dirt detection
        self.leftDirt = 0
        self.rightDirt = 0
        self.dirt = 0

        # Control and buttons
        self.remoteControlCommand = 0
        self.powerButton = 0
        self.spotButton = 0
        self.cleanButton = 0
        self.maxButton = 0

        # Motion and position
        self.distance = 0
        self.rawAngle = 0
        self.angleInRadians = 0

        # Power and charging
        self.chargingState = 0
        self.voltage = 0
        self.current = 0
        self.temperature = 0
        self.charge = 0
        self.capacity = 0

        # Light bump sensors
        self.lightBumpLeft = 0
        self.lightBumpFrontLeft = 0
        self.lightCenterLeft = 0
        self.lightCenterRight = 0
        self.lightBumpFrontRight = 0
        self.lightBumpRight = 0

    def __str__(self):
        """Return a string representation of all sensor values."""
        lines = [
            f'casterDrop: {self.casterDrop}',
            f'leftWheelDrop: {self.leftWheelDrop}',
            f'rightWheelDrop: {self.rightWheelDrop}',
            f'leftBump: {self.leftBump}',
            f'rightBump: {self.rightBump}',
            f'wallSensor: {self.wallSensor}',
            f'leftCliff: {self.leftCliff}',
            f'frontLeftCliff: {self.frontLeftCliff}',
            f'frontRightCliff: {self.frontRightCliff}',
            f'rightCliff: {self.rightCliff}',
            f'virtualWall: {self.virtualWall}',
            f'driveLeft: {self.driveLeft}',
            f'driveRight: {self.driveRight}',
            f'mainBrush: {self.mainBrush}',
            f'vacuum: {self.vacuum}',
            f'sideBrush: {self.sideBrush}',
            f'leftDirt: {self.leftDirt}',
            f'rightDirt: {self.rightDirt}',
            f'remoteControlCommand: {self.remoteControlCommand}',
            f'powerButton: {self.powerButton}',
            f'spotButton: {self.spotButton}',
            f'cleanButton: {self.cleanButton}',
            f'maxButton: {self.maxButton}',
            f'distance: {self.distance}',
            f'rawAngle: {self.rawAngle}',
            f'angleInRadians: {self.angleInRadians}',
            f'angleInDegrees: {math.degrees(self.angleInRadians)}',
            f'chargingState: {self.chargingState}',
            f'voltage: {self.voltage}',
            f'current: {self.current}',
            f'temperature: {self.temperature}',
            f'charge: {self.charge}',
            f'capacity: {self.capacity}',
        ]
        return '\\n'.join(lines)

    def _toBinaryString(self):
        """
        Convert the SensorFrame into a 26-byte binary string.

        This matches the format the Roomba sends back for sensor data.
        Used primarily for testing and simulation.

        Returns:
            bytes: 26-byte representation of sensor data
        """
        slist = [0] * 26

        # First Frame - Bumps and sensors
        slist[0] = (self.casterDrop << 4 | self.leftWheelDrop << 3 |
                    self.rightWheelDrop << 2 | self.leftBump << 1 |
                    self.rightBump)
        slist[1] = self.wallSensor
        slist[2] = self.leftCliff
        slist[3] = self.frontLeftCliff
        slist[4] = self.frontRightCliff
        slist[5] = self.rightCliff
        slist[6] = self.virtualWall
        slist[7] = (self.driveLeft << 4 | self.driveRight << 3 |
                    self.mainBrush << 2 | self.vacuum << 1 |
                    self.sideBrush)
        slist[8] = self.leftDirt
        slist[9] = self.rightDirt

        # Second Frame - Control and motion
        slist[10] = self.remoteControlCommand
        slist[11] = (self.powerButton << 3 | self.spotButton << 2 |
                     self.cleanButton << 1 | self.maxButton)

        highVal, lowVal = _toTwosComplement2Bytes(self.distance)
        slist[12] = highVal
        slist[13] = lowVal

        highVal, lowVal = _toTwosComplement2Bytes(self.rawAngle)
        slist[14] = highVal
        slist[15] = lowVal

        # Third Frame - Power and battery
        slist[16] = self.chargingState
        slist[17] = (self.voltage >> 8) & 0xFF
        slist[18] = self.voltage & 0xFF

        highVal, lowVal = _toTwosComplement2Bytes(self.current)
        slist[19] = highVal
        slist[20] = lowVal

        slist[21] = self.temperature
        slist[22] = (self.charge >> 8) & 0xFF
        slist[23] = self.charge & 0xFF
        slist[24] = (self.capacity >> 8) & 0xFF
        slist[25] = self.capacity & 0xFF

        return bytes(slist)
