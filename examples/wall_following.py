"""
Wall Following Algorithm - Advanced Autonomous Navigation

This example demonstrates a sophisticated wall-following algorithm using
reactive control and sensor fusion. The robot maintains a constant distance
from the wall while navigating autonomously.

Key Concepts Demonstrated:
- Reactive control with sensor feedback
- PID-like proportional control
- State machine for behavior management
- Real-time sensor processing
- Autonomous navigation
"""

import time
import logging
from roomba import Create, SAFE_MODE
from roomba.sensors import WALL_SIGNAL, BUMPS_AND_WHEEL_DROPS, WALL
from config import DEFAULT_PORT, configure_logging

# Configure logging
configure_logging(level=logging.INFO)
logger = logging.getLogger(__name__)


class WallFollower:
    """
    Autonomous wall-following behavior using reactive control.

    The robot follows the wall on its right side, maintaining a
    constant distance using proportional control based on wall sensor readings.
    """

    # Control parameters
    BASE_SPEED = 15  # cm/s
    WALL_THRESHOLD = 50  # Wall detection threshold
    TARGET_WALL_SIGNAL = 100  # Desired wall distance (sensor value)

    # Proportional control gain
    KP = 0.5  # How aggressively to correct distance errors

    # State definitions
    STATE_FOLLOWING = "following"
    STATE_SEEKING = "seeking"
    STATE_BUMPED = "bumped"

    def __init__(self, robot):
        """Initialize wall follower with robot instance."""
        self.robot = robot
        self.state = self.STATE_SEEKING
        self.running = True

    def read_sensors(self):
        """Read and return relevant sensor data."""
        self.robot.sensors([WALL, WALL_SIGNAL, BUMPS_AND_WHEEL_DROPS])
        d = self.robot.sensord

        return {
            'wall_detected': d.get(WALL, 0) == 1,
            'wall_signal': d.get(WALL_SIGNAL, 0),
            'left_bump': (d.get(BUMPS_AND_WHEEL_DROPS, 0) & 0x02) != 0,
            'right_bump': (d.get(BUMPS_AND_WHEEL_DROPS, 0) & 0x01) != 0,
        }

    def calculate_control(self, wall_signal):
        """
        Calculate steering correction using proportional control.

        Returns velocity and spin rate for the robot.
        """
        # Error: difference between target and actual wall distance
        error = self.TARGET_WALL_SIGNAL - wall_signal

        # Proportional correction: turn towards/away from wall
        # Positive error = too far from wall, turn right (positive spin)
        # Negative error = too close to wall, turn left (negative spin)
        spin_correction = int(self.KP * error)

        # Limit spin rate for smooth movement
        spin_correction = max(-30, min(30, spin_correction))

        return self.BASE_SPEED, spin_correction

    def handle_seeking(self, sensors):
        """Search for a wall by spinning in place."""
        logger.info("Seeking wall...")

        if sensors['wall_detected']:
            logger.info("Wall found! Starting to follow.")
            self.state = self.STATE_FOLLOWING
        else:
            # Spin slowly to find wall
            self.robot.go(5, 30)

    def handle_following(self, sensors):
        """Follow the wall using proportional control."""
        if sensors['left_bump'] or sensors['right_bump']:
            logger.warning("Bump detected!")
            self.state = self.STATE_BUMPED
            return

        if not sensors['wall_detected']:
            logger.info("Lost wall, seeking...")
            self.state = self.STATE_SEEKING
            return

        # Calculate control output
        velocity, spin = self.calculate_control(sensors['wall_signal'])

        # Apply control
        self.robot.go(velocity, spin)

        # Log status periodically
        if int(time.time() * 10) % 20 == 0:  # Every 2 seconds
            logger.info(f"Wall signal: {sensors['wall_signal']}, "
                       f"Velocity: {velocity}, Spin: {spin}")

    def handle_bumped(self, sensors):
        """Recover from bump by backing up and turning."""
        logger.info("Recovering from bump...")

        # Stop
        self.robot.stop()
        time.sleep(0.2)

        # Back up
        self.robot.go(-10, 0)
        time.sleep(1.0)

        # Turn away from obstacle
        if sensors['right_bump']:
            self.robot.go(0, -50)  # Turn left
        else:
            self.robot.go(0, 50)   # Turn right
        time.sleep(1.0)

        # Resume seeking
        self.state = self.STATE_SEEKING

    def run(self, duration=30):
        """
        Run wall-following behavior for specified duration.

        Args:
            duration: Time in seconds to run (default: 30)
        """
        logger.info(f"Starting wall-following for {duration} seconds...")
        start_time = time.time()

        try:
            while self.running and (time.time() - start_time < duration):
                # Read sensors
                sensors = self.read_sensors()

                # State machine
                if self.state == self.STATE_SEEKING:
                    self.handle_seeking(sensors)
                elif self.state == self.STATE_FOLLOWING:
                    self.handle_following(sensors)
                elif self.state == self.STATE_BUMPED:
                    self.handle_bumped(sensors)

                # Small delay to prevent overwhelming the robot
                time.sleep(0.1)

            logger.info("Wall-following complete!")

        finally:
            # Always stop the robot
            self.robot.stop()

    def stop(self):
        """Stop the wall-following behavior."""
        self.running = False


def main():
    """Run wall-following demo."""
    logger.info("=== Wall Following Algorithm Demo ===")
    logger.info("This demo showcases autonomous navigation with reactive control")
    logger.info("")

    # Initialize robot connection
    logger.info(f"Connecting to Roomba on {DEFAULT_PORT}")
    robot = Create(DEFAULT_PORT, startingMode=SAFE_MODE)

    try:
        # Create wall follower instance
        follower = WallFollower(robot)

        # Run for 60 seconds (can be interrupted with Ctrl+C)
        logger.info("Starting wall following (press Ctrl+C to stop)...")
        follower.run(duration=60)

    except KeyboardInterrupt:
        logger.info("\nDemo interrupted by user")
    except Exception as e:
        logger.error(f"Error during demo: {e}", exc_info=True)
    finally:
        # Always close the connection
        logger.info("Closing robot connection")
        robot.stop()
        robot.close()


if __name__ == "__main__":
    main()
