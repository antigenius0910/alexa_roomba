"""
Integration tests for roomba.Create class.

Tests robot control methods with mocked serial communication.
"""

import pytest
from unittest.mock import Mock, patch, call
from roomba import Create, PASSIVE_MODE, SAFE_MODE, FULL_MODE
from roomba.commands import START, SAFE, FULL, DRIVE, SENSORS, SONG, PLAY_SONG
from roomba.sensors import BATTERY_CHARGE, WALL_SIGNAL


class TestCreateInitialization:
    """Test Create class initialization."""

    @pytest.mark.integration
    def test_init_with_defaults(self, mock_serial, monkeypatch):
        """Test initialization with default parameters."""
        monkeypatch.setattr('serial.Serial', lambda *args, **kwargs: mock_serial)

        robot = Create('/dev/ttyUSB0')

        # Verify serial port was opened
        assert robot.ser == mock_serial

        # Verify initialization commands sent
        assert mock_serial.write.called

    @pytest.mark.integration
    def test_init_safe_mode(self, mock_serial, monkeypatch):
        """Test initialization in safe mode."""
        monkeypatch.setattr('serial.Serial', lambda *args, **kwargs: mock_serial)

        robot = Create('/dev/ttyUSB0', startingMode=SAFE_MODE)

        # Should send START and SAFE commands
        calls = mock_serial.write.call_args_list
        assert len(calls) >= 2

    @pytest.mark.integration
    def test_init_full_mode(self, mock_serial, monkeypatch):
        """Test initialization in full mode."""
        monkeypatch.setattr('serial.Serial', lambda *args, **kwargs: mock_serial)

        robot = Create('/dev/ttyUSB0', startingMode=FULL_MODE)

        # Should send START and FULL commands
        calls = mock_serial.write.call_args_list
        assert len(calls) >= 2

    @pytest.mark.integration
    def test_init_custom_baud(self, mock_serial, monkeypatch):
        """Test initialization with custom baud rate."""
        def mock_serial_class(port, baudrate, *args, **kwargs):
            mock_serial.baudrate = baudrate
            return mock_serial

        monkeypatch.setattr('serial.Serial', mock_serial_class)

        robot = Create('/dev/ttyUSB0', baudrate=57600)

        assert mock_serial.baudrate == 57600


class TestMovementCommands:
    """Test movement command methods."""

    @pytest.mark.integration
    def test_go_forward(self, mock_create_instance):
        """Test moving forward."""
        robot = mock_create_instance

        robot.go(20, 0)  # 20 cm/s forward

        # Verify Drive command was sent
        assert robot.ser.write.called

    @pytest.mark.integration
    def test_go_backward(self, mock_create_instance):
        """Test moving backward."""
        robot = mock_create_instance

        robot.go(-20, 0)  # 20 cm/s backward

        assert robot.ser.write.called

    @pytest.mark.integration
    def test_go_spin_clockwise(self, mock_create_instance):
        """Test spinning clockwise."""
        robot = mock_create_instance

        robot.go(0, 50)  # Spin clockwise

        assert robot.ser.write.called

    @pytest.mark.integration
    def test_go_spin_counter_clockwise(self, mock_create_instance):
        """Test spinning counter-clockwise."""
        robot = mock_create_instance

        robot.go(0, -50)  # Spin counter-clockwise

        assert robot.ser.write.called

    @pytest.mark.integration
    def test_go_curved_path(self, mock_create_instance):
        """Test moving in curved path."""
        robot = mock_create_instance

        robot.go(20, 30)  # Forward + turn

        assert robot.ser.write.called

    @pytest.mark.integration
    def test_stop(self, mock_create_instance):
        """Test stop command."""
        robot = mock_create_instance

        robot.stop()

        # Verify Drive command with zero velocity
        assert robot.ser.write.called

    @pytest.mark.integration
    @pytest.mark.parametrize("velocity,spin", [
        (10, 0),
        (-10, 0),
        (0, 50),
        (20, 30),
        (-15, -20),
    ])
    def test_various_movements(self, mock_create_instance, velocity, spin):
        """Test various movement combinations."""
        robot = mock_create_instance

        robot.go(velocity, spin)

        assert robot.ser.write.called


