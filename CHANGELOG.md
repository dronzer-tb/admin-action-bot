# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
### Changed
### Deprecated
### Removed
### Fixed
### Security

## [0.2.2] - 2025-11-09
### Added
- **Bot Channel Configuration** - Separate channel for bot commands vs audit logs
  - Added `DISCORD_BOT_CHANNEL_ID` configuration parameter
  - `/admin` command now only works in the designated bot channel
  - Keeps server organized by separating commands from logs
- Channel restriction validation - bot responds with helpful message if used in wrong channel
- Setup script now asks for both bot channel and audit channel IDs
- Better channel identification in logs and startup messages

### Changed
- Configuration now requires both `DISCORD_BOT_CHANNEL_ID` and `DISCORD_AUDIT_CHANNEL_ID`
- Bot startup logs now show both bot channel and audit channel names
- Setup script provides clearer explanation of channel purposes
- Updated all documentation to reflect two-channel architecture

### Technical
- Added `bot_channel` and `bot_channel_id` to Config class
- Added channel ID validation in `show_admin_panel()` method
- Updated tests to include bot channel ID in test environment
- All 8 tests still passing

## [0.2.1] - 2025-11-09
### Fixed
- **Critical Bug**: Freeze/unfreeze commands no longer require {player} placeholder
  - Changed default commands from `freeze {player}` to `tick freeze`
  - Changed default commands from `unfreeze {player}` to `tick unfreeze`
  - These are game-wide commands that affect all players, not individual targets
- Fixed IP ban command default from `ban-ip` to `ban` for EssentialsX compatibility
- Improved configuration validation to distinguish between player-targeted and global commands
- Setup script now validates command placeholders and asks for confirmation if missing
- Better error messages showing actual command values when validation fails

### Changed
- Updated PRD documentation to clarify freeze/unfreeze are game tick commands
- Updated bot UI descriptions for freeze/unfreeze actions
- Improved setup.sh with command validation function and retry loops
- Enhanced test suite with 8 total tests (added 2 new tests for freeze validation)

### Technical
- Added `player_required_commands` and `global_commands` categorization to Config class
- Commands requiring {player}: kill, kick, tempban, ipban, mute, warn
- Global commands (no {player} needed): freeze, unfreeze
- Fixed test isolation issues with environment variable mocking

## [0.2.0] - 2025-11-09
### Added
- Core Discord bot client with slash command support
- Configuration management system with environment variable validation
- Automated setup script (setup.sh) for easy VPS deployment
- Admin panel UI with 8 moderation action buttons
- Audit logging system for tracking all moderation actions
- Permission checking (admin role or administrator permission required)
- Basic project structure (src/, tests/)
- Test suite with 6 passing tests for configuration module
- Requirements.txt with all necessary dependencies
- .env.example template for easy configuration
- Main.py entry point with error handling

### Technical Details
- Discord.py 2.3+ integration with modern interactions API
- Button-based UI (View components)
- Ephemeral messages for admin commands
- Automatic slash command syncing to guild
- Comprehensive logging throughout application
- Virtual environment support in setup script
- Optional systemd service creation

## [0.1.0] - 2025-11-09
### Added
- Initial project structure
- Agent logging system
- Product Requirements Document (PRD)
- Version tracking system
- Changelog documentation
