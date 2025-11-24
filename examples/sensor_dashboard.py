"""
Real-Time Sensor Monitoring Dashboard

This example demonstrates full-stack development skills by creating a web-based
real-time sensor monitoring dashboard using Flask and WebSockets.

Key Concepts Demonstrated:
- Web development (Flask)
- Real-time data streaming (Server-Sent Events)
- REST API design
- Data visualization concepts
- Concurrent programming (threading)
- Full-stack integration
"""

import time
import json
import threading
import logging
from datetime import datetime
from collections import deque
from flask import Flask, render_template_string, jsonify, Response
from roomba import Create, SAFE_MODE
from roomba.sensors import (
    BATTERY_CHARGE, BATTERY_CAPACITY, VOLTAGE, CURRENT,
    WALL_SIGNAL, CLIFF_LEFT, CLIFF_FRONT_LEFT, CLIFF_FRONT_RIGHT, CLIFF_RIGHT,
    BUMPS_AND_WHEEL_DROPS, ENCODER_LEFT, ENCODER_RIGHT, TEMPERATURE
)
from config import DEFAULT_PORT, configure_logging

# Configure logging
configure_logging(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask app
app = Flask(__name__)

# Global sensor data storage
sensor_data = {
    'timestamp': None,
    'battery': {'charge': 0, 'capacity': 0, 'percentage': 0, 'voltage': 0, 'current': 0},
    'proximity': {'wall_signal': 0},
    'cliffs': {'left': False, 'front_left': False, 'front_right': False, 'right': False},
    'bumps': {'left': False, 'right': False},
    'encoders': {'left': 0, 'right': 0},
    'temperature': 0,
    'connected': False
}

# Historical data for charts (last 60 readings)
sensor_history = {
    'timestamps': deque(maxlen=60),
    'battery_percentage': deque(maxlen=60),
    'voltage': deque(maxlen=60),
    'wall_signal': deque(maxlen=60)
}

# HTML Dashboard Template
DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Roomba Sensor Dashboard</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }
        h1 {
            color: #667eea;
            margin-top: 0;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .status {
            font-size: 14px;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: bold;
        }
        .status.connected {
            background: #4caf50;
            color: white;
        }
        .status.disconnected {
            background: #f44336;
            color: white;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        .card {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }
        .card h3 {
            margin-top: 0;
            color: #667eea;
            font-size: 18px;
        }
        .metric {
            display: flex;
            justify-content: space-between;
            margin: 10px 0;
            padding: 8px 0;
            border-bottom: 1px solid #ddd;
        }
        .metric:last-child {
            border-bottom: none;
        }
        .metric-label {
            font-weight: 500;
            color: #666;
        }
        .metric-value {
            font-weight: bold;
            color: #333;
        }
        .battery-bar {
            width: 100%;
            height: 30px;
            background: #e0e0e0;
            border-radius: 15px;
            overflow: hidden;
            margin: 10px 0;
        }
        .battery-fill {
            height: 100%;
            background: linear-gradient(90deg, #4caf50 0%, #8bc34a 100%);
            transition: width 0.5s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
        }
        .battery-fill.low {
            background: linear-gradient(90deg, #f44336 0%, #ff5722 100%);
        }
        .sensor-indicator {
            display: inline-block;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            margin-right: 10px;
        }
        .sensor-indicator.active {
            background: #f44336;
            box-shadow: 0 0 10px #f44336;
        }
        .sensor-indicator.inactive {
            background: #4caf50;
        }
        .timestamp {
            text-align: center;
            color: #999;
            margin-top: 20px;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>
            🤖 Roomba Sensor Dashboard
            <span class="status" id="status">DISCONNECTED</span>
        </h1>

        <div class="grid">
            <!-- Battery Card -->
            <div class="card">
                <h3>🔋 Battery Status</h3>
                <div class="battery-bar">
                    <div class="battery-fill" id="battery-fill">0%</div>
                </div>
                <div class="metric">
                    <span class="metric-label">Charge:</span>
                    <span class="metric-value" id="battery-charge">0 mAh</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Capacity:</span>
                    <span class="metric-value" id="battery-capacity">0 mAh</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Voltage:</span>
                    <span class="metric-value" id="voltage">0 mV</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Current:</span>
                    <span class="metric-value" id="current">0 mA</span>
                </div>
            </div>

            <!-- Proximity Card -->
            <div class="card">
                <h3>📡 Proximity Sensors</h3>
                <div class="metric">
                    <span class="metric-label">Wall Signal:</span>
                    <span class="metric-value" id="wall-signal">0</span>
                </div>
            </div>

            <!-- Cliff Sensors Card -->
            <div class="card">
                <h3>⚠️ Cliff Sensors</h3>
                <div class="metric">
                    <span class="metric-label">
                        <span class="sensor-indicator inactive" id="cliff-left"></span>
                        Left:
                    </span>
                    <span class="metric-value" id="cliff-left-text">Safe</span>
                </div>
                <div class="metric">
                    <span class="metric-label">
                        <span class="sensor-indicator inactive" id="cliff-front-left"></span>
                        Front Left:
                    </span>
                    <span class="metric-value" id="cliff-front-left-text">Safe</span>
                </div>
                <div class="metric">
                    <span class="metric-label">
                        <span class="sensor-indicator inactive" id="cliff-front-right"></span>
                        Front Right:
                    </span>
                    <span class="metric-value" id="cliff-front-right-text">Safe</span>
                </div>
                <div class="metric">
                    <span class="metric-label">
                        <span class="sensor-indicator inactive" id="cliff-right"></span>
                        Right:
                    </span>
                    <span class="metric-value" id="cliff-right-text">Safe</span>
                </div>
            </div>

            <!-- Bump Sensors Card -->
            <div class="card">
                <h3>💥 Bump Sensors</h3>
                <div class="metric">
                    <span class="metric-label">
                        <span class="sensor-indicator inactive" id="bump-left"></span>
                        Left:
                    </span>
                    <span class="metric-value" id="bump-left-text">No Contact</span>
                </div>
                <div class="metric">
                    <span class="metric-label">
                        <span class="sensor-indicator inactive" id="bump-right"></span>
                        Right:
                    </span>
                    <span class="metric-value" id="bump-right-text">No Contact</span>
                </div>
            </div>

            <!-- Encoders Card -->
            <div class="card">
                <h3>🔄 Wheel Encoders</h3>
                <div class="metric">
                    <span class="metric-label">Left Wheel:</span>
                    <span class="metric-value" id="encoder-left">0</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Right Wheel:</span>
                    <span class="metric-value" id="encoder-right">0</span>
                </div>
            </div>

            <!-- System Info Card -->
            <div class="card">
                <h3>ℹ️ System Info</h3>
                <div class="metric">
                    <span class="metric-label">Temperature:</span>
                    <span class="metric-value" id="temperature">0 °C</span>
                </div>
            </div>
        </div>

        <div class="timestamp" id="timestamp">Waiting for data...</div>
    </div>

    <script>
        // Connect to Server-Sent Events stream
        const eventSource = new EventSource('/stream');

        eventSource.onmessage = function(event) {
            const data = JSON.parse(event.data);
            updateDashboard(data);
        };

        function updateDashboard(data) {
            // Update status
            const statusEl = document.getElementById('status');
            if (data.connected) {
                statusEl.textContent = 'CONNECTED';
                statusEl.className = 'status connected';
            } else {
                statusEl.textContent = 'DISCONNECTED';
                statusEl.className = 'status disconnected';
            }

            // Update battery
            const batteryPct = data.battery.percentage;
            const batteryFill = document.getElementById('battery-fill');
            batteryFill.style.width = batteryPct + '%';
            batteryFill.textContent = batteryPct.toFixed(1) + '%';
            batteryFill.className = 'battery-fill' + (batteryPct < 20 ? ' low' : '');

            document.getElementById('battery-charge').textContent = data.battery.charge + ' mAh';
            document.getElementById('battery-capacity').textContent = data.battery.capacity + ' mAh';
            document.getElementById('voltage').textContent = data.battery.voltage + ' mV';
            document.getElementById('current').textContent = data.battery.current + ' mA';

            // Update proximity
            document.getElementById('wall-signal').textContent = data.proximity.wall_signal;

            // Update cliffs
            updateSensor('cliff-left', data.cliffs.left);
            updateSensor('cliff-front-left', data.cliffs.front_left);
            updateSensor('cliff-front-right', data.cliffs.front_right);
            updateSensor('cliff-right', data.cliffs.right);

            // Update bumps
            updateSensor('bump-left', data.bumps.left);
            updateSensor('bump-right', data.bumps.right);

            // Update encoders
            document.getElementById('encoder-left').textContent = data.encoders.left;
            document.getElementById('encoder-right').textContent = data.encoders.right;

            // Update temperature
            document.getElementById('temperature').textContent = data.temperature + ' °C';

            // Update timestamp
            document.getElementById('timestamp').textContent = 'Last updated: ' + data.timestamp;
        }

        function updateSensor(id, active) {
            const indicator = document.getElementById(id);
            const text = document.getElementById(id + '-text');

            if (active) {
                indicator.className = 'sensor-indicator active';
                if (id.startsWith('cliff')) {
                    text.textContent = 'CLIFF!';
                    text.style.color = '#f44336';
                } else {
                    text.textContent = 'CONTACT!';
                    text.style.color = '#f44336';
                }
            } else {
                indicator.className = 'sensor-indicator inactive';
                if (id.startsWith('cliff')) {
                    text.textContent = 'Safe';
                } else {
                    text.textContent = 'No Contact';
                }
                text.style.color = '#333';
            }
        }
    </script>
</body>
</html>
"""


class SensorMonitor:
    """Monitors robot sensors and updates global data."""

    def __init__(self, robot_port=DEFAULT_PORT):
        self.robot_port = robot_port
        self.robot = None
        self.running = False
        self.thread = None

    def start(self):
        """Start sensor monitoring in background thread."""
        if self.running:
            return

        logger.info("Starting sensor monitor...")
        self.running = True
        self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.thread.start()

    def stop(self):
        """Stop sensor monitoring."""
        logger.info("Stopping sensor monitor...")
        self.running = False
        if self.thread:
            self.thread.join(timeout=2.0)
        if self.robot:
            self.robot.close()

    def _monitor_loop(self):
        """Main monitoring loop."""
        try:
            # Connect to robot
            logger.info(f"Connecting to robot on {self.robot_port}...")
            self.robot = Create(self.robot_port, startingMode=SAFE_MODE)
            sensor_data['connected'] = True
            logger.info("✅ Robot connected")

            while self.running:
                self._read_sensors()
                time.sleep(0.5)  # Update every 500ms

        except Exception as e:
            logger.error(f"Error in sensor monitor: {e}")
            sensor_data['connected'] = False
        finally:
            if self.robot:
                self.robot.close()

    def _read_sensors(self):
        """Read all sensors and update global data."""
        try:
            self.robot.sensors([
                BATTERY_CHARGE, BATTERY_CAPACITY, VOLTAGE, CURRENT,
                WALL_SIGNAL,
                CLIFF_LEFT, CLIFF_FRONT_LEFT, CLIFF_FRONT_RIGHT, CLIFF_RIGHT,
                BUMPS_AND_WHEEL_DROPS,
                ENCODER_LEFT, ENCODER_RIGHT,
                TEMPERATURE
            ])
            d = self.robot.sensord

            # Update battery data
            charge = d.get(BATTERY_CHARGE, 0)
            capacity = d.get(BATTERY_CAPACITY, 1)
            percentage = (charge / capacity * 100) if capacity > 0 else 0

            sensor_data['battery'] = {
                'charge': charge,
                'capacity': capacity,
                'percentage': percentage,
                'voltage': d.get(VOLTAGE, 0),
                'current': d.get(CURRENT, 0)
            }

            # Update proximity
            sensor_data['proximity'] = {
                'wall_signal': d.get(WALL_SIGNAL, 0)
            }

            # Update cliffs
            sensor_data['cliffs'] = {
                'left': d.get(CLIFF_LEFT, 0) == 1,
                'front_left': d.get(CLIFF_FRONT_LEFT, 0) == 1,
                'front_right': d.get(CLIFF_FRONT_RIGHT, 0) == 1,
                'right': d.get(CLIFF_RIGHT, 0) == 1
            }

            # Update bumps
            bumps = d.get(BUMPS_AND_WHEEL_DROPS, 0)
            sensor_data['bumps'] = {
                'left': (bumps & 0x02) != 0,
                'right': (bumps & 0x01) != 0
            }

            # Update encoders
            sensor_data['encoders'] = {
                'left': d.get(ENCODER_LEFT, 0),
                'right': d.get(ENCODER_RIGHT, 0)
            }

            # Update temperature
            sensor_data['temperature'] = d.get(TEMPERATURE, 0)

            # Update timestamp
            sensor_data['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Update history for charts
            sensor_history['timestamps'].append(time.time())
            sensor_history['battery_percentage'].append(percentage)
            sensor_history['voltage'].append(d.get(VOLTAGE, 0))
            sensor_history['wall_signal'].append(d.get(WALL_SIGNAL, 0))

        except Exception as e:
            logger.error(f"Error reading sensors: {e}")


# Flask routes
@app.route('/')
def index():
    """Serve the dashboard HTML."""
    return render_template_string(DASHBOARD_HTML)


@app.route('/api/sensors')
def api_sensors():
    """API endpoint for sensor data."""
    return jsonify(sensor_data)


@app.route('/stream')
def stream():
    """Server-Sent Events stream for real-time updates."""
    def event_stream():
        while True:
            # Send current sensor data
            yield f"data: {json.dumps(sensor_data)}\n\n"
            time.sleep(0.5)  # Update every 500ms

    return Response(event_stream(), mimetype='text/event-stream')


def main():
    """Run the sensor dashboard."""
    logger.info("=" * 60)
    logger.info("📊 Roomba Sensor Dashboard")
    logger.info("=" * 60)
    logger.info("Starting web server on http://localhost:5000")
    logger.info("Open your browser to view real-time sensor data")
    logger.info("Press Ctrl+C to stop")
    logger.info("=" * 60)

    # Start sensor monitoring
    monitor = SensorMonitor()
    monitor.start()

    try:
        # Run Flask server
        app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
    except KeyboardInterrupt:
        logger.info("\n🛑 Shutting down...")
    finally:
        monitor.stop()


if __name__ == "__main__":
    main()
