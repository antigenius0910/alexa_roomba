"""
Unit tests for roomba.utils module.

Tests utility functions for bit operations, conversions, and mode strings.
"""

import pytest
from roomba.utils import (
    mode_to_string, _bit_of_byte, _toTwosComplement2Bytes,
    _toUnsignedBytes, _get_signed_integer_from_bytes
)
from roomba import OFF_MODE, PASSIVE_MODE, SAFE_MODE, FULL_MODE


class TestModeToString:
    """Test mode_to_string function."""

    @pytest.mark.unit
    def test_off_mode(self):
        """Test OFF_MODE conversion."""
        assert mode_to_string(OFF_MODE) == 'OFF_MODE'

    @pytest.mark.unit
    def test_passive_mode(self):
        """Test PASSIVE_MODE conversion."""
        assert mode_to_string(PASSIVE_MODE) == 'PASSIVE_MODE'

    @pytest.mark.unit
    def test_safe_mode(self):
        """Test SAFE_MODE conversion."""
        assert mode_to_string(SAFE_MODE) == 'SAFE_MODE'

    @pytest.mark.unit
    def test_full_mode(self):
        """Test FULL_MODE conversion."""
        assert mode_to_string(FULL_MODE) == 'FULL_MODE'

    @pytest.mark.unit
    def test_unknown_mode(self):
        """Test unknown mode returns UNKNOWN_MODE."""
        assert mode_to_string(99) == 'UNKNOWN_MODE'

    @pytest.mark.unit
    def test_negative_mode(self):
        """Test negative mode value."""
        assert mode_to_string(-1) == 'UNKNOWN_MODE'


class TestBitOfByte:
    """Test _bit_of_byte function."""

    @pytest.mark.unit
    def test_bit_0(self):
        """Test extracting bit 0."""
        assert _bit_of_byte(0b00000001, 0) == 1
        assert _bit_of_byte(0b00000000, 0) == 0

    @pytest.mark.unit
    def test_bit_7(self):
        """Test extracting bit 7."""
        assert _bit_of_byte(0b10000000, 7) == 1
        assert _bit_of_byte(0b01111111, 7) == 0

    @pytest.mark.unit
    def test_bit_middle(self):
        """Test extracting middle bits."""
        assert _bit_of_byte(0b00001000, 3) == 1
        assert _bit_of_byte(0b00010000, 4) == 1

    @pytest.mark.unit
    def test_all_bits_set(self):
        """Test extracting from byte with all bits set."""
        byte = 0xFF
        for bit in range(8):
            assert _bit_of_byte(byte, bit) == 1

    @pytest.mark.unit
    def test_no_bits_set(self):
        """Test extracting from byte with no bits set."""
        byte = 0x00
        for bit in range(8):
            assert _bit_of_byte(byte, bit) == 0

    @pytest.mark.unit
    @pytest.mark.parametrize("byte,bit,expected", [
        (0b10101010, 1, 1),
        (0b10101010, 0, 0),
        (0b01010101, 1, 0),
        (0b01010101, 0, 1),
    ])
    def test_alternating_pattern(self, byte, bit, expected):
        """Test extracting from alternating bit patterns."""
        assert _bit_of_byte(byte, bit) == expected


class TestTwosComplement:
    """Test _toTwosComplement2Bytes function."""

    @pytest.mark.unit
    def test_positive_zero(self):
        """Test zero value."""
        high, low = _toTwosComplement2Bytes(0)
        assert high == 0
        assert low == 0

    @pytest.mark.unit
    def test_positive_one(self):
        """Test positive one."""
        high, low = _toTwosComplement2Bytes(1)
        assert high == 0
        assert low == 1

    @pytest.mark.unit
    def test_positive_255(self):
        """Test maximum single byte positive."""
        high, low = _toTwosComplement2Bytes(255)
        assert high == 0
        assert low == 255

    @pytest.mark.unit
    def test_positive_256(self):
        """Test value requiring high byte."""
        high, low = _toTwosComplement2Bytes(256)
        assert high == 1
        assert low == 0

    @pytest.mark.unit
    def test_positive_500(self):
        """Test typical positive velocity (500 mm/s)."""
        high, low = _toTwosComplement2Bytes(500)
        assert high == 1
        assert low == 244  # 500 = 256 + 244

    @pytest.mark.unit
    def test_negative_one(self):
        """Test negative one in two's complement."""
        high, low = _toTwosComplement2Bytes(-1)
        assert high == 255
        assert low == 255

    @pytest.mark.unit
    def test_negative_256(self):
        """Test -256 in two's complement."""
        high, low = _toTwosComplement2Bytes(-256)
        assert high == 255
        assert low == 0

    @pytest.mark.unit
    def test_negative_500(self):
        """Test typical negative velocity (-500 mm/s)."""
        high, low = _toTwosComplement2Bytes(-500)
        # -500 in 16-bit two's complement is 65036
        expected_value = (1 << 16) - 500
        assert (high << 8) | low == expected_value

    @pytest.mark.unit
    def test_max_positive(self):
        """Test maximum positive 16-bit value."""
        high, low = _toTwosComplement2Bytes(32767)
        assert high == 127
        assert low == 255

    @pytest.mark.unit
    def test_max_negative(self):
        """Test minimum negative 16-bit value."""
        high, low = _toTwosComplement2Bytes(-32768)
        assert high == 128
        assert low == 0


