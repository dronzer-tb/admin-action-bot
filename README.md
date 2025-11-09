# Admin Action Bot

![Version](https://img.shields.io/badge/version-1.1.0-blue)
![Python](https://img.shields.io/badge/python-3.9+-green)
![Discord.py](https://img.shields.io/badge/discord.py-2.3+-7289DA)
![Tests](https://img.shields.io/badge/tests-8%2F8%20passing-brightgreen)
![License](https://img.shields.io/badge/license-MIT-orange)
![Status](https://img.shields.io/badge/status-production%20ready-success)

**Version**: 1.1.0 🎉  
**Status**: ✅ Production Ready - Stable Release

## Overview

Admin Action Bot is a **production-ready** Discord-integrated Minecraft server administration tool that provides intuitive button-based moderation controls through Discord, connecting to Minecraft servers via the Pterodactyl API.

## 🚀 One-Line Installer

```bash
bash <(curl -s https://raw.githubusercontent.com/dronzer-tb/admin-action-bot/main/install.sh)
```

## ✨ Features

- 🎮 **Discord-Based Moderation** - Execute server commands without in-game access  
- 🔘 **Button Interface** - Intuitive, visual controls instead of text commands  
- 📋 **Interactive Modals** - Easy input forms for player names, reasons, and durations  
- 🎯 **Player Dropdown** - Auto-remembers last 25 players for quick selection (NEW in v1.1.0!)  
- ✅ **Real-Time Execution** - Commands execute instantly via Pterodactyl API  
- 📝 **Audit Logging** - Complete transparency with detailed action logs  
- 🔧 **Easy Setup** - Automated deployment script for quick VPS configuration  
- ⚙️ **Customizable** - Configure commands for your specific server setup  
- 🛡️ **Role-Based Access** - Admin role restrictions for security  
- 📍 **Channel Separation** - Dedicated channels for commands and audit logs  
- 🔄 **Persistent Buttons** - Buttons work even after bot restarts or Discord reconnections

## 🎯 Supported Moderation Actions (All Functional!)

| Action | Status | Description |
|--------|--------|-------------|
| 🔴 Kill | ✅ Working | Remove a player instantly |
| 👢 Kick | ✅ Working | Disconnect a player with reason |
| ⏰ Temp Ban | ✅ Working | Temporarily ban for specified duration (minutes) |
| 🚫 Ban | ✅ Working | Permanently ban player with reason |
| ❄️ Freeze | ✅ Working | Freeze game ticks (instant) |
| ✅ Unfreeze | ✅ Working | Unfreeze game ticks (instant) |

## Quick Start

### Prerequisites
- Linux VPS or local machine
- Python 3.9 or higher
- pip3 package manager
- Discord bot token ([Create one here](https://discord.com/developers/applications))
- Pterodactyl panel access with API key

### Installation

#### Option 1: One-Line Install (Recommended)
```bash
bash <(curl -s https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/install.sh)
```
> Replace `YOUR_USERNAME/YOUR_REPO` with your GitHub repository path.

This will automatically:
- ✅ Install all dependencies
- ✅ Create virtual environment
- ✅ Run interactive configuration
- ✅ Set up systemd service (optional)
- ✅ Start the bot

#### Option 2: Manual Installation

1. **Clone or download the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
   cd YOUR_REPO
   ```

2. **Run the automated setup script**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

3. **Follow the interactive prompts** to configure:
   - Discord Bot Token
   - Discord Server ID
   - **Bot Commands Channel ID** (where admins use /admin)
   - **Audit Log Channel ID** (where actions are logged)
   - Pterodactyl API credentials
   - Custom command mappings

4. **Start the bot**
   ```bash
   # Manually
   source venv/bin/activate
   python3 main.py
   
   # Or via systemd (if configured during setup)
   sudo systemctl start admin-action-bot
   sudo systemctl status admin-action-bot
   ```

### Discord Bot Setup

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to "Bot" section and create a bot
4. Enable these Privileged Gateway Intents:
   - Server Members Intent
   - Message Content Intent
5. Copy the bot token
6. Go to OAuth2 → URL Generator
7. Select scopes: `bot`, `applications.commands`
8. Select permissions:
   - Send Messages
   - Embed Links
   - Use Application Commands
   - Read Message History
9. Use the generated URL to invite the bot to your server

### Usage

In your Discord server, use the `/admin` command **in the designated bot channel** to open the admin panel. Select an action button to begin the moderation workflow.

**Important:** The `/admin` command only works in the channel you configured during setup. This keeps your server organized and prevents command spam in other channels.

**New in v1.1.0**: The bot now remembers the last 25 players you've moderated! After entering a player name once, they'll appear in a dropdown menu for quick selection.

## Project Structure

```
admin-action-bot/
├── docs/              # Documentation and PRD
├── logs/              # Agent activity logs
├── src/               # Source code (to be created)
├── tests/             # Test suite (to be created)
├── CHANGELOG.md       # Version history
├── README.md          # This file
└── VERSION            # Current version number
```

## Documentation

- [Product Requirements Document](./docs/PRD.md)
- [Changelog](./CHANGELOG.md)
- [Agent Activity Log](./logs/agent_log.md)

## Development

This project follows strict version control and logging protocols:
- Semantic versioning (MAJOR.MINOR.PATCH)
- All changes logged in agent_log.md
- Comprehensive testing before version increments
- PRD-driven development approach

## License

MIT License - see [LICENSE](LICENSE) file for details

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines and how to contribute to this project.

## Support

- **Documentation**: See [docs/PRD.md](docs/PRD.md)
- **Bug Reports**: Open an issue on GitHub
- **Feature Requests**: Check PRD first, then open an issue

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and changes.

## Project Status

- ✅ Core bot framework
- ✅ Automated setup
- ✅ Configuration management
- ✅ Dual-channel architecture
- ✅ Admin panel UI
- ✅ Audit logging framework
- ✅ Pterodactyl API integration
- ✅ Player dropdown selection
- ✅ Command execution (all 6 actions working)
- ✅ Full workflow (production ready)
- ✅ LibertyBan compatibility
- ✅ Persistent buttons
- ✅ Player caching system

---

**Made with ❤️ for Minecraft server administrators**