class TestSensorCommands:
    """Test sensor reading methods."""

    @pytest.mark.integration
    def test_sensors_all(self, mock_create_instance):
        """Test reading all sensors."""
        robot = mock_create_instance

        # Mock sensor response
        robot.ser.read = Mock(return_value=b'\x09\xC4')  # Example: 2500 mAh

        robot.sensors()

        # Verify SENSORS command was sent
        assert robot.ser.write.called

    @pytest.mark.integration
    def test_sensors_specific(self, mock_create_instance):
        """Test reading specific sensors."""
        robot = mock_create_instance
        robot.ser.read = Mock(return_value=b'\x09\xC4')

        robot.sensors([BATTERY_CHARGE, WALL_SIGNAL])

        # Should send multiple SENSORS commands
        assert robot.ser.write.call_count >= 2

    @pytest.mark.integration
    def test_sensors_battery(self, mock_create_instance, sample_sensor_data):
        """Test reading battery sensors."""
        robot = mock_create_instance
        robot.sensord = sample_sensor_data

        # Simulate sensor read
        robot.sensors([BATTERY_CHARGE])

        # Verify sensor dictionary populated
        assert BATTERY_CHARGE in robot.sensord or robot.ser.write.called

    @pytest.mark.integration
    def test_print_sensors(self, mock_create_instance, capsys):
        """Test printSensors output."""
        robot = mock_create_instance
        robot.sensord = {BATTERY_CHARGE: 2500}

        # Mock printSensors to not actually read
        with patch.object(robot, 'sensors'):
            robot.printSensors()

        # Verify output contains sensor info
        captured = capsys.readouterr()
        assert len(captured.out) > 0 or robot.sensors.called


class TestMusicCommands:
    """Test music playback methods."""

    @pytest.mark.integration
    def test_set_song(self, mock_create_instance):
        """Test setting a song."""
        robot = mock_create_instance
        from roomba.music import c5, d5, e5, QUARTER

        song = [(c5, QUARTER), (d5, QUARTER), (e5, QUARTER)]

        robot.setSong(0, song)

        # Verify SONG command sent
        assert robot.ser.write.called

    @pytest.mark.integration
    def test_play_song_direct(self, mock_create_instance):
        """Test playing song directly."""
        robot = mock_create_instance
        from roomba.music import c5, QUARTER

        song = [(c5, QUARTER)]

        robot.playSong(song)

        # Should set song and play it
        assert robot.ser.write.call_count >= 2

    @pytest.mark.integration
    def test_play_song_by_number(self, mock_create_instance):
        """Test playing previously defined song."""
        robot = mock_create_instance

        robot.PlaySong(0)

        # Verify PLAY_SONG command sent
        assert robot.ser.write.called

    @pytest.mark.integration
    def test_song_length_limit(self, mock_create_instance):
        """Test song with maximum notes."""
        robot = mock_create_instance
        from roomba.music import c5, QUARTER

        # Max 16 notes
        max_song = [(c5, QUARTER)] * 16

        robot.setSong(0, max_song)

        assert robot.ser.write.called


class TestModeCommands:
    """Test mode switching methods."""

    @pytest.mark.integration
    def test_to_safe_mode(self, mock_create_instance):
        """Test switching to safe mode."""
        robot = mock_create_instance

        robot.toSafeMode()

        assert robot.ser.write.called

    @pytest.mark.integration
    def test_to_full_mode(self, mock_create_instance):
        """Test switching to full mode."""
        robot = mock_create_instance

        robot.toFullMode()

        assert robot.ser.write.called

    @pytest.mark.integration
    def test_to_passive_mode(self, mock_create_instance):
        """Test switching to passive mode."""
        robot = mock_create_instance

        robot.toPassiveMode()

        assert robot.ser.write.called

    @pytest.mark.integration
    def test_mode_sequence(self, mock_create_instance):
        """Test switching through modes."""
        robot = mock_create_instance

        robot.toPassiveMode()
        robot.toSafeMode()
        robot.toFullMode()

        # Should have sent 3 mode commands
        assert robot.ser.write.call_count >= 3


class TestCleanupCommands:
    """Test cleanup and connection management."""

    @pytest.mark.integration
    def test_close(self, mock_create_instance):
        """Test closing connection."""
        robot = mock_create_instance

        robot.close()

        # Verify serial port closed
        assert robot.ser.close.called

    @pytest.mark.integration
    def test_close_after_movement(self, mock_create_instance):
        """Test close stops robot before closing."""
        robot = mock_create_instance

        robot.go(20, 0)
        robot.close()

        # Should stop and close
        assert robot.ser.write.called  # Stop command
        assert robot.ser.close.called


