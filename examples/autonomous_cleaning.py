"""
Autonomous Cleaning Algorithm - Intelligent Room Coverage

This example demonstrates an intelligent room coverage algorithm that combines
multiple behaviors: spiral pattern movement, bump-and-turn obstacle avoidance,
and cliff detection. Showcases advanced robotics concepts for portfolio.

Key Concepts Demonstrated:
- Coverage path planning (spiral pattern)
- Behavior-based architecture
- Obstacle avoidance (bump sensors)
- Safety mechanisms (cliff detection)
- State management
- Real-time decision making
"""

import time
import random
import logging
from roomba import Create, SAFE_MODE
from roomba.sensors import (
    BUMPS_AND_WHEEL_DROPS, CLIFF_LEFT, CLIFF_FRONT_LEFT,
    CLIFF_FRONT_RIGHT, CLIFF_RIGHT, BATTERY_CHARGE, BATTERY_CAPACITY
)
from config import DEFAULT_PORT, configure_logging

# Configure logging
configure_logging(level=logging.INFO)
logger = logging.getLogger(__name__)


class AutonomousCleaner:
    """
    Intelligent autonomous cleaning robot using behavior-based architecture.

    Implements multiple behaviors with priority:
    1. Cliff detection (highest priority - safety)
    2. Bump reaction (obstacle avoidance)
    3. Spiral coverage (default cleaning behavior)
    """

    # Movement parameters
    SPIRAL_INCREMENT = 2  # cm/s increase per revolution
    MAX_SPIRAL_SPEED = 30  # Maximum forward speed
    TURN_SPEED = 30  # Rotation speed for turns

    # Battery threshold for low battery warning
    LOW_BATTERY_THRESHOLD = 20  # percent

    def __init__(self, robot):
        """Initialize autonomous cleaner with robot instance."""
        self.robot = robot
        self.running = True
        self.current_speed = 10  # Start slow
        self.coverage_time = 0
        self.bumps_handled = 0
        self.cliffs_avoided = 0

    def read_sensors(self):
        """Read and return all relevant sensor data."""
        self.robot.sensors([
            BUMPS_AND_WHEEL_DROPS,
            CLIFF_LEFT, CLIFF_FRONT_LEFT, CLIFF_FRONT_RIGHT, CLIFF_RIGHT,
            BATTERY_CHARGE, BATTERY_CAPACITY
        ])
        d = self.robot.sensord

        return {
            'left_bump': (d.get(BUMPS_AND_WHEEL_DROPS, 0) & 0x02) != 0,
            'right_bump': (d.get(BUMPS_AND_WHEEL_DROPS, 0) & 0x01) != 0,
            'cliff_left': d.get(CLIFF_LEFT, 0) == 1,
            'cliff_front_left': d.get(CLIFF_FRONT_LEFT, 0) == 1,
            'cliff_front_right': d.get(CLIFF_FRONT_RIGHT, 0) == 1,
            'cliff_right': d.get(CLIFF_RIGHT, 0) == 1,
            'battery_charge': d.get(BATTERY_CHARGE, 0),
            'battery_capacity': d.get(BATTERY_CAPACITY, 1),
        }

    def check_battery(self, sensors):
        """Check battery level and warn if low."""
        charge = sensors['battery_charge']
        capacity = sensors['battery_capacity']

        if capacity > 0:
            battery_pct = (charge / capacity) * 100
            if battery_pct < self.LOW_BATTERY_THRESHOLD:
                logger.warning(f"⚠️  Low battery: {battery_pct:.1f}%")
                return battery_pct
        return 100

    def handle_cliff(self, sensors):
        """
        Emergency cliff avoidance - highest priority behavior.

        Returns True if cliff was detected and handled.
        """
        any_cliff = (sensors['cliff_left'] or sensors['cliff_front_left'] or
                    sensors['cliff_front_right'] or sensors['cliff_right'])

        if any_cliff:
            logger.warning("🚨 CLIFF DETECTED! Reversing immediately!")
            self.cliffs_avoided += 1

            # Stop immediately
            self.robot.stop()
            time.sleep(0.2)

            # Back up away from cliff
            self.robot.go(-15, 0)
            time.sleep(1.5)

            # Turn away from cliff
            self.robot.go(0, random.choice([-self.TURN_SPEED, self.TURN_SPEED]))
            time.sleep(1.5)

            # Reset spiral pattern
            self.current_speed = 10

            return True
        return False

    def handle_bump(self, sensors):
        """
        Obstacle avoidance using bump sensors.

        Returns True if bump was detected and handled.
        """
        if sensors['left_bump'] or sensors['right_bump']:
            logger.info("💥 Bump detected! Avoiding obstacle...")
            self.bumps_handled += 1

            # Stop
            self.robot.stop()
            time.sleep(0.2)

            # Back up
            self.robot.go(-10, 0)
            time.sleep(1.0)

            # Turn away from obstacle
            if sensors['right_bump']:
                # Right bump, turn left
                turn_angle = random.randint(60, 120)
                logger.info(f"Turning left {turn_angle}°")
                self.robot.go(0, -self.TURN_SPEED)
            else:
                # Left bump, turn right
                turn_angle = random.randint(60, 120)
                logger.info(f"Turning right {turn_angle}°")
                self.robot.go(0, self.TURN_SPEED)

            time.sleep(turn_angle / 90.0)  # Approximate time for turn

            # Reset spiral pattern
            self.current_speed = 10

            return True
        return False

    def execute_spiral_pattern(self):
        """
        Execute spiral coverage pattern - default cleaning behavior.

        Gradually increases turning radius to cover maximum area.
        """
        # Slowly increase forward speed to create spiral
        if self.current_speed < self.MAX_SPIRAL_SPEED:
            self.current_speed += 0.1

        # Constant gentle turn creates spiral
        # Positive spin = clockwise spiral
        spin_rate = 15

        self.robot.go(int(self.current_speed), spin_rate)

    def print_statistics(self):
        """Print cleaning session statistics."""
        logger.info("=" * 60)
        logger.info("Cleaning Session Statistics:")
        logger.info(f"  Coverage Time:    {self.coverage_time:.1f} seconds")
        logger.info(f"  Obstacles Avoided: {self.bumps_handled}")
        logger.info(f"  Cliffs Avoided:    {self.cliffs_avoided}")
        logger.info("=" * 60)

    def run(self, duration=60):
        """
        Run autonomous cleaning for specified duration.

        Args:
            duration: Time in seconds to run (default: 60)
        """
        logger.info("=" * 60)
        logger.info("🤖 Starting Autonomous Cleaning Mode")
        logger.info(f"Duration: {duration} seconds")
        logger.info("Behaviors: Spiral Coverage + Obstacle Avoidance + Cliff Detection")
        logger.info("=" * 60)

        start_time = time.time()

        try:
            while self.running and (time.time() - start_time < duration):
                # Read all sensors
                sensors = self.read_sensors()

                # Check battery (non-blocking)
                self.check_battery(sensors)

                # Behavior priority:
                # 1. Safety first - cliff detection
                if self.handle_cliff(sensors):
                    continue

                # 2. Obstacle avoidance - bump sensors
                if self.handle_bump(sensors):
                    continue

                # 3. Default behavior - spiral coverage pattern
                self.execute_spiral_pattern()
                self.coverage_time += 0.1

                # Log progress every 10 seconds
                elapsed = time.time() - start_time
                if int(elapsed) % 10 == 0 and int(elapsed * 10) % 10 == 0:
                    logger.info(f"⏱️  Cleaning progress: {elapsed:.0f}s / {duration}s "
                              f"(Speed: {self.current_speed:.0f} cm/s)")

                # Small delay
                time.sleep(0.1)

            logger.info("✅ Cleaning session complete!")
            self.print_statistics()

        except KeyboardInterrupt:
            logger.info("\n⏸️  Cleaning interrupted by user")
            self.print_statistics()
        finally:
            # Always stop the robot
            self.robot.stop()

    def stop(self):
        """Stop the cleaning behavior."""
        self.running = False


def main():
    """Run autonomous cleaning demo."""
    logger.info("=== Autonomous Cleaning Algorithm Demo ===")
    logger.info("Demonstrates intelligent room coverage with obstacle avoidance")
    logger.info("")

    # Initialize robot connection
    logger.info(f"Connecting to Roomba on {DEFAULT_PORT}")
    robot = Create(DEFAULT_PORT, startingMode=SAFE_MODE)

    try:
        # Create autonomous cleaner instance
        cleaner = AutonomousCleaner(robot)

        # Run for 90 seconds (can be interrupted with Ctrl+C)
        logger.info("Press Ctrl+C to stop cleaning")
        cleaner.run(duration=90)

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
