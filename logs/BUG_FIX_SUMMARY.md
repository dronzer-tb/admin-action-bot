# Bug Fix Summary - Version 0.2.1

## Issue Reported
Configuration validation was failing with errors about missing `{player}` placeholders in freeze/unfreeze commands and other commands.

## Root Cause
1. **Freeze/Unfreeze commands** were incorrectly configured to require `{player}` placeholder
   - These are game-wide commands (`tick freeze`/`tick unfreeze`) that affect the entire game, not individual players
   - Previous validation required ALL commands to have `{player}` placeholder

2. **Incorrect default commands** in .env.example and user's .env file
   - `CMD_KILL` had `/kill` instead of `kill {player}`
   - `CMD_IPBAN` had `ipban` instead of `ban {player} {reason}`
   - `CMD_WARN` had `ipwarn` instead of `warn {player} {reason}`

## Fixes Applied

### 1. Configuration Validation (src/config.py)
- ✅ Added command categorization:
  - **Player-required commands**: kill, kick, tempban, ipban, mute, warn
  - **Global commands**: freeze, unfreeze
- ✅ Updated validation to only check `{player}` for player-required commands
- ✅ Improved error messages to show current command value

### 2. Default Commands (.env.example)
- ✅ Fixed all default commands for EssentialsX plugin
- ✅ Changed `freeze {player}` → `tick freeze`
- ✅ Changed `unfreeze {player}` → `tick unfreeze`
- ✅ Changed `ban-ip {player} {reason}` → `ban {player} {reason}`

### 3. Setup Script (setup.sh)
- ✅ Added `validate_command()` function
- ✅ Warns users if player-required commands are missing `{player}` placeholder
- ✅ Asks for confirmation before accepting invalid commands
- ✅ Retry loops for each command until valid
- ✅ Better documentation about placeholders

### 4. Documentation Updates
- ✅ PRD updated to clarify freeze/unfreeze are game-wide commands
- ✅ Bot UI text updated ("Stop game ticks" instead of "Stop movement")
- ✅ README unchanged (no user-facing impact)

### 5. Tests
- ✅ Added 2 new tests for freeze command validation
- ✅ Fixed 1 existing test for environment isolation
- ✅ All 8 tests now passing (100%)

### 6. User's .env File
- ✅ Created `fix_env.sh` script to automatically fix incorrect commands
- ✅ Backup created as `.env.backup`
- ✅ All commands now validated and working

## Verification

Run this to verify your configuration:
```bash
python3 verify_config.py
```

Expected output:
```
✅ Configuration validation: PASSED
✅ All checks passed! Bot is ready to run.
```

## Testing
All tests passing:
```bash
python3 -m pytest tests/test_config.py -v
# Result: 8 passed
```

## Version Change
- 0.2.0 → **0.2.1** (PATCH - bug fix only)

## Files Modified
1. `src/config.py` - Validation logic
2. `.env.example` - Default commands
3. `setup.sh` - Command validation
4. `docs/PRD.md` - Documentation
5. `src/bot.py` - UI text
6. `tests/test_config.py` - Test suite
7. `VERSION` - Version number
8. `CHANGELOG.md` - Release notes
9. `.env` - Your configuration (via fix_env.sh)

## Commands Reference

### EssentialsX Default Commands

**Player-Targeted Commands** (require `{player}` placeholder):
```bash
CMD_KILL=kill {player}
CMD_KICK=kick {player} {reason}
CMD_TEMPBAN=tempban {player} {duration}m {reason}
CMD_IPBAN=ban {player} {reason}
CMD_MUTE=mute {player} {reason}
CMD_WARN=warn {player} {reason}
```

**Game-Wide Commands** (NO `{player}` placeholder):
```bash
CMD_FREEZE=tick freeze
CMD_UNFREEZE=tick unfreeze
```

## Next Steps

Your bot is now ready to run! Start it with:
```bash
source venv/bin/activate
python3 main.py
```

Or use the systemd service if you configured it:
```bash
sudo systemctl start admin-action-bot
sudo systemctl status admin-action-bot
```

## Notes
- The freeze/unfreeze commands affect the **entire game server**, not individual players
- If you want to freeze individual players, you'll need different plugin commands
- All placeholders (`{player}`, `{reason}`, `{duration}`) are now properly documented
- Setup script will now warn you if you configure commands incorrectly
