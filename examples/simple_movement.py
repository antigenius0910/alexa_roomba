"""
Simple movement example demonstrating the roomba package API.

This example shows basic robot control using the new modular structure.
"""

import time
import logging
from roomba import Create, SAFE_MODE
from config import DEFAULT_PORT, configure_logging

# Configure logging
configure_logging(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Demonstrate basic Roomba movement patterns."""
    logger.info("Starting simple movement demo...")

    # Initialize robot connection
    logger.info(f"Connecting to Roomba on {DEFAULT_PORT}")
    robot = Create(DEFAULT_PORT, startingMode=SAFE_MODE)

    try:
        # Print current sensor data
        logger.info("Reading sensors...")
        robot.printSensors()

        # Move forward
        logger.info("Moving forward at 20 cm/s for 2 seconds")
        robot.go(20, 0)
        time.sleep(2.0)

        # Stop
        logger.info("Stopping")
        robot.stop()
        time.sleep(1.0)

        # Spin in place
        logger.info("Spinning clockwise for 2 seconds")
        robot.go(0, 50)
        time.sleep(2.0)

        # Stop
        logger.info("Stopping")
        robot.stop()
        time.sleep(1.0)

        # Move in a circle
        logger.info("Moving in a circle")
        robot.go(20, 30)
        time.sleep(3.0)

        # Stop
        logger.info("Stopping")
        robot.stop()

        logger.info("Demo complete!")

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
