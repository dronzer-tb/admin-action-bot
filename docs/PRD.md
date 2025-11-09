# Admin Action Bot - Product Requirements Document

**Version**: 0.2.2
**Last Updated**: 2025-11-09T08:27:22.532Z
**Status**: Active

## 1. Executive Summary

Admin Action Bot is a Discord-integrated Minecraft server administration tool that enables server administrators to manage player actions and enforce server rules through an intuitive button-based interface. The bot connects to Minecraft servers via the Pterodactyl API and provides real-time moderation capabilities with comprehensive audit logging.

## 2. Features & Requirements

### 2.1 Moderation Actions - Status: Planned
**Version Introduced**: 0.1.0
**Priority**: High
**Description**: Core moderation commands accessible through Discord interface

**Supported Commands**:
- Kill - Remove a player from the server instantly
- Kick - Disconnect a player from the server with optional reason
- Temp Ban - Temporarily ban a player for a specified duration (in minutes)
- IP Ban - Permanently ban a player by IP address
- Mute - Prevent a player from sending chat messages
- Warn - Issue a formal warning to a player (recorded in audit log)
- Tick Freeze - Freeze the entire game (stops all tick processing)
- Tick Unfreeze - Restore game tick processing

**Default Commands (EssentialsX)**:
- `kill {player}` - Kill specific player
- `kick {player} {reason}` - Kick player with reason
- `tempban {player} {duration}m {reason}` - Temporary ban with duration
- `ban {player} {reason}` - Permanent ban
- `mute {player} {reason}` - Mute player
- `warn {player} {reason}` - Warn player
- `tick freeze` - Freeze game ticks (no {player} placeholder - affects entire game)
- `tick unfreeze` - Unfreeze game ticks (no {player} placeholder - affects entire game)

**Acceptance Criteria**:
- [ ] All 8 moderation commands implemented
- [ ] Commands execute via Pterodactyl API successfully
- [ ] Error handling for failed command execution
- [ ] Feedback provided to administrator on success/failure
- [ ] All commands configurable per server setup

**Technical Notes**:
- Implementation via Discord.py or discord.js
- API integration with Pterodactyl
- MCP servers involved: context7 (for API documentation), test-sprite (for validation)

**Change History**:
- [0.1.0] - Feature planned and documented

---

### 2.2 User Selection Interface - Status: In Progress
**Version Introduced**: 0.2.0
**Priority**: High
**Description**: Button and dropdown-based interface for selecting players and actions

**Acceptance Criteria**:
- [x] Intuitive button layout for action selection
- [x] Color coding for action severity (red=dangerous, yellow=warnings)
- [ ] Dropdown list populated with active players
- [ ] Searchable/filterable player selection
- [ ] Display player information (username, join time, status)

**Technical Notes**:
- Discord embeds with interactive components ✅
- Button UI implemented with discord.ui.View ✅
- Real-time player list fetching from server (pending)
- MCP servers involved: context7 (Discord API best practices)

**Change History**:
- [0.1.0] - Feature planned and documented
- [0.2.0] - Button interface implemented, player selection pending

---

### 2.3 Action Workflow - Status: Planned
**Version Introduced**: 0.1.0
**Priority**: High
**Description**: Multi-step workflow with confirmation before execution

**Workflow Steps**:
1. Action Selection - Administrator selects moderation action via button
2. Player Selection - Administrator selects target player from dropdown
3. Reason Input - Administrator provides reason for action (text input)
4. Duration Input - For temp bans, administrator specifies duration in minutes
5. Confirmation - Bot displays summary and requests final confirmation
6. Execution - Action sent to Minecraft server via Pterodactyl API
7. Logging - Action recorded in audit log channel

**Acceptance Criteria**:
- [ ] All 7 workflow steps implemented
- [ ] Confirmation step prevents accidental actions
- [ ] Clear feedback at each step
- [ ] Timeout handling for inactive workflows
- [ ] Cancel option available at any step

**Technical Notes**:
- Discord modals/forms for input collection
- State management for multi-step flows
- MCP servers involved: sequential-thinking (workflow planning), test-sprite (flow validation)

**Change History**:
- [0.1.0] - Feature planned and documented

---

### 2.4 Audit Log - Status: In Progress
**Version Introduced**: 0.2.0
**Priority**: High
**Description**: Comprehensive logging of all moderation actions

