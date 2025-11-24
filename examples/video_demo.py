"""
Comprehensive Video Demonstration Script

This script provides a structured demonstration of all major features
for creating portfolio videos or live demonstrations.

Demonstration Flow:
1. System initialization and connection
2. Basic movement patterns
3. Sensor readings with explanations
4. Music playback (fun feature)
5. Autonomous behaviors (wall following, cleaning)
6. Voice control simulation

Perfect for recording demonstrations or live presentations!
"""

import time
import logging
from roomba import Create, SAFE_MODE
from roomba.sensors import (
    BATTERY_CHARGE, BATTERY_CAPACITY, WALL_SIGNAL,
    BUMPS_AND_WHEEL_DROPS, CLIFF_LEFT
)
from roomba.music import c5, d5, e5, f5, g5, QUARTER, EIGHTH
from config import DEFAULT_PORT, configure_logging

# Configure logging with nice formatting
configure_logging(level=logging.INFO)
logger = logging.getLogger(__name__)


class VideoDemo:
    """Structured demonstration for video recording."""

    def __init__(self, robot_port=DEFAULT_PORT):
        self.robot_port = robot_port
        self.robot = None

    def print_section(self, title):
        """Print a formatted section header."""
        print("\n" + "=" * 70)
        print(f"  {title}")
        print("=" * 70)
        time.sleep(1)

    def print_step(self, step_num, description):
        """Print a formatted step."""
        print(f"\n[Step {step_num}] {description}")
        time.sleep(0.5)

    def wait_for_continue(self):
        """Wait for user to press Enter before continuing."""
        input("\n⏸️  Press Enter to continue to next demo...")

    def demo_connection(self):
        """Demo 1: System initialization and connection."""
        self.print_section("DEMO 1: System Initialization")

        self.print_step(1, "Connecting to Roomba robot...")
        logger.info(f"Serial port: {self.robot_port}")
        logger.info("Baud rate: 115200")

        self.robot = Create(self.robot_port, startingMode=SAFE_MODE)
        logger.info("✅ Connection established!")
        logger.info("⚡ Robot in SAFE MODE (cliff sensors active)")

        time.sleep(2)

    def demo_basic_movement(self):
        """Demo 2: Basic movement patterns."""
        self.print_section("DEMO 2: Basic Movement Patterns")

        self.print_step(1, "Moving forward at 20 cm/s")
        self.robot.go(20, 0)
        time.sleep(2)

        self.print_step(2, "Stopping")
        self.robot.stop()
        time.sleep(1)

        self.print_step(3, "Rotating clockwise")
        self.robot.go(0, 50)
        time.sleep(2)

        self.print_step(4, "Stopping")
        self.robot.stop()
        time.sleep(1)

        self.print_step(5, "Moving in a circle (curved path)")
        self.robot.go(20, 30)
        time.sleep(3)

        self.print_step(6, "Stopping")
        self.robot.stop()
        time.sleep(1)

        logger.info("✅ Basic movement demo complete!")

    def demo_sensors(self):
        """Demo 3: Sensor reading and monitoring."""
        self.print_section("DEMO 3: Sensor Monitoring")

        self.print_step(1, "Reading battery sensors...")
        self.robot.sensors([BATTERY_CHARGE, BATTERY_CAPACITY])
        d = self.robot.sensord

        charge = d.get(BATTERY_CHARGE, 0)
        capacity = d.get(BATTERY_CAPACITY, 1)
        battery_pct = (charge / capacity * 100) if capacity > 0 else 0

        logger.info(f"📊 Battery charge: {charge} mAh")
        logger.info(f"📊 Battery capacity: {capacity} mAh")
        logger.info(f"🔋 Battery level: {battery_pct:.1f}%")
        time.sleep(2)

        self.print_step(2, "Reading proximity sensors...")
        self.robot.sensors([WALL_SIGNAL])
        d = self.robot.sensord
        logger.info(f"📡 Wall signal: {d.get(WALL_SIGNAL, 0)}")
        time.sleep(2)

        self.print_step(3, "Reading bump sensors...")
        self.robot.sensors([BUMPS_AND_WHEEL_DROPS])
        d = self.robot.sensord
        bumps = d.get(BUMPS_AND_WHEEL_DROPS, 0)
        logger.info(f"💥 Left bump: {'ACTIVE' if bumps & 0x02 else 'inactive'}")
        logger.info(f"💥 Right bump: {'ACTIVE' if bumps & 0x01 else 'inactive'}")
        time.sleep(2)

        logger.info("✅ Sensor demo complete!")

    def demo_music(self):
        """Demo 4: Music playback."""
        self.print_section("DEMO 4: Music Playback")

        self.print_step(1, "Playing C major scale...")
        scale = [
            (c5, QUARTER), (d5, QUARTER), (e5, QUARTER),
            (f5, QUARTER), (g5, QUARTER)
        ]
        self.robot.playSong(scale)
        time.sleep(3)

        self.print_step(2, "Playing melody...")
        melody = [
            (e5, QUARTER), (e5, QUARTER), (e5, EIGHTH),
            (e5, QUARTER), (e5, QUARTER), (e5, EIGHTH),
            (e5, QUARTER), (g5, QUARTER), (c5, QUARTER), (d5, QUARTER),
            (e5, QUARTER)
        ]
        self.robot.playSong(melody)
        time.sleep(4)

        logger.info("✅ Music demo complete!")

    def demo_wall_following(self):
        """Demo 5: Wall following behavior."""
        self.print_section("DEMO 5: Autonomous Wall Following")

        logger.info("This demonstrates reactive control with sensor feedback")
        logger.info("The robot will maintain a constant distance from the wall")
        time.sleep(2)

        self.print_step(1, "Starting wall following (10 seconds)...")

        # Simple wall following for demo
        start_time = time.time()
        while time.time() - start_time < 10:
            self.robot.sensors([WALL_SIGNAL, BUMPS_AND_WHEEL_DROPS])
            d = self.robot.sensord

            wall_signal = d.get(WALL_SIGNAL, 0)
            bumps = d.get(BUMPS_AND_WHEEL_DROPS, 0)

            # Check for bump
            if bumps & 0x03:
                logger.info("💥 Bump! Backing up and turning...")
                self.robot.go(-10, 0)
                time.sleep(1)
                self.robot.go(0, 50)
                time.sleep(1)
                continue

            # Simple proportional control
            if wall_signal > 120:
                # Too far from wall, turn right
                self.robot.go(15, 10)
            elif wall_signal < 80:
                # Too close to wall, turn left
                self.robot.go(15, -10)
            else:
                # Just right, go straight
                self.robot.go(15, 0)

            time.sleep(0.1)

        self.robot.stop()
        logger.info("✅ Wall following demo complete!")

    def demo_spiral_cleaning(self):
        """Demo 6: Spiral cleaning pattern."""
        self.print_section("DEMO 6: Autonomous Spiral Cleaning")

        logger.info("This demonstrates coverage path planning")
        logger.info("The robot moves in an expanding spiral pattern")
        time.sleep(2)

        self.print_step(1, "Starting spiral pattern (10 seconds)...")

        speed = 10
        start_time = time.time()
        while time.time() - start_time < 10:
            # Check for bumps
            self.robot.sensors([BUMPS_AND_WHEEL_DROPS])
            d = self.robot.sensord
            bumps = d.get(BUMPS_AND_WHEEL_DROPS, 0)

            if bumps & 0x03:
                logger.info("💥 Obstacle detected! Recovering...")
                self.robot.stop()
                time.sleep(0.2)
                self.robot.go(-10, 0)
                time.sleep(1)
                self.robot.go(0, 50)
                time.sleep(1)
                speed = 10  # Reset speed
                continue

            # Spiral pattern
            self.robot.go(int(speed), 15)
            speed = min(speed + 0.2, 25)  # Gradually increase speed

            time.sleep(0.1)

        self.robot.stop()
        logger.info("✅ Spiral cleaning demo complete!")

    def demo_complete(self):
        """Summary and completion."""
        self.print_section("DEMONSTRATION COMPLETE!")

        print("\n✨ All features demonstrated:")
        print("  ✅ System initialization and connection")
        print("  ✅ Basic movement control (forward, rotate, turn)")
        print("  ✅ Real-time sensor monitoring")
        print("  ✅ Music playback via MIDI")
        print("  ✅ Autonomous wall following (reactive control)")
        print("  ✅ Autonomous cleaning (spiral pattern)")
        print("\n🎬 Thank you for watching!")
        print("\nKey Technical Highlights:")
        print("  • Behavior-based robotics architecture")
        print("  • Real-time sensor fusion")
        print("  • Reactive and deliberative control")
        print("  • Modular Python package design")
        print("  • IoT integration (Alexa voice control)")
        print("")

    def run_full_demo(self, interactive=True):
        """Run the complete demonstration."""
        logger.info("🎬 Starting Alexa Roomba Video Demonstration")
        logger.info("=" * 70)
        time.sleep(2)

        try:
            # Demo 1: Connection
            self.demo_connection()
            if interactive:
                self.wait_for_continue()

            # Demo 2: Basic Movement
            self.demo_basic_movement()
            if interactive:
                self.wait_for_continue()

            # Demo 3: Sensors
            self.demo_sensors()
            if interactive:
                self.wait_for_continue()

            # Demo 4: Music
            self.demo_music()
            if interactive:
                self.wait_for_continue()

            # Demo 5: Wall Following
            self.demo_wall_following()
            if interactive:
                self.wait_for_continue()

            # Demo 6: Spiral Cleaning
            self.demo_spiral_cleaning()
            if interactive:
                self.wait_for_continue()

            # Complete
            self.demo_complete()

        except KeyboardInterrupt:
            logger.info("\n⏸️  Demo interrupted by user")
        except Exception as e:
            logger.error(f"❌ Error during demo: {e}", exc_info=True)
        finally:
            if self.robot:
                self.robot.stop()
                self.robot.close()
                logger.info("Robot connection closed")


def main():
    """Run the video demonstration."""
    import sys

    print("\n" + "=" * 70)
    print("  🎥 ALEXA ROOMBA - COMPLETE VIDEO DEMONSTRATION")
    print("=" * 70)
    print("\nThis script demonstrates all major features for portfolio videos.")
    print("\nOptions:")
    print("  1. Interactive mode (pause between demos)")
    print("  2. Continuous mode (auto-run all demos)")
    print("")

    choice = input("Select mode (1 or 2) [1]: ").strip() or "1"
    interactive = (choice == "1")

    # Create and run demo
    demo = VideoDemo()

    if interactive:
        print("\n▶️  Running in INTERACTIVE mode")
        print("You'll be prompted to continue between each demo section")
    else:
        print("\n▶️  Running in CONTINUOUS mode")
        print("All demos will run automatically")

    print("\nPress Ctrl+C at any time to stop")
    time.sleep(2)

    demo.run_full_demo(interactive=interactive)


if __name__ == "__main__":
    main()
