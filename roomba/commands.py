"""
iRobot Create/Roomba Open Interface command byte constants.

This module defines all the command opcodes for communicating with the Roomba
via serial interface using the Open Interface protocol.

Reference: iRobot Create Open Interface Specification
"""

# Basic control commands
START = bytes([128])        # Initialize the robot, enter passive mode
BAUD = bytes([129])         # Change baud rate (+ 1 byte)
CONTROL = bytes([130])      # Deprecated for Create
SAFE = bytes([131])         # Enter safe mode
FULL = bytes([132])         # Enter full mode
POWER = bytes([133])        # Power down robot
SPOT = bytes([134])         # Start spot cleaning
CLEAN = bytes([135])        # Start cleaning (Roomba) / Cover demo (Create)
COVER = bytes([135])        # Same as CLEAN for Create
MAX = bytes([136])          # Start max cleaning (Roomba) / Demo (Create)
DEMO = bytes([136])         # Same as MAX for Create

# Movement commands
DRIVE = bytes([137])        # Control wheels with velocity/radius (+ 4 bytes)
DRIVEDIRECT = bytes([145])  # Direct wheel velocity control (+ 4 bytes, Create only)
MOTORS = bytes([138])       # Control brush/vacuum motors (+ 1 byte)

# LED/Display commands
LEDS = bytes([139])         # Control LED state (+ 3 bytes)

# Song/Audio commands
SONG = bytes([140])         # Define a song (+ 2N+2 bytes)
PLAY = bytes([141])         # Play a defined song (+ 1 byte)

# Sensor commands
SENSORS = bytes([142])      # Request sensor data (+ 1 byte)
QUERYLIST = bytes([149])    # Request specific sensor packets (+ N bytes, Create only)
STREAM = bytes([148])       # Stream sensor data (+ N bytes, Create only)
PAUSERESUME = bytes([150])  # Pause/resume sensor stream (+ 1 byte, Create only)

# Docking command
FORCESEEKINGDOCK = bytes([143])  # Force robot to seek dock

# Script commands (for autonomous sequences)
SCRIPT = bytes([152])       # Start script definition (+ N bytes)
ENDSCRIPT = bytes([153])    # End script and execute
WAITDIST = bytes([156])     # Wait for distance in script (+ 2 bytes)
WAITANGLE = bytes([157])    # Wait for angle in script (+ 2 bytes)

# Operating modes
OFF_MODE = 0
PASSIVE_MODE = 1
SAFE_MODE = 2
FULL_MODE = 3
