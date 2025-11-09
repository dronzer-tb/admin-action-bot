#!/bin/bash
# One-line installer for Admin Action Bot
# Usage: bash <(curl -s https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/install.sh)

set -e  # Exit on error

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
REPO_URL="https://github.com/YOUR_USERNAME/YOUR_REPO.git"
INSTALL_DIR="$HOME/admin-action-bot"
SERVICE_NAME="admin-action-bot"

# Functions
print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_header() {
    echo -e "${BLUE}$1${NC}"
}

# Header
clear
echo "╔════════════════════════════════════════════════╗"
echo "║   Admin Action Bot - One-Line Installer       ║"
echo "║              Version 1.1.0                     ║"
echo "╚════════════════════════════════════════════════╝"
echo ""

# Check prerequisites
print_header "Checking prerequisites..."
echo ""

# Check for curl/wget
if ! command -v curl &> /dev/null && ! command -v wget &> /dev/null; then
    print_error "curl or wget is required but not installed"
    exit 1
fi
print_success "Found download tool"

# Check for git
if ! command -v git &> /dev/null; then
    print_error "git is required but not installed"
    echo "  Install: sudo apt install git -y"
    exit 1
fi
print_success "Found git"

# Check for Python 3.9+
if ! command -v python3 &> /dev/null; then
    print_error "Python 3.9+ is required but not installed"
    echo "  Install: sudo apt install python3 python3-pip python3-venv -y"
    exit 1
fi

python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.9"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    print_error "Python 3.9+ required, found Python $python_version"
    exit 1
fi
print_success "Found Python $python_version"

# Check for pip
if ! command -v pip3 &> /dev/null; then
    print_error "pip3 is required but not installed"
    echo "  Install: sudo apt install python3-pip -y"
    exit 1
fi
print_success "Found pip3"

echo ""
print_header "Installation Options"
echo ""
echo "1) Install to $HOME/admin-action-bot (recommended)"
echo "2) Install to custom directory"
echo "3) Install to /opt/admin-action-bot (system-wide, requires sudo)"
echo ""
read -p "Choose option [1-3]: " install_option

case $install_option in
    1)
        INSTALL_DIR="$HOME/admin-action-bot"
        ;;
    2)
        read -p "Enter installation directory: " INSTALL_DIR
        INSTALL_DIR="${INSTALL_DIR/#\~/$HOME}"  # Expand ~
        ;;
    3)
        INSTALL_DIR="/opt/admin-action-bot"
        if [ "$EUID" -ne 0 ]; then
            print_error "System-wide installation requires sudo"
            exit 1
        fi
        ;;
    *)
        print_error "Invalid option"
        exit 1
        ;;
esac

echo ""
print_header "Installing to: $INSTALL_DIR"
echo ""

# Clone repository
print_warning "Cloning repository..."
if [ -d "$INSTALL_DIR" ]; then
    read -p "Directory exists. Overwrite? (y/N): " overwrite
    if [[ $overwrite =~ ^[Yy]$ ]]; then
        rm -rf "$INSTALL_DIR"
    else
        print_error "Installation cancelled"
        exit 1
    fi
fi

git clone "$REPO_URL" "$INSTALL_DIR" 2>&1 | grep -v "Cloning into" || true
cd "$INSTALL_DIR"
print_success "Repository cloned"

# Create virtual environment
print_warning "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate
print_success "Virtual environment created"

# Install dependencies
print_warning "Installing dependencies..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt > /dev/null 2>&1
print_success "Dependencies installed"

echo ""
print_header "Configuration"
echo ""
print_warning "Starting interactive configuration..."
echo ""

# Make setup.sh executable and run it
chmod +x setup.sh
./setup.sh

# Verify configuration
print_warning "Verifying configuration..."
if python3 verify_config.py > /dev/null 2>&1; then
    print_success "Configuration verified"
else
    print_error "Configuration verification failed!"
    exit 1
fi

echo ""
print_header "Service Setup"
echo ""
read -p "Install as systemd service for auto-start? (Y/n): " install_service

if [[ ! $install_service =~ ^[Nn]$ ]]; then
    CURRENT_USER=$(whoami)
    
    # Create systemd service file
    print_warning "Creating systemd service..."
    
    sudo tee /etc/systemd/system/${SERVICE_NAME}.service > /dev/null << EOF
[Unit]
Description=Admin Action Discord Bot for Minecraft Server Moderation
After=network.target

[Service]
Type=simple
User=$CURRENT_USER
WorkingDirectory=$INSTALL_DIR
Environment="PATH=$INSTALL_DIR/venv/bin"
ExecStart=$INSTALL_DIR/venv/bin/python3 $INSTALL_DIR/main.py
Restart=always
RestartSec=10
StandardOutput=append:$INSTALL_DIR/logs/bot.log
StandardError=append:$INSTALL_DIR/logs/bot.log

[Install]
WantedBy=multi-user.target
EOF

    sudo systemctl daemon-reload
    print_success "Service created"
    
    # Enable and start service
    sudo systemctl enable ${SERVICE_NAME} > /dev/null 2>&1
    print_success "Service enabled (auto-start on boot)"
    
    print_warning "Starting service..."
    sudo systemctl start ${SERVICE_NAME}
    sleep 3
    
    if sudo systemctl is-active --quiet ${SERVICE_NAME}; then
        print_success "Service started successfully!"
        SERVICE_INSTALLED=true
    else
        print_error "Service failed to start"
        echo "  Check logs: sudo journalctl -u ${SERVICE_NAME} -n 50"
        SERVICE_INSTALLED=false
    fi
else
    SERVICE_INSTALLED=false
fi

# Security hardening
print_warning "Securing configuration..."
chmod 600 .env
mkdir -p logs cache
chmod 755 logs cache
print_success "Security hardening complete"

echo ""
echo "════════════════════════════════════════════════"
echo " ✅ Installation Complete!"
echo "════════════════════════════════════════════════"
echo ""
print_success "Admin Action Bot v1.1.0 installed successfully!"
echo ""
echo "📍 Installation Directory: $INSTALL_DIR"
echo ""

if [ "$SERVICE_INSTALLED" = true ]; then
    echo "📊 Service Status: ${GREEN}● Running${NC}"
    echo ""
    echo "📝 Useful Commands:"
    echo "  View logs:     sudo journalctl -u ${SERVICE_NAME} -f"
    echo "  Restart:       sudo systemctl restart ${SERVICE_NAME}"
    echo "  Stop:          sudo systemctl stop ${SERVICE_NAME}"
    echo "  Status:        sudo systemctl status ${SERVICE_NAME}"
else
    echo "📊 Service Status: ${YELLOW}Manual Mode${NC}"
    echo ""
    echo "📝 To Start Bot:"
    echo "  cd $INSTALL_DIR"
    echo "  source venv/bin/activate"
    echo "  python3 main.py"
fi

echo ""
echo "🎯 Next Steps:"
echo "  1. Test bot in Discord: Run /admin in your bot channel"
echo "  2. Try the new player dropdown feature!"
echo "  3. Check audit logs in your designated channel"
echo ""
echo "📚 Documentation:"
echo "  README:        $INSTALL_DIR/README.md"
echo "  Features:      $INSTALL_DIR/PLAYER_DROPDOWN_FEATURE.md"
echo "  Changelog:     $INSTALL_DIR/CHANGELOG.md"
echo ""
print_success "Happy moderating! 🎉"
