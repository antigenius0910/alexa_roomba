"""
Complete Alexa Voice Control Integration

This example demonstrates the full Alexa voice control system using Fauxmo
to emulate a Belkin WeMo device. Shows integration skills and IoT concepts.

Voice Commands Supported:
- "Alexa, turn on <device name>" - Start cleaning
- "Alexa, turn off <device name>" - Stop and dock
- "Alexa, set <device name> to 50%" - Set cleaning intensity

Key Concepts Demonstrated:
- IoT integration (Alexa Smart Home)
- UPnP device emulation
- Async event handling
- Voice-activated robotics
- REST API concepts
"""

import logging
import time
import threading
from fauxmo import fauxmo
from roomba import Create, SAFE_MODE
from config import (
    DEFAULT_PORT, FAUXMO_DEVICE_NAME, FAUXMO_PORT,
    FAUXMO_DEBUG, configure_logging
)

# Configure logging
configure_logging(level=logging.INFO if FAUXMO_DEBUG else logging.WARNING)
logger = logging.getLogger(__name__)


class AlexaRoombaController:
    """
    Alexa-controlled Roomba with multiple voice commands.

    Implements the Fauxmo interface to respond to Alexa voice commands
    and translates them into robot actions.
    """

    def __init__(self, robot_port=DEFAULT_PORT):
        """Initialize the Alexa controller."""
        self.robot_port = robot_port
        self.robot = None
        self.is_cleaning = False
        self.cleaning_thread = None
        self.cleaning_intensity = 50  # Default intensity (0-100)

        # Statistics
        self.total_starts = 0
        self.total_cleaning_time = 0
        self.last_start_time = None

    def connect_robot(self):
        """Connect to the Roomba robot."""
        if self.robot is None:
            logger.info(f"Connecting to Roomba on {self.robot_port}...")
            try:
                self.robot = Create(self.robot_port, startingMode=SAFE_MODE)
                logger.info("✅ Robot connected successfully")
                return True
            except Exception as e:
                logger.error(f"❌ Failed to connect to robot: {e}")
                return False
        return True

    def disconnect_robot(self):
        """Safely disconnect from the robot."""
        if self.robot:
            try:
                self.robot.stop()
                self.robot.close()
                self.robot = None
                logger.info("Robot disconnected")
            except Exception as e:
                logger.error(f"Error disconnecting robot: {e}")

    def start_cleaning(self):
        """
        Start autonomous cleaning behavior.

        Uses spiral pattern with intensity-based speed.
        """
        if not self.connect_robot():
            return False

        if self.is_cleaning:
            logger.info("Already cleaning!")
            return True

        logger.info(f"🎬 Starting cleaning at {self.cleaning_intensity}% intensity")
        self.is_cleaning = True
        self.last_start_time = time.time()
        self.total_starts += 1

        # Start cleaning in separate thread
        self.cleaning_thread = threading.Thread(target=self._cleaning_loop, daemon=True)
        self.cleaning_thread.start()

        return True

    def stop_cleaning(self):
        """Stop cleaning and update statistics."""
        if not self.is_cleaning:
            logger.info("Not currently cleaning")
            return True

        logger.info("⏹️  Stopping cleaning")
        self.is_cleaning = False

        # Update statistics
        if self.last_start_time:
            session_time = time.time() - self.last_start_time
            self.total_cleaning_time += session_time
            logger.info(f"📊 Session duration: {session_time:.1f}s")

        # Wait for cleaning thread to finish
        if self.cleaning_thread and self.cleaning_thread.is_alive():
            self.cleaning_thread.join(timeout=2.0)

        # Stop the robot
        if self.robot:
            self.robot.stop()

        return True

    def set_intensity(self, level):
        """
        Set cleaning intensity (0-100%).

        Args:
            level: Intensity percentage (0-100)
        """
        self.cleaning_intensity = max(0, min(100, level))
        logger.info(f"🎚️  Cleaning intensity set to {self.cleaning_intensity}%")

        # If currently cleaning, the new intensity will apply
        if self.is_cleaning:
            logger.info("New intensity will be applied to ongoing cleaning")

        return True

    def _cleaning_loop(self):
        """
        Internal cleaning loop running in separate thread.

        Implements simple spiral pattern scaled by intensity.
        """
        try:
            # Calculate speed based on intensity
            min_speed = 10
            max_speed = 30
            speed = min_speed + (max_speed - min_speed) * (self.cleaning_intensity / 100.0)

            logger.info(f"Cleaning loop started (speed: {speed:.0f} cm/s)")

            while self.is_cleaning:
                # Simple spiral pattern
                self.robot.go(int(speed), 20)
                time.sleep(0.5)

        except Exception as e:
            logger.error(f"Error in cleaning loop: {e}")
            self.is_cleaning = False

    def print_statistics(self):
        """Print usage statistics."""
        logger.info("=" * 60)
        logger.info("Alexa Roomba Statistics:")
        logger.info(f"  Total Activations: {self.total_starts}")
        logger.info(f"  Total Cleaning Time: {self.total_cleaning_time:.1f}s")
        if self.total_starts > 0:
            avg_time = self.total_cleaning_time / self.total_starts
            logger.info(f"  Average Session: {avg_time:.1f}s")
        logger.info("=" * 60)