class TestUnsignedBytes:
    """Test _toUnsignedBytes function."""

    @pytest.mark.unit
    def test_zero(self):
        """Test zero value."""
        high, low = _toUnsignedBytes(0)
        assert high == 0
        assert low == 0

    @pytest.mark.unit
    def test_255(self):
        """Test maximum single byte."""
        high, low = _toUnsignedBytes(255)
        assert high == 0
        assert low == 255

    @pytest.mark.unit
    def test_256(self):
        """Test first two-byte value."""
        high, low = _toUnsignedBytes(256)
        assert high == 1
        assert low == 0

    @pytest.mark.unit
    def test_65535(self):
        """Test maximum 16-bit unsigned value."""
        high, low = _toUnsignedBytes(65535)
        assert high == 255
        assert low == 255

    @pytest.mark.unit
    @pytest.mark.parametrize("value,expected_high,expected_low", [
        (1000, 3, 232),  # 1000 = 3*256 + 232
        (2500, 9, 196),  # 2500 = 9*256 + 196
        (3000, 11, 184), # 3000 = 11*256 + 184
    ])
    def test_typical_battery_values(self, value, expected_high, expected_low):
        """Test values typical for battery charge/capacity."""
        high, low = _toUnsignedBytes(value)
        assert high == expected_high
        assert low == expected_low


class TestGetSignedInteger:
    """Test _get_signed_integer_from_bytes function."""

    @pytest.mark.unit
    def test_positive_zero(self):
        """Test zero from two bytes."""
        value = _get_signed_integer_from_bytes(0, 0)
        assert value == 0

    @pytest.mark.unit
    def test_positive_one(self):
        """Test positive one."""
        value = _get_signed_integer_from_bytes(0, 1)
        assert value == 1

    @pytest.mark.unit
    def test_positive_256(self):
        """Test positive 256."""
        value = _get_signed_integer_from_bytes(1, 0)
        assert value == 256

    @pytest.mark.unit
    def test_positive_500(self):
        """Test positive 500."""
        value = _get_signed_integer_from_bytes(1, 244)
        assert value == 500

    @pytest.mark.unit
    def test_negative_one(self):
        """Test negative one from two's complement."""
        value = _get_signed_integer_from_bytes(255, 255)
        assert value == -1

    @pytest.mark.unit
    def test_negative_256(self):
        """Test negative 256."""
        value = _get_signed_integer_from_bytes(255, 0)
        assert value == -256

    @pytest.mark.unit
    def test_max_positive(self):
        """Test maximum positive value."""
        value = _get_signed_integer_from_bytes(127, 255)
        assert value == 32767

    @pytest.mark.unit
    def test_max_negative(self):
        """Test minimum negative value."""
        value = _get_signed_integer_from_bytes(128, 0)
        assert value == -32768

    @pytest.mark.unit
    def test_roundtrip(self):
        """Test roundtrip conversion for various values."""
        test_values = [0, 1, -1, 100, -100, 500, -500, 32767, -32768]
        for original in test_values:
            high, low = _toTwosComplement2Bytes(original)
            recovered = _get_signed_integer_from_bytes(high, low)
            assert recovered == original, f"Roundtrip failed for {original}"


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    @pytest.mark.unit
    def test_bit_extraction_boundary(self):
        """Test bit extraction at boundaries."""
        # Test first and last bits
        byte = 0b10000001
        assert _bit_of_byte(byte, 0) == 1
        assert _bit_of_byte(byte, 7) == 1
        for bit in range(1, 7):
            assert _bit_of_byte(byte, bit) == 0

    @pytest.mark.unit
    def test_signed_unsigned_equivalence_positive(self):
        """Test signed and unsigned give same result for positive values."""
        for value in [0, 1, 100, 1000, 32767]:
            signed_high, signed_low = _toTwosComplement2Bytes(value)
            unsigned_high, unsigned_low = _toUnsignedBytes(value)
            assert signed_high == unsigned_high
            assert signed_low == unsigned_low

    @pytest.mark.unit
    def test_byte_range(self):
        """Test that byte values stay within 0-255."""
        test_values = [-32768, -1000, -1, 0, 1, 1000, 32767]
        for value in test_values:
            high, low = _toTwosComplement2Bytes(value)
            assert 0 <= high <= 255, f"High byte out of range for {value}"
            assert 0 <= low <= 255, f"Low byte out of range for {value}"
