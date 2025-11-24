"""
Main robot control interface for iRobot Create/Roomba.

This module provides the Create class for controlling the robot via serial interface.
Currently imports from the legacy create.py module for backwards compatibility.

Future: Extract the full Create class implementation into this module.
"""

import logging

# Import the Create class from legacy create.py
# This maintains backwards compatibility while we set up the new structure
from create import Create

# Configure logging
logger = logging.getLogger(__name__)

# Re-export Create for use via roomba.robot
__all__ = ['Create']


# Future: Full Create class implementation will go here
# For now, we use the legacy implementation to maintain compatibility
# while demonstrating the new modular structure
