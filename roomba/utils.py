"""
Utility functions for bit manipulation and data conversion.

These functions handle low-level operations like two's complement conversion,
binary string manipulation, and byte-level data processing.
"""

import logging
from .commands import OFF_MODE, PASSIVE_MODE, SAFE_MODE, FULL_MODE

# Configure logging
logger = logging.getLogger(__name__)


def mode_to_string(mode):
    """
    Convert a robot mode constant to its string representation.

    Args:
        mode (int): One of OFF_MODE, PASSIVE_MODE, SAFE_MODE, FULL_MODE

    Returns:
        str: String name of the mode
    """
    mode_map = {
        OFF_MODE: 'OFF_MODE',
        PASSIVE_MODE: 'PASSIVE_MODE',
        SAFE_MODE: 'SAFE_MODE',
        FULL_MODE: 'FULL_MODE'
    }
    if mode in mode_map:
        return mode_map[mode]
    logger.warning(f'Unknown mode {mode} seen in mode_to_string')
    return 'UNKNOWN_MODE'


def _bit_of_byte(bit, byte):
    """
    Extract a specific bit from a byte.

    Args:
        bit (int): Bit position (0-7, where 0 is LSB)
        byte (int): Byte value

    Returns:
        int: 0 or 1, the value of the specified bit
    """
    if bit < 0 or bit > 7:
        logger.error(f'Bit position {bit} is out of range (0-7), returning 0')
        return 0
    return ((byte >> bit) & 0x01)


def _to_binary(val, numbits):
    """
    Print a value in binary format (for debugging).

    Args:
        val (int): Value to print
        numbits (int): Number of bits to display
    """
    if numbits == 0:
        return
    _to_binary(val >> 1, numbits - 1)
    print(val & 0x01, end='')


def _from_binary(s):
    """
    Convert a binary string to an integer.

    Args:
        s (str): String of '0's and '1's

    Returns:
        int: Integer value
    """
    if s == '':
        return 0
    lowbit = ord(s[-1]) - ord('0')
    return lowbit + 2 * _from_binary(s[:-1])


def _twos_complement_int1byte(byte):
    """
    Interpret a byte as a two's complement signed integer.

    Args:
        byte (int): Unsigned byte value (0-255)

    Returns:
        int: Signed integer value (-128 to 127)
    """
    topbit = _bit_of_byte(7, byte)
    lowerbits = byte & 127
    if topbit == 1:
        return lowerbits - (1 << 7)
    else:
        return lowerbits


def _twos_complement_int2bytes(high_byte, low_byte):
    """
    Interpret two bytes as a two's complement signed 16-bit integer.

    Args:
        high_byte (int): High byte (MSB)
        low_byte (int): Low byte (LSB)

    Returns:
        int: Signed integer value (-32768 to 32767)
    """
    val = (high_byte << 8) | low_byte
    topbit = _bit_of_byte(15, val)
    lowerbits = val & 32767
    if topbit == 1:
        return lowerbits - (1 << 15)
    else:
        return lowerbits


def _toTwosComplement2Bytes(value):
    """
    Convert a signed integer to two's complement 2-byte representation.

    Args:
        value (int): Signed integer (-32768 to 32767)

    Returns:
        tuple: (high_byte, low_byte) as unsigned integers
    """
    if value < 0:
        value = (1 << 16) + value
    high_byte = (value >> 8) & 0xFF
    low_byte = value & 0xFF
    return (high_byte, low_byte)


def bytes_of_r(r):
    """
    Debug function to print raw bytes of a sensor reply.

    Args:
        r (bytes): Raw sensor data
    """
    logger.debug(f'Raw r is: {r}')
    for i, byte in enumerate(r):
        logger.debug(f'Byte {i} is: {byte}')
    logger.debug('Finished reading sensor data')
