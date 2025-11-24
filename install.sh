#!/bin/bash
#
# Alexa Roomba Installation Script
# Automates the installation and configuration process
#

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Functions
print_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

check_python() {
    print_header "Checking Python Installation"

    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        print_success "Python 3 found: $PYTHON_VERSION"
        PYTHON_CMD="python3"
    else
        print_error "Python 3 not found. Please install Python 3.7 or higher."
        exit 1
    fi

    # Check Python version is 3.7+
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)

    if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 7 ]); then
        print_error "Python 3.7 or higher required. Found: $PYTHON_VERSION"
        exit 1
    fi
}

create_virtualenv() {
    print_header "Setting Up Virtual Environment"

    if [ -d "venv" ]; then
        print_warning "Virtual environment already exists. Skipping creation."
    else
        $PYTHON_CMD -m venv venv
        print_success "Virtual environment created"
    fi

    # Activate virtual environment
    source venv/bin/activate
    print_success "Virtual environment activated"
}

install_dependencies() {
    print_header "Installing Dependencies"

    pip install --upgrade pip
    pip install -r requirements.txt

    # Install python-dotenv for .env file support
    pip install python-dotenv

    print_success "Dependencies installed"
}

create_config() {
    print_header "Creating Configuration"

    if [ -f ".env" ]; then
        print_warning ".env file already exists. Skipping configuration."
        echo "To reconfigure, delete .env and run install again."
    else
        cp .env.example .env
        print_success ".env file created from template"

        # Interactive configuration
        echo ""
        echo "Please configure your settings:"
        echo ""

        # Detect platform and suggest port
        if [[ "$OSTYPE" == "linux-gnu"* ]]; then
            SUGGESTED_PORT="/dev/ttyUSB0"
        elif [[ "$OSTYPE" == "darwin"* ]]; then
            SUGGESTED_PORT="/dev/tty.usbserial"
        else
            SUGGESTED_PORT="COM3"
        fi

        read -p "Serial port [$SUGGESTED_PORT]: " USER_PORT
        USER_PORT=${USER_PORT:-$SUGGESTED_PORT}
        sed -i.bak "s|ROOMBA_PORT=.*|ROOMBA_PORT=$USER_PORT|" .env

        read -p "Device name [Stardust Destroyer]: " USER_NAME
        USER_NAME=${USER_NAME:-"Stardust Destroyer"}
        sed -i.bak "s|FAUXMO_DEVICE_NAME=.*|FAUXMO_DEVICE_NAME=\"$USER_NAME\"|" .env

        rm -f .env.bak
        print_success "Configuration saved to .env"
    fi
}

check_serial_permissions() {
    print_header "Checking Serial Port Permissions"

    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Check if user is in dialout group
        if groups | grep -q dialout; then
            print_success "User is in 'dialout' group"
        else
            print_warning "User is NOT in 'dialout' group"
            echo "Run: sudo usermod -a -G dialout $USER"
            echo "Then log out and back in for changes to take effect"
        fi
    fi
}

setup_systemd() {
    print_header "Setting Up Systemd Service"

    read -p "Install systemd service for auto-start? (y/N): " INSTALL_SERVICE

    if [[ "$INSTALL_SERVICE" =~ ^[Yy]$ ]]; then
        # Update service file with correct paths
        sed "s|INSTALL_DIR|$SCRIPT_DIR|g" roomba.service.template > roomba.service

        sudo cp roomba.service /etc/systemd/system/
        sudo systemctl daemon-reload

        print_success "Systemd service installed"

        read -p "Enable service to start on boot? (y/N): " ENABLE_SERVICE
        if [[ "$ENABLE_SERVICE" =~ ^[Yy]$ ]]; then
            sudo systemctl enable roomba.service
            print_success "Service enabled for auto-start"
        fi

        read -p "Start service now? (y/N): " START_SERVICE
        if [[ "$START_SERVICE" =~ ^[Yy]$ ]]; then
            sudo systemctl start roomba.service
            print_success "Service started"
            echo "Check status with: sudo systemctl status roomba.service"
        fi
    else
        print_warning "Systemd service not installed"
    fi
}

test_installation() {
    print_header "Testing Installation"

    echo "Running configuration test..."
    $PYTHON_CMD config.py

    print_success "Installation test passed"
}

print_completion() {
    print_header "Installation Complete!"

    echo ""
    echo "Next steps:"
    echo ""
    echo "1. Activate virtual environment:"
    echo "   source venv/bin/activate"
    echo ""
    echo "2. Test robot connection:"
    echo "   python -c 'from roomba import Create; r = Create(\"$USER_PORT\"); r.printSensors(); r.close()'"
    echo ""
    echo "3. Run Alexa integration:"
    echo "   python example-minimal.py"
    echo ""
    echo "4. Configure Alexa:"
    echo "   Say: 'Alexa, discover my devices'"
    echo "   Then: 'Alexa, turn on $USER_NAME'"
    echo ""

    if [[ "$INSTALL_SERVICE" =~ ^[Yy]$ ]]; then
        echo "Systemd service commands:"
        echo "   sudo systemctl start roomba.service"
        echo "   sudo systemctl stop roomba.service"
        echo "   sudo systemctl status roomba.service"
        echo "   journalctl -u roomba.service -f"
        echo ""
    fi

    echo "For more information, see README.md"
    echo ""
}

# Main installation flow
main() {
    print_header "Alexa Roomba Installer"
    echo ""
    echo "This script will:"
    echo "  • Check Python installation"
    echo "  • Create virtual environment"
    echo "  • Install dependencies"
    echo "  • Create configuration file"
    echo "  • Optionally set up systemd service"
    echo ""

    read -p "Continue with installation? (Y/n): " CONTINUE
    if [[ "$CONTINUE" =~ ^[Nn]$ ]]; then
        echo "Installation cancelled."
        exit 0
    fi

    check_python
    create_virtualenv
    install_dependencies
    create_config
    check_serial_permissions
    setup_systemd
    test_installation
    print_completion
}

# Run main installation
main