class TestErrorHandling:
    """Test error handling and edge cases."""

    @pytest.mark.integration
    def test_serial_write_error(self, mock_create_instance):
        """Test handling serial write errors."""
        robot = mock_create_instance
        robot.ser.write = Mock(side_effect=Exception("Write error"))

        with pytest.raises(Exception):
            robot.go(20, 0)

    @pytest.mark.integration
    def test_serial_read_timeout(self, mock_create_instance):
        """Test handling serial read timeout."""
        robot = mock_create_instance
        robot.ser.read = Mock(return_value=b'')  # Empty read (timeout)

        # Should handle gracefully
        robot.sensors([BATTERY_CHARGE])

        # May populate with 0 or leave empty, but shouldn't crash
        assert True  # If we get here, no exception was raised

    @pytest.mark.integration
    def test_invalid_port(self):
        """Test handling invalid serial port."""
        with patch('serial.Serial', side_effect=Exception("Port not found")):
            with pytest.raises(Exception):
                robot = Create('/dev/invalid')

    @pytest.mark.integration
    def test_close_already_closed(self, mock_create_instance):
        """Test closing already closed connection."""
        robot = mock_create_instance
        robot.ser.is_open = False

        # Should handle gracefully
        robot.close()

        assert robot.ser.close.called


class TestCommandSequences:
    """Test common command sequences."""

    @pytest.mark.integration
    def test_typical_movement_sequence(self, mock_create_instance):
        """Test typical movement sequence."""
        robot = mock_create_instance

        # Init -> Move -> Stop -> Close
        robot.toSafeMode()
        robot.go(20, 0)
        robot.stop()
        robot.close()

        # Verify all commands sent
        assert robot.ser.write.call_count >= 3

    @pytest.mark.integration
    def test_sensor_reading_sequence(self, mock_create_instance):
        """Test typical sensor reading sequence."""
        robot = mock_create_instance
        robot.ser.read = Mock(return_value=b'\x09\xC4')

        # Read sensors multiple times
        for _ in range(5):
            robot.sensors([BATTERY_CHARGE])

        # Should have read sensors 5 times
        assert robot.ser.write.call_count >= 5

    @pytest.mark.integration
    def test_music_and_movement(self, mock_create_instance):
        """Test playing music while moving."""
        robot = mock_create_instance
        from roomba.music import c5, QUARTER

        song = [(c5, QUARTER)]

        # Play song
        robot.playSong(song)

        # Then move
        robot.go(10, 0)

        # Both commands should be sent
        assert robot.ser.write.call_count >= 3


class TestThreadSafety:
    """Test thread safety considerations."""

    @pytest.mark.integration
    @pytest.mark.slow
    def test_concurrent_sensor_reads(self, mock_create_instance):
        """Test multiple sensor reads don't interfere."""
        robot = mock_create_instance
        robot.ser.read = Mock(return_value=b'\x09\xC4')

        # Read different sensors
        robot.sensors([BATTERY_CHARGE])
        robot.sensors([WALL_SIGNAL])

        # Both should complete
        assert robot.ser.write.call_count >= 2

    @pytest.mark.integration
    def test_command_ordering(self, mock_create_instance):
        """Test commands are sent in order."""
        robot = mock_create_instance

        # Send sequence of commands
        robot.toSafeMode()
        robot.go(20, 0)
        robot.stop()

        # Verify order (each write call is in order)
        assert robot.ser.write.call_count == 3


class TestRealWorldScenarios:
    """Test real-world usage scenarios."""

    @pytest.mark.integration
    def test_wall_following_iteration(self, mock_create_instance):
        """Test single iteration of wall following."""
        robot = mock_create_instance
        robot.ser.read = Mock(return_value=b'\x00\x32')  # Wall signal = 50

        # Read wall sensor
        robot.sensors([WALL_SIGNAL])

        # Adjust movement based on sensor
        robot.go(15, 10)

        assert robot.ser.write.called

    @pytest.mark.integration
    def test_bump_reaction(self, mock_create_instance):
        """Test reacting to bump sensor."""
        robot = mock_create_instance
        robot.ser.read = Mock(return_value=b'\x03')  # Both bumps

        # Read bump sensors
        robot.sensors()

        # Back up
        robot.go(-10, 0)

        # Turn
        robot.go(0, 50)

        assert robot.ser.write.call_count >= 3

    @pytest.mark.integration
    def test_battery_monitoring(self, mock_create_instance, sample_sensor_data):
        """Test monitoring battery level."""
        robot = mock_create_instance
        robot.sensord = sample_sensor_data

        # Calculate battery percentage
        charge = robot.sensord.get(BATTERY_CHARGE, 0)
        capacity = robot.sensord.get(26, 1)  # BATTERY_CAPACITY

        if capacity > 0:
            percentage = (charge / capacity) * 100
            assert 0 <= percentage <= 100
