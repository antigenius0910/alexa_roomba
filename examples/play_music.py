"""
Music playback example demonstrating MIDI note control.

This example shows how to compose and play songs using the roomba package.
"""

import time
import logging
from roomba import Create, SAFE_MODE
from roomba.music import c5, d5, e5, f5, g5, a5, QUARTER, HALF, EIGHTH
from config import DEFAULT_PORT, configure_logging

# Configure logging
configure_logging(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Play various melodies on the Roomba."""
    logger.info("Starting music demo...")

    # Initialize robot connection
    logger.info(f"Connecting to Roomba on {DEFAULT_PORT}")
    robot = Create(DEFAULT_PORT, startingMode=SAFE_MODE)

    try:
        # Define a simple melody (C major scale)
        logger.info("Playing C major scale...")
        scale = [
            (c5, QUARTER),
            (d5, QUARTER),
            (e5, QUARTER),
            (f5, QUARTER),
            (g5, QUARTER),
            (a5, QUARTER),
        ]
        robot.playSong(scale)
        time.sleep(3.0)

        # Define Mary Had a Little Lamb
        logger.info("Playing Mary Had a Little Lamb...")
        mary = [
            (e5, QUARTER), (d5, QUARTER), (c5, QUARTER), (d5, QUARTER),
            (e5, QUARTER), (e5, QUARTER), (e5, HALF),
            (d5, QUARTER), (d5, QUARTER), (d5, HALF),
            (e5, QUARTER), (g5, QUARTER), (g5, HALF),
            (e5, QUARTER), (d5, QUARTER), (c5, QUARTER), (d5, QUARTER),
            (e5, QUARTER), (e5, QUARTER), (e5, QUARTER), (e5, QUARTER),
            (d5, QUARTER), (d5, QUARTER), (e5, QUARTER), (d5, QUARTER),
            (c5, HALF),
        ]
        robot.playSong(mary)
        time.sleep(8.0)

        logger.info("Music demo complete!")

    except KeyboardInterrupt:
        logger.info("Demo interrupted by user")
    except Exception as e:
        logger.error(f"Error during demo: {e}")
    finally:
        # Always close the connection
        logger.info("Closing robot connection")
        robot.close()


if __name__ == "__main__":
    main()
