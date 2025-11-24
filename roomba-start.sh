#!/bin/bash
#
# Roomba Service Startup Script
# Starts the Alexa Roomba integration with proper error handling and logging
#

# Exit on error
set -e

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Configuration
LOG_DIR="$SCRIPT_DIR/logs"
LOG_FILE="$LOG_DIR/roomba_$(date +%Y%m%d).log"
PID_FILE="$SCRIPT_DIR/roomba.pid"

# Create log directory if it doesn't exist
mkdir -p "$LOG_DIR"

# Load environment variables from .env if it exists
if [ -f "$SCRIPT_DIR/.env" ]; then
    set -a
    source "$SCRIPT_DIR/.env"
    set +a
fi

# Detect Python executable
if [ -n "$PYTHON_EXEC" ]; then
    PYTHON="$PYTHON_EXEC"
elif [ -f "$SCRIPT_DIR/venv/bin/python" ]; then
    PYTHON="$SCRIPT_DIR/venv/bin/python"
elif command -v python3 &> /dev/null; then
    PYTHON="python3"
else
    echo "ERROR: Python 3 not found" | tee -a "$LOG_FILE"
    exit 1
fi

# Function to log messages
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Function to cleanup on exit
cleanup() {
    log "Shutting down Roomba service..."
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null 2>&1; then
            kill "$PID" 2>/dev/null || true
        fi
        rm -f "$PID_FILE"
    fi
    log "Roomba service stopped"
}

# Set up trap for cleanup
trap cleanup EXIT INT TERM

# Check if already running
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    if ps -p "$OLD_PID" > /dev/null 2>&1; then
        log "WARNING: Roomba service already running with PID $OLD_PID"
        exit 1
    else
        # Stale PID file
        rm -f "$PID_FILE"
    fi
fi

# Log startup
log "====================================="
log "Starting Alexa Roomba Service"
log "====================================="
log "Python: $PYTHON"
log "Working Directory: $SCRIPT_DIR"
log "Log File: $LOG_FILE"

# Check for required files
if [ ! -f "$SCRIPT_DIR/example-minimal.py" ]; then
    log "ERROR: example-minimal.py not found"
    exit 1
fi

# Start the service
log "Launching Roomba control daemon..."
nohup "$PYTHON" "$SCRIPT_DIR/example-minimal.py" >> "$LOG_FILE" 2>&1 &
PID=$!

# Save PID
echo "$PID" > "$PID_FILE"
log "Service started with PID: $PID"

# Verify it's running
sleep 2
if ps -p "$PID" > /dev/null 2>&1; then
    log "✓ Service is running successfully"
    log "Monitor logs with: tail -f $LOG_FILE"
else
    log "✗ ERROR: Service failed to start"
    rm -f "$PID_FILE"
    exit 1
fi

# Keep script alive if run directly (not from systemd)
if [ -t 0 ]; then
    log "Running in interactive mode. Press Ctrl+C to stop."
    wait "$PID"
fi
