#!/usr/bin/env python3
"""Verify configuration is correct"""

from src.config import Config

print("Loading configuration...")
config = Config()

print("\n" + "="*60)
print("CONFIGURATION VALIDATION")
print("="*60)

is_valid = config.validate()

if is_valid:
    print("✅ Configuration validation: PASSED")
else:
    print("❌ Configuration validation: FAILED")
    exit(1)

print("\n" + "="*60)
print("LOADED COMMANDS")
print("="*60)

for cmd_name, cmd_template in config.commands.items():
    placeholder_info = ""
    if cmd_name in config.player_required_commands:
        if "{player}" in cmd_template:
            placeholder_info = "✅ {player} required and present"
        else:
            placeholder_info = "❌ {player} MISSING!"
    elif cmd_name in config.global_commands:
        placeholder_info = "ℹ️  Global command (no {player} needed)"
    
    print(f"{cmd_name:12} | {cmd_template:40} | {placeholder_info}")

print("\n✅ All checks passed! Bot is ready to run.")
