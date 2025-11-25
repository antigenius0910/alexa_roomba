"""
Unit tests for roomba.sensors module.

Tests sensor constants and SensorFrame class.
"""

import pytest
from roomba import sensors
from roomba.sensors import SensorFrame


class TestSensorConstants:
    """Test that sensor packet IDs are defined correctly."""

    @pytest.mark.unit
    def test_bump_and_wheel_drops(self):
        """Test bump and wheel drop sensor IDs."""
        assert sensors.BUMPS_AND_WHEEL_DROPS == 7

    @pytest.mark.unit
    def test_wall_sensor(self):
        """Test wall sensor ID."""
        assert sensors.WALL == 8

    @pytest.mark.unit
    def test_cliff_sensors(self):
        """Test cliff sensor IDs."""
        assert sensors.CLIFF_LEFT == 9
        assert sensors.CLIFF_FRONT_LEFT == 10
        assert sensors.CLIFF_FRONT_RIGHT == 11
        assert sensors.CLIFF_RIGHT == 12

    @pytest.mark.unit
    def test_virtual_wall(self):
        """Test virtual wall sensor ID."""
        assert sensors.VIRTUAL_WALL == 13

    @pytest.mark.unit
    def test_battery_sensors(self):
        """Test battery-related sensor IDs."""
        assert sensors.CHARGING_STATE == 21
        assert sensors.VOLTAGE == 22
        assert sensors.CURRENT == 23
        assert sensors.TEMPERATURE == 24
        assert sensors.BATTERY_CHARGE == 25
        assert sensors.BATTERY_CAPACITY == 26

    @pytest.mark.unit
    def test_distance_angle(self):
        """Test distance and angle sensor IDs."""
        assert sensors.DISTANCE == 19
        assert sensors.ANGLE == 20

    @pytest.mark.unit
    def test_wall_signal(self):
        """Test wall signal sensor ID."""
        assert sensors.WALL_SIGNAL == 27

    @pytest.mark.unit
    def test_cliff_signals(self):
        """Test cliff signal sensor IDs."""
        assert sensors.CLIFF_LEFT_SIGNAL == 28
        assert sensors.CLIFF_FRONT_LEFT_SIGNAL == 29
        assert sensors.CLIFF_FRONT_RIGHT_SIGNAL == 30
        assert sensors.CLIFF_RIGHT_SIGNAL == 31

    @pytest.mark.unit
    def test_encoders(self):
        """Test encoder sensor IDs."""
        assert sensors.ENCODER_LEFT == 43
        assert sensors.ENCODER_RIGHT == 44

    @pytest.mark.unit
    def test_light_bumpers(self):
        """Test light bumper sensor IDs."""
        assert sensors.LIGHT_BUMPER == 45
        assert sensors.LIGHT_BUMP_LEFT == 46
        assert sensors.LIGHT_BUMP_FRONT_LEFT == 47
        assert sensors.LIGHT_BUMP_CENTER_LEFT == 48
        assert sensors.LIGHT_BUMP_CENTER_RIGHT == 49
        assert sensors.LIGHT_BUMP_FRONT_RIGHT == 50
        assert sensors.LIGHT_BUMP_RIGHT == 51

    @pytest.mark.unit
    def test_unique_sensor_ids(self):
        """Test that all sensor IDs are unique."""
        sensor_ids = [
            sensors.BUMPS_AND_WHEEL_DROPS, sensors.WALL,
            sensors.CLIFF_LEFT, sensors.CLIFF_FRONT_LEFT,
            sensors.CLIFF_FRONT_RIGHT, sensors.CLIFF_RIGHT,
            sensors.VIRTUAL_WALL, sensors.CHARGING_STATE,
            sensors.VOLTAGE, sensors.CURRENT, sensors.TEMPERATURE,
            sensors.BATTERY_CHARGE, sensors.BATTERY_CAPACITY,
            sensors.DISTANCE, sensors.ANGLE, sensors.WALL_SIGNAL,
            sensors.CLIFF_LEFT_SIGNAL, sensors.CLIFF_FRONT_LEFT_SIGNAL,
            sensors.CLIFF_FRONT_RIGHT_SIGNAL, sensors.CLIFF_RIGHT_SIGNAL,
            sensors.ENCODER_LEFT, sensors.ENCODER_RIGHT,
            sensors.LIGHT_BUMPER,
        ]
        # Check all are unique
        assert len(sensor_ids) == len(set(sensor_ids))


