"""
Sensor reading example demonstrating sensor data access.

This example shows how to read and display various sensor values from the Roomba.
"""

import time
import logging
from roomba import Create, SAFE_MODE
from roomba.sensors import (
    WALL_SIGNAL, CLIFF_LEFT, CLIFF_RIGHT, BATTERY_CHARGE,
    BATTERY_CAPACITY, VOLTAGE, ENCODER_LEFT, ENCODER_RIGHT
)
from config import DEFAULT_PORT, configure_logging

# Configure logging
configure_logging(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Read and display Roomba sensor data."""
    logger.info("Starting sensor reading demo...")

    # Initialize robot connection
    logger.info(f"Connecting to Roomba on {DEFAULT_PORT}")
    robot = Create(DEFAULT_PORT, startingMode=SAFE_MODE)

    try:
        logger.info("Reading sensor data continuously (Ctrl+C to stop)...")

        while True:
            # Read specific sensors
            sensors = robot.sensors([
                WALL_SIGNAL,
                CLIFF_LEFT,
                CLIFF_RIGHT,
                BATTERY_CHARGE,
                BATTERY_CAPACITY,
                VOLTAGE,
                ENCODER_LEFT,
                ENCODER_RIGHT
            ])

            # Get the sensor dictionary
            d = robot.sensord

            # Display selected sensor values
            print("\\n" + "="*50)
            print(f"Wall Signal:      {d.get(WALL_SIGNAL, 'N/A')}")
            print(f"Cliff Left:       {d.get(CLIFF_LEFT, 'N/A')}")
            print(f"Cliff Right:      {d.get(CLIFF_RIGHT, 'N/A')}")
            print(f"Battery Charge:   {d.get(BATTERY_CHARGE, 'N/A')} mAh")
            print(f"Battery Capacity: {d.get(BATTERY_CAPACITY, 'N/A')} mAh")
            print(f"Voltage:          {d.get(VOLTAGE, 'N/A')} mV")
            print(f"Encoder Left:     {d.get(ENCODER_LEFT, 'N/A')}")
            print(f"Encoder Right:    {d.get(ENCODER_RIGHT, 'N/A')}")

            # Calculate battery percentage
            charge = d.get(BATTERY_CHARGE, 0)
            capacity = d.get(BATTERY_CAPACITY, 1)
            battery_pct = (charge / capacity * 100) if capacity > 0 else 0
            print(f"Battery Level:    {battery_pct:.1f}%")
            print("="*50)

            time.sleep(1.0)

    except KeyboardInterrupt:
        logger.info("\\nSensor reading stopped by user")
    except Exception as e:
        logger.error(f"Error reading sensors: {e}")
    finally:
        # Always close the connection
        logger.info("Closing robot connection")
        robot.close()


if __name__ == "__main__":
    main()