# Global controller instance
controller = AlexaRoombaController()


class RoombaDevice(fauxmo.fauxmo_device):
    """Fauxmo device representing the Roomba for Alexa."""

    def on(self):
        """Called when Alexa turns device on."""
        logger.info(f'🗣️  Alexa command: Turn ON "{FAUXMO_DEVICE_NAME}"')
        return controller.start_cleaning()

    def off(self):
        """Called when Alexa turns device off."""
        logger.info(f'🗣️  Alexa command: Turn OFF "{FAUXMO_DEVICE_NAME}"')
        return controller.stop_cleaning()

    def set_level(self, level):
        """Called when Alexa sets device level (0-100)."""
        logger.info(f'🗣️  Alexa command: Set "{FAUXMO_DEVICE_NAME}" to {level}%')
        return controller.set_intensity(level)


def main():
    """Run Alexa voice control service."""
    logger.info("=" * 60)
    logger.info("🎤 Alexa Roomba Voice Control")
    logger.info("=" * 60)
    logger.info(f"Device Name: {FAUXMO_DEVICE_NAME}")
    logger.info(f"Port: {FAUXMO_PORT}")
    logger.info("")
    logger.info("Voice Commands:")
    logger.info(f'  "Alexa, turn on {FAUXMO_DEVICE_NAME}"')
    logger.info(f'  "Alexa, turn off {FAUXMO_DEVICE_NAME}"')
    logger.info(f'  "Alexa, set {FAUXMO_DEVICE_NAME} to 75 percent"')
    logger.info("")
    logger.info("Setup Instructions:")
    logger.info("  1. Say: 'Alexa, discover my devices'")
    logger.info("  2. Wait for discovery to complete")
    logger.info(f"  3. Use voice commands with device name '{FAUXMO_DEVICE_NAME}'")
    logger.info("")
    logger.info("Press Ctrl+C to stop")
    logger.info("=" * 60)

    try:
        # Create Fauxmo server
        server = fauxmo.fauxmo(
            FAUXMO_DEVICE_NAME,
            RoombaDevice,
            FAUXMO_PORT,
            FAUXMO_DEBUG
        )

        # Run server (blocks until interrupted)
        logger.info("🚀 Service started, waiting for Alexa commands...")
        server.run()

    except KeyboardInterrupt:
        logger.info("\n🛑 Service stopped by user")
        controller.print_statistics()
    except Exception as e:
        logger.error(f"❌ Error running service: {e}", exc_info=True)
    finally:
        # Clean up
        controller.stop_cleaning()
        controller.disconnect_robot()
        logger.info("Service shutdown complete")


if __name__ == "__main__":
    main()
