#!/bin/bash

################################################################################
# Admin Action Bot - Automated Setup Script
# Version: 0.2.0
# 
# This script automates the deployment and configuration of the Admin Action Bot
# on any VPS or Linux system.
################################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to validate input
validate_not_empty() {
    if [ -z "$1" ]; then
        return 1
    fi
    return 0
}

validate_url() {
    if [[ $1 =~ ^https?:// ]]; then
        return 0
    fi
    return 1
}

validate_numeric() {
    if [[ $1 =~ ^[0-9]+$ ]]; then
        return 0
    fi
    return 1
}

################################################################################
# Main Setup
################################################################################

echo -e "${GREEN}"
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                                                           ║"
echo "║          Admin Action Bot - Setup Wizard                 ║"
echo "║          Version 0.2.0                                   ║"
echo "║                                                           ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

print_info "This script will guide you through setting up the Admin Action Bot."
echo ""

# Check for Python
print_info "Checking for Python 3.9 or higher..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
print_success "Found Python $PYTHON_VERSION"

# Check for pip
print_info "Checking for pip..."
if ! command -v pip3 &> /dev/null; then
    print_error "pip3 is not installed. Please install pip3."
    exit 1
fi
print_success "pip3 is available"

echo ""
print_info "Starting configuration wizard..."
echo ""

################################################################################
# Discord Configuration
################################################################################

echo -e "${BLUE}=== Discord Configuration ===${NC}"
echo ""

# Discord Bot Token
while true; do
    read -p "Enter your Discord Bot Token: " DISCORD_BOT_TOKEN
    if validate_not_empty "$DISCORD_BOT_TOKEN"; then
        if [ ${#DISCORD_BOT_TOKEN} -ge 50 ]; then
            break
        else
            print_warning "Token seems too short. Please check and try again."
        fi
    else
        print_warning "Token cannot be empty."
    fi
done

# Discord Guild ID
while true; do
    read -p "Enter your Discord Server (Guild) ID: " DISCORD_GUILD_ID
    if validate_numeric "$DISCORD_GUILD_ID"; then
        break
    else
        print_warning "Guild ID must be a numeric value."
    fi
done

# Discord Bot Channel ID
while true; do
    read -p "Enter your Bot Commands Channel ID (where /admin will work): " DISCORD_BOT_CHANNEL_ID
    if validate_numeric "$DISCORD_BOT_CHANNEL_ID"; then
        break
    else
        print_warning "Channel ID must be a numeric value."
    fi
done

# Discord Audit Channel ID
while true; do
    read -p "Enter your Audit Log Channel ID (where actions are logged): " DISCORD_AUDIT_CHANNEL_ID
    if validate_numeric "$DISCORD_AUDIT_CHANNEL_ID"; then
        break
    else
        print_warning "Channel ID must be a numeric value."
    fi
done

echo ""

################################################################################
# Pterodactyl Configuration
################################################################################

echo -e "${BLUE}=== Pterodactyl Configuration ===${NC}"
echo ""

# Pterodactyl API URL
while true; do
    read -p "Enter your Pterodactyl Panel URL (e.g., https://panel.example.com): " PTERODACTYL_API_URL
    if validate_url "$PTERODACTYL_API_URL"; then
        # Remove trailing slash
        PTERODACTYL_API_URL=${PTERODACTYL_API_URL%/}
        break
    else
        print_warning "URL must start with http:// or https://"
    fi
done

# Pterodactyl API Key
while true; do
    read -p "Enter your Pterodactyl API Key: " PTERODACTYL_API_KEY
    if validate_not_empty "$PTERODACTYL_API_KEY"; then
        break
    else
        print_warning "API Key cannot be empty."
    fi
done

# Pterodactyl Server ID
while true; do
    read -p "Enter your Minecraft Server ID (from Pterodactyl): " PTERODACTYL_SERVER_ID
    if validate_not_empty "$PTERODACTYL_SERVER_ID"; then
        break
    else
        print_warning "Server ID cannot be empty."
    fi
done

echo ""

################################################################################
# Bot Configuration
################################################################################

echo -e "${BLUE}=== Bot Configuration ===${NC}"
echo ""

# Admin Role ID (optional)
read -p "Enter Admin Role ID (optional, press Enter to skip): " ADMIN_ROLE_ID
if [ -z "$ADMIN_ROLE_ID" ]; then
    print_info "No admin role specified. Only users with Administrator permission can use the bot."
fi

echo ""

################################################################################
# Command Configuration
################################################################################

echo -e "${BLUE}=== Command Configuration ===${NC}"
echo ""
print_info "Configure custom commands for your Minecraft server."
print_info "Default commands are for EssentialsX plugin."
echo ""
print_warning "IMPORTANT: Use placeholders in your commands:"
print_warning "  {player}   - Player name (required for most commands)"
print_warning "  {reason}   - Reason for action"
print_warning "  {duration} - Duration in minutes (for temp bans)"
echo ""
print_info "Press Enter to use default commands (recommended for EssentialsX)."
echo ""

# Function to validate and confirm command
validate_command() {
    local cmd_name=$1
    local cmd_value=$2
    local requires_player=$3
    
    if [ "$requires_player" = "true" ]; then
        if [[ ! "$cmd_value" =~ \{player\} ]]; then
            print_warning "WARNING: '$cmd_name' command does not contain {player} placeholder!"
            print_warning "Current value: $cmd_value"
            read -p "This may not work correctly. Use this command anyway? (y/N): " confirm
            if [[ ! $confirm =~ ^[Yy]$ ]]; then
                return 1
            fi
        fi
    fi
    return 0
}

read -p "Kill command [default: kill {player}]: " CMD_KILL
CMD_KILL=${CMD_KILL:-"kill {player}"}
while ! validate_command "kill" "$CMD_KILL" "true"; do
    read -p "Kill command [default: kill {player}]: " CMD_KILL
    CMD_KILL=${CMD_KILL:-"kill {player}"}
done

read -p "Kick command [default: kick {player} {reason}]: " CMD_KICK
CMD_KICK=${CMD_KICK:-"kick {player} {reason}"}
while ! validate_command "kick" "$CMD_KICK" "true"; do
    read -p "Kick command [default: kick {player} {reason}]: " CMD_KICK
    CMD_KICK=${CMD_KICK:-"kick {player} {reason}"}
done

read -p "Temp Ban command [default: tempban {player} {duration}m {reason}]: " CMD_TEMPBAN
CMD_TEMPBAN=${CMD_TEMPBAN:-"tempban {player} {duration}m {reason}"}
while ! validate_command "tempban" "$CMD_TEMPBAN" "true"; do
    read -p "Temp Ban command [default: tempban {player} {duration}m {reason}]: " CMD_TEMPBAN
    CMD_TEMPBAN=${CMD_TEMPBAN:-"tempban {player} {duration}m {reason}"}
done

read -p "IP Ban command [default: ban {player} {reason}]: " CMD_IPBAN
CMD_IPBAN=${CMD_IPBAN:-"ban {player} {reason}"}
while ! validate_command "ipban" "$CMD_IPBAN" "true"; do
    read -p "IP Ban command [default: ban {player} {reason}]: " CMD_IPBAN
    CMD_IPBAN=${CMD_IPBAN:-"ban {player} {reason}"}
done

read -p "Mute command [default: mute {player} {reason}]: " CMD_MUTE
CMD_MUTE=${CMD_MUTE:-"mute {player} {reason}"}
while ! validate_command "mute" "$CMD_MUTE" "true"; do
    read -p "Mute command [default: mute {player} {reason}]: " CMD_MUTE
    CMD_MUTE=${CMD_MUTE:-"mute {player} {reason}"}
done

read -p "Warn command [default: warn {player} {reason}]: " CMD_WARN
CMD_WARN=${CMD_WARN:-"warn {player} {reason}"}
while ! validate_command "warn" "$CMD_WARN" "true"; do
    read -p "Warn command [default: warn {player} {reason}]: " CMD_WARN
    CMD_WARN=${CMD_WARN:-"warn {player} {reason}"}
done

echo ""
print_info "Game-wide commands (these freeze/unfreeze the entire game, not individual players):"

read -p "Freeze Game command [default: tick freeze]: " CMD_FREEZE
CMD_FREEZE=${CMD_FREEZE:-"tick freeze"}

read -p "Unfreeze Game command [default: tick unfreeze]: " CMD_UNFREEZE
CMD_UNFREEZE=${CMD_UNFREEZE:-"tick unfreeze"}

echo ""

################################################################################
# Create .env file
################################################################################

print_info "Creating .env configuration file..."

# Remove old .env files if they exist
if [ -f ".env" ]; then
    print_warning "Existing .env file found. Creating backup..."
    mv .env .env.backup.$(date +%Y%m%d_%H%M%S)
    print_success "Old .env file backed up"
fi

# Remove any old backup files older than 7 days
find . -maxdepth 1 -name ".env.backup.*" -mtime +7 -delete 2>/dev/null

cat > .env << EOF
# Discord Configuration
DISCORD_BOT_TOKEN=$DISCORD_BOT_TOKEN
DISCORD_GUILD_ID=$DISCORD_GUILD_ID
DISCORD_BOT_CHANNEL_ID=$DISCORD_BOT_CHANNEL_ID
DISCORD_AUDIT_CHANNEL_ID=$DISCORD_AUDIT_CHANNEL_ID

# Pterodactyl Configuration
PTERODACTYL_API_URL=$PTERODACTYL_API_URL
PTERODACTYL_API_KEY=$PTERODACTYL_API_KEY
PTERODACTYL_SERVER_ID=$PTERODACTYL_SERVER_ID

# Bot Configuration
${ADMIN_ROLE_ID:+ADMIN_ROLE_ID=$ADMIN_ROLE_ID}
COMMAND_PREFIX=!

# Custom Minecraft Commands
CMD_KILL=$CMD_KILL
CMD_KICK=$CMD_KICK
CMD_TEMPBAN=$CMD_TEMPBAN
CMD_IPBAN=$CMD_IPBAN
CMD_MUTE=$CMD_MUTE
CMD_WARN=$CMD_WARN
CMD_FREEZE=$CMD_FREEZE
CMD_UNFREEZE=$CMD_UNFREEZE
EOF

print_success ".env file created successfully"

################################################################################
# Install Dependencies
################################################################################

echo ""
print_info "Installing Python dependencies..."

# Create virtual environment
if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_success "Virtual environment created"
else
    print_info "Virtual environment already exists"
fi

# Activate virtual environment and install requirements
source venv/bin/activate
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt

print_success "Dependencies installed successfully"

################################################################################
# Create systemd service (optional)
################################################################################

echo ""
read -p "Do you want to create a systemd service for auto-start? (y/N): " CREATE_SERVICE

if [[ $CREATE_SERVICE =~ ^[Yy]$ ]]; then
    SERVICE_NAME="admin-action-bot"
    WORK_DIR=$(pwd)
    USER=$(whoami)
    
    print_info "Creating systemd service..."
    
    sudo tee /etc/systemd/system/${SERVICE_NAME}.service > /dev/null << EOF
[Unit]
Description=Admin Action Bot - Discord Minecraft Admin Tool
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$WORK_DIR
Environment="PATH=$WORK_DIR/venv/bin"
ExecStart=$WORK_DIR/venv/bin/python3 $WORK_DIR/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
    
    sudo systemctl daemon-reload
    sudo systemctl enable ${SERVICE_NAME}
    
    print_success "Systemd service created: ${SERVICE_NAME}"
    print_info "Start with: sudo systemctl start ${SERVICE_NAME}"
    print_info "Check status: sudo systemctl status ${SERVICE_NAME}"
    print_info "View logs: sudo journalctl -u ${SERVICE_NAME} -f"
fi

################################################################################
# Final Summary
################################################################################

echo ""
echo -e "${GREEN}"
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                                                           ║"
echo "║          Setup Complete! 🎉                              ║"
echo "║                                                           ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

print_success "Admin Action Bot is configured and ready to run!"
echo ""
print_info "To start the bot manually:"
echo "  source venv/bin/activate"
echo "  python3 main.py"
echo ""

if [[ $CREATE_SERVICE =~ ^[Yy]$ ]]; then
    print_info "Or start the systemd service:"
    echo "  sudo systemctl start admin-action-bot"
    echo ""
fi

print_info "Configuration saved in: .env"
print_info "Bot commands channel: $DISCORD_BOT_CHANNEL_ID (use /admin here)"
print_info "Audit logs channel: $DISCORD_AUDIT_CHANNEL_ID (actions logged here)"
echo ""

print_warning "Important: Make sure your Discord bot has the following permissions:"
print_warning "  - Send Messages"
print_warning "  - Embed Links"
print_warning "  - Use Application Commands"
print_warning "  - Read Message History"
echo ""

print_info "Use /admin in your Discord server to open the admin panel"
echo ""

print_success "Setup complete! Happy moderating! 🛡️"