**Acceptance Criteria**:
- [x] Dedicated Discord channel for audit logs
- [x] Log entries include: action type, target player, admin name, timestamp, reason, outcome
- [x] Structured log format in Discord embeds
- [ ] Searchable log history
- [ ] Filterable by action type, player, or administrator
- [ ] Automatic log retention and archival

**Technical Notes**:
- Structured log format in Discord embeds ✅
- Log method implemented in AdminBot class ✅
- Optional database backup of logs (pending)
- MCP servers involved: time (accurate timestamps), super-memory (log storage patterns)

**Change History**:
- [0.1.0] - Feature planned and documented
- [0.2.0] - Basic audit logging implemented, search/filter features pending

---

### 2.5 API Integration - Status: Planned
**Version Introduced**: 0.1.0
**Priority**: High
**Description**: Pterodactyl API connection for server command execution

**Acceptance Criteria**:
- [ ] Secure storage of API credentials
- [ ] Successful connection to Pterodactyl API
- [ ] Command execution through API
- [ ] Error handling and status feedback
- [ ] Support for custom command configurations per server

**Technical Notes**:
- Environment variable storage for credentials
- API authentication and request handling
- Retry logic for failed requests
- MCP servers involved: context7 (Pterodactyl API documentation)

**Change History**:
- [0.1.0] - Feature planned and documented

---

### 2.6 Setup & Deployment - Status: Completed
**Version Introduced**: 0.2.0
**Priority**: High
**Description**: Automated setup script for easy deployment

**Acceptance Criteria**:
- [x] Interactive setup script created
- [x] Script validates all inputs before saving
- [x] Creates necessary environment files and directories
- [x] Works on standard Linux VPS environments
- [x] Completes setup in under 5 minutes

**Configuration Parameters**:
- Discord Bot Token ✅
- Discord Server ID (Guild ID) ✅
- Discord Bot Channel ID ✅ (where /admin commands work)
- Discord Audit Log Channel ID ✅ (where actions are logged)
- Pterodactyl API URL ✅
- Pterodactyl API Key ✅
- Minecraft Server ID ✅
- Custom command mappings ✅
- Administrator role requirements ✅

**Technical Notes**:
- Bash script for setup automation ✅
- Virtual environment creation ✅
- Dependency installation ✅
- Optional systemd service creation ✅
- Input validation for all parameters ✅
- Docker support optional (future enhancement)
- MCP servers involved: sequential-thinking (setup flow planning)

**Change History**:
- [0.1.0] - Feature planned and documented
- [0.2.0] - Feature fully implemented and tested

---

## 3. Technical Architecture

**Programming Language**: Python (recommended) with Discord.py
**Alternative**: Node.js with discord.js

**Key Dependencies**:
- Discord.py or discord.js (Discord API library)
- Pterodactyl API client library
- python-dotenv or similar (environment variable management)
- SQLite (optional, for log backup)

**API Structure**:
- Discord Bot Gateway connection
- Pterodactyl RESTful API integration
- Command pattern for moderation actions
- State machine for workflow management

**Database Schema** (Optional):
- audit_logs table: id, timestamp, action_type, target_player, admin_id, reason, duration, outcome
- Configuration storage in environment files

---

## 4. Testing Requirements

**Unit Test Coverage Targets**: 80%+

**Test Categories**:
- Unit tests for individual moderation commands
- Integration tests for Discord interactions
- API integration tests with Pterodactyl (mocked)
- Workflow state management tests
- Error handling and edge case tests

**Performance Benchmarks**:
- Action execution within 2 seconds of confirmation
- Bot response time < 500ms for button clicks
- Setup script completion < 5 minutes

**MCP Server**: test-sprite will be used for test execution and validation

---

## 5. Deployment & Maintenance

**Deployment Process**:
1. Run setup script on VPS
2. Provide configuration details interactively
3. Script validates and creates environment
4. Start bot service
5. Verify connection to Discord and Pterodactyl

**Rollback Procedures**:
- Version-controlled configuration files
- Backup of .env before changes
- Bot restart command for quick recovery

**Monitoring and Alerts**:
- Bot online/offline status in Discord
- Error logging to dedicated channel
- API connection health checks

---

## 6. Version History

- **[0.2.0] - 2025-11-09** - Core bot implementation with setup automation
  - Implemented Discord bot client with slash commands
  - Created automated setup script (setup.sh)
  - Built configuration management system
  - Implemented admin panel UI with action buttons
  - Added audit logging framework
  - Created test suite with 6 passing tests
  - Completed setup & deployment feature (2.6)
  
- **[0.1.0] - 2025-11-09** - Initial PRD creation and project planning phase
