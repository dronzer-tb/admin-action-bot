# Admin Action Bot

![Version](https://img.shields.io/badge/version-0.2.2-blue)
![Python](https://img.shields.io/badge/python-3.9+-green)
![Discord.py](https://img.shields.io/badge/discord.py-2.3+-7289DA)
![Tests](https://img.shields.io/badge/tests-8%2F8%20passing-brightgreen)
![License](https://img.shields.io/badge/license-MIT-orange)

**Version**: 0.2.2  
**Status**: In Development

## Overview

Admin Action Bot is a Discord-integrated Minecraft server administration tool that provides intuitive button-based moderation controls through Discord, connecting to Minecraft servers via the Pterodactyl API.

## Features

- 🎮 **Discord-Based Moderation** - Execute server commands without in-game access
- 🔘 **Button Interface** - Intuitive, visual controls instead of text commands
- ✅ **Confirmation Steps** - Prevent accidental actions with built-in confirmations
- 📝 **Audit Logging** - Complete transparency with comprehensive action logs
- 🔧 **Easy Setup** - Automated deployment script for quick VPS configuration
- ⚙️ **Customizable** - Configure commands for your specific server setup

## Supported Moderation Actions

- Kill - Remove a player instantly
- Kick - Disconnect a player with optional reason
- Temp Ban - Temporarily ban for specified duration
- IP Ban - Permanently ban by IP address
- Mute - Prevent chat messages
- Warn - Issue formal warnings
- Tick Freeze/Unfreeze - Control player movement

## Quick Start

### Prerequisites
- Linux VPS or local machine
- Python 3.9 or higher
- pip3 package manager
- Discord bot token ([Create one here](https://discord.com/developers/applications))
- Pterodactyl panel access with API key

### Installation

1. **Clone or download the repository**
   ```bash
   cd /path/to/admin-action-bot
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

**Note**: Currently, action buttons show "not yet implemented" messages. Full functionality will be added in version 0.3.0.

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
- ⏳ Pterodactyl API integration (v0.3.0)
- ⏳ Player selection (v0.3.0)
- ⏳ Command execution (v0.3.0)
- ⏳ Full workflow (v0.3.0)

---

**Made with ❤️ for Minecraft server administrators**