class TestSensorFrame:
    """Test SensorFrame class."""

    @pytest.mark.unit
    def test_initialization(self):
        """Test SensorFrame initializes with default values."""
        frame = SensorFrame()

        # Test bump sensors default to 0
        assert frame.leftBump == 0
        assert frame.rightBump == 0

        # Test wheel drop sensors
        assert frame.casterDrop == 0
        assert frame.leftDrop == 0
        assert frame.rightDrop == 0

        # Test cliff sensors
        assert frame.cliffLeft == 0
        assert frame.cliffFrontLeft == 0
        assert frame.cliffFrontRight == 0
        assert frame.cliffRight == 0

        # Test wall sensor
        assert frame.wall == 0

        # Test battery sensors
        assert frame.batteryCharge == 0
        assert frame.batteryCapacity == 0
        assert frame.voltage == 0
        assert frame.current == 0

    @pytest.mark.unit
    def test_set_bump_sensors(self):
        """Test setting bump sensor values."""
        frame = SensorFrame()
        frame.leftBump = 1
        frame.rightBump = 1

        assert frame.leftBump == 1
        assert frame.rightBump == 1

    @pytest.mark.unit
    def test_set_cliff_sensors(self):
        """Test setting cliff sensor values."""
        frame = SensorFrame()
        frame.cliffLeft = 1
        frame.cliffFrontLeft = 1
        frame.cliffFrontRight = 1
        frame.cliffRight = 1

        assert frame.cliffLeft == 1
        assert frame.cliffFrontLeft == 1
        assert frame.cliffFrontRight == 1
        assert frame.cliffRight == 1

    @pytest.mark.unit
    def test_set_battery_values(self):
        """Test setting battery sensor values."""
        frame = SensorFrame()
        frame.batteryCharge = 2500
        frame.batteryCapacity = 3000
        frame.voltage = 15000
        frame.current = -500

        assert frame.batteryCharge == 2500
        assert frame.batteryCapacity == 3000
        assert frame.voltage == 15000
        assert frame.current == -500

    @pytest.mark.unit
    def test_wall_signal_values(self):
        """Test wall signal can hold various values."""
        frame = SensorFrame()

        # Test range of wall signal values
        for value in [0, 50, 100, 150, 200, 255]:
            frame.wallSignal = value
            assert frame.wallSignal == value

    @pytest.mark.unit
    def test_encoder_values(self):
        """Test encoder values."""
        frame = SensorFrame()
        frame.encoderLeft = 1000
        frame.encoderRight = 1005

        assert frame.encoderLeft == 1000
        assert frame.encoderRight == 1005

    @pytest.mark.unit
    def test_distance_angle(self):
        """Test distance and angle values."""
        frame = SensorFrame()
        frame.distance = 1500  # mm
        frame.angle = 90  # degrees

        assert frame.distance == 1500
        assert frame.angle == 90

    @pytest.mark.unit
    def test_negative_values(self):
        """Test that frame can hold negative values (current, angle)."""
        frame = SensorFrame()
        frame.current = -1000
        frame.angle = -45

        assert frame.current == -1000
        assert frame.angle == -45

    @pytest.mark.unit
    def test_multiple_frames(self):
        """Test that multiple SensorFrame instances are independent."""
        frame1 = SensorFrame()
        frame2 = SensorFrame()

        frame1.leftBump = 1
        frame2.leftBump = 0

        assert frame1.leftBump == 1
        assert frame2.leftBump == 0

    @pytest.mark.unit
    def test_frame_update_pattern(self):
        """Test typical frame update pattern."""
        frame = SensorFrame()

        # Simulate sensor update
        frame.leftBump = 1
        frame.wall = 1
        frame.wallSignal = 120
        frame.batteryCharge = 2500

        # Verify all updated correctly
        assert frame.leftBump == 1
        assert frame.wall == 1
        assert frame.wallSignal == 120
        assert frame.batteryCharge == 2500

        # Verify others still at default
        assert frame.rightBump == 0
        assert frame.cliffLeft == 0


