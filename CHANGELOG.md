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

## [1.1.0] - 2025-11-09 🎯 PLAYER DROPDOWN FEATURE
### Added
- **🎯 Player Dropdown Selection** - Automatic player list for faster moderation!
  - Caches last 25 unique players used in commands
  - Shows dropdown menu when clicking action buttons
  - No need to type usernames anymore - just select from list!
  - "Enter Manually" option for players not in cache
  - Smart caching: Most recently used players appear first
  
- **Player Cache System**:
  - `add_recent_player()` - Automatically adds players to cache
  - `get_recent_players()` - Retrieves cached player list
  - Players added to cache whenever action is executed
  - Cache persists during bot runtime (resets on restart)
  - Maximum 25 players (Discord dropdown limit)

- **New UI Components**:
  - `PlayerSelectionView` - Shows player dropdown + manual input button
  - `PlayerDropdown` - Discord select menu with recent players
  - `ManualPlayerInputModal` - Fallback for manual player entry
  - Enhanced `PlayerActionModal` - Detects if cache available

### Changed
- **Improved Workflow**: 
  1. Click action button (e.g., "Kick")
  2. Enter reason/duration in modal
  3. Click Submit
  4. **NEW**: Player dropdown appears with recent players!
  5. Select player from list or click "Enter Manually"
  6. Action executes immediately
  
- **First-Time Experience**: 
  - No cached players yet? Shows manual input (same as before)
  - After first action, player is cached for future use
  - Each successful action adds player to cache
  
### Technical
- Added `recent_players` list to `AdminBot` class
- Maximum cache size: 25 players (configurable via `max_recent_players`)
- Player added to cache in `_execute_action()` method
- Dropdown automatically populated from cache
- Manual input always available as fallback

## [1.0.0] - 2025-11-09 🎉 STABLE RELEASE
### Fixed
- **CRITICAL**: Fixed persistent interaction timeout errors after Discord reconnection
  - Changed view timeout from 300 seconds to `None` (persistent view)
  - Added `custom_id` to all buttons for persistence across bot restarts
  - Buttons now work even after Discord gateway reconnection/resume
  
- **Network Resilience**: Improved Pterodactyl API timeout handling
  - Increased timeout from 10 seconds to 30 seconds
  - Added specific `asyncio.TimeoutError` exception handling
  - Better error messages for timeout scenarios
  
### Removed
- **Removed Mute action** - User requested removal (not needed for their server)
- **Removed Warn action** - User requested removal (using LibertyBan, not EssentialsX)
- **Removed IP Ban action** - Replaced with standard Ban (LibertyBan compatibility)

### Changed
- **Renamed "IP Ban" to "Ban"** - Now uses standard permanent ban command
- **Updated command templates** for LibertyBan plugin compatibility:
  - `CMD_BAN=ban {player} {reason}` (was CMD_IPBAN=ipban {player} {reason})
  - Removed CMD_MUTE and CMD_WARN from configuration
- **Reduced button count** from 8 to 6 actions (cleaner UI)
- Updated all documentation to reflect 6 actions instead of 8
- Updated setup script to ask for 6 commands instead of 8

### Technical
- View persistence: `timeout=None` prevents button expiration
- Custom IDs format: `admin_action:{action_name}` for stateless button handling
- Better async timeout handling with separate TimeoutError catch block
- Configuration now only validates 4 player-required commands (kill, kick, tempban, ban)

## [0.3.0] - 2025-11-09
### Added
- **🎉 MAJOR**: Full Pterodactyl API integration - all actions now functional!
  - Created `src/pterodactyl.py` - Complete API client with error handling
  - `send_command()` - Executes commands on Minecraft server
  - `get_server_status()` - Retrieves server status and resources
  - `test_connection()` - Validates API credentials on startup
  - Automatic connection test when bot starts
  
- **Interactive Modals** for player-targeted actions:
  - Player name input field (max 16 characters)
  - Reason input field (for kick, ban, mute, warn)
  - Duration input field (for temp bans, in minutes)
  - Input validation and error handling
  
- **Command Execution** - All 8 actions now work:
  - ✅ Kill - Instant player removal with modal input
  - ✅ Kick - Disconnect player with reason
  - ✅ Temp Ban - Temporary ban with duration and reason
  - ✅ IP Ban - Permanent ban with reason
  - ✅ Mute - Prevent chat with reason
  - ✅ Warn - Issue warning with reason
  - ✅ Freeze - Instant game freeze (no modal needed)
  - ✅ Unfreeze - Instant game unfreeze (no modal needed)
  
- **Enhanced Audit Logging** - Now logs actual execution results:
  - Success/failure status with color coding (green/red)
  - Error messages for failed commands
  - All parameters (player, reason, duration)
  - Timestamp and admin ID for accountability

### Fixed
- **CRITICAL**: Fixed interaction timeout by moving defer to command decorator
  - Defer now happens in `admin_panel()` before calling `show_admin_panel()`
  - Added try/catch for already-expired interactions
  - Better error logging for timeout issues
  
### Changed
- Button handlers now open modals instead of showing "not implemented" messages
- Freeze/Unfreeze buttons execute immediately without modal (global game commands)
- All command formatting now uses `Config.get_command()` method
- Bot now tests Pterodactyl connection on startup

### Technical
- Added PterodactylClient class with async/await support
- HTTP timeout set to 10 seconds for API calls
- Proper error handling for network issues, auth failures, server not found
- Modal input validation for duration (must be positive integer)
- Player name validation (max 16 characters per Minecraft spec)

## [0.2.3] - 2025-11-09
### Fixed
- **CRITICAL**: Fixed "Unknown interaction" error (Discord 10062) that prevented `/admin` command from working
  - Added `await interaction.response.defer()` at start of `show_admin_panel()` to acknowledge interaction within 3 seconds
  - Changed all `interaction.response.send_message()` calls to `interaction.followup.send()` after deferral
  - This prevents Discord's 3-second interaction timeout when processing validation checks

### Added
- Welcome message posted to bot channel on startup showing:
  - Available commands and how to use them
  - List of all 8 moderation actions with descriptions
  - Bot version and configuration information
  - Helps users discover bot features without reading documentation
- Updated bot status to show `/admin` command hint in presence

### Technical Details
- Discord interactions must be acknowledged within 3 seconds or they expire
- `defer()` extends response time from 3 seconds to 15 minutes
- Using `followup.send()` after deferral instead of `response.send_message()`
- See `INTERACTION_TIMEOUT_FIX.md` for detailed technical analysis

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