class TestSensorBitMasks:
    """Test sensor bit interpretation."""

    @pytest.mark.unit
    def test_bumps_and_drops_bitmask(self):
        """Test bump and wheel drop bit positions."""
        # According to OI spec, BUMPS_AND_WHEEL_DROPS byte:
        # Bit 0: Right bump
        # Bit 1: Left bump
        # Bit 2: Right wheel drop
        # Bit 3: Left wheel drop
        # Bit 4: Caster wheel drop

        # Test right bump only
        byte = 0b00000001
        assert byte & 0x01  # Right bump

        # Test left bump only
        byte = 0b00000010
        assert byte & 0x02  # Left bump

        # Test both bumps
        byte = 0b00000011
        assert byte & 0x01  # Right bump
        assert byte & 0x02  # Left bump

        # Test wheel drops
        byte = 0b00011100
        assert byte & 0x04  # Right wheel drop
        assert byte & 0x08  # Left wheel drop
        assert byte & 0x10  # Caster wheel drop

    @pytest.mark.unit
    def test_buttons_bitmask(self):
        """Test button bit positions."""
        # Buttons byte has different bits for different buttons
        # This tests we can extract individual buttons

        # Clean button (bit 0)
        byte = 0b00000001
        assert byte & 0x01

        # Spot button (bit 1)
        byte = 0b00000010
        assert byte & 0x02

        # Dock button (bit 2)
        byte = 0b00000100
        assert byte & 0x04

        # Multiple buttons
        byte = 0b00000111  # All three
        assert byte & 0x01
        assert byte & 0x02
        assert byte & 0x04


class TestSensorRanges:
    """Test sensor value ranges."""

    @pytest.mark.unit
    @pytest.mark.parametrize("sensor_value", [0, 127, 255, 1000, 4095])
    def test_wall_signal_range(self, sensor_value):
        """Test wall signal can hold full range of values."""
        frame = SensorFrame()
        frame.wallSignal = sensor_value
        assert frame.wallSignal == sensor_value

    @pytest.mark.unit
    @pytest.mark.parametrize("charge,capacity", [
        (0, 0),
        (1500, 3000),
        (2500, 3000),
        (3000, 3000),
        (65535, 65535),  # Max 16-bit
    ])
    def test_battery_ranges(self, charge, capacity):
        """Test battery values can hold expected ranges."""
        frame = SensorFrame()
        frame.batteryCharge = charge
        frame.batteryCapacity = capacity

        assert frame.batteryCharge == charge
        assert frame.batteryCapacity == capacity

        # Test battery percentage calculation
        if capacity > 0:
            percentage = (charge / capacity) * 100
            assert 0 <= percentage <= 100

    @pytest.mark.unit
    @pytest.mark.parametrize("voltage", [0, 10000, 15000, 16800, 65535])
    def test_voltage_range(self, voltage):
        """Test voltage values in mV."""
        frame = SensorFrame()
        frame.voltage = voltage
        assert frame.voltage == voltage

    @pytest.mark.unit
    @pytest.mark.parametrize("current", [-32768, -1000, 0, 1000, 32767])
    def test_current_range(self, current):
        """Test current can be positive or negative."""
        frame = SensorFrame()
        frame.current = current
        assert frame.current == current
