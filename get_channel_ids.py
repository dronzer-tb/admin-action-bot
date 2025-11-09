#!/usr/bin/env python3
"""
Helper script to display Discord channel information
Helps users find channel IDs for configuration
"""

import sys

print("""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║       How to Get Discord Channel IDs                     ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝

Step 1: Enable Developer Mode in Discord
  1. Open Discord
  2. Go to User Settings (gear icon)
  3. Go to Advanced
  4. Enable "Developer Mode"

Step 2: Get Channel IDs
  1. Right-click on any channel
  2. Click "Copy Channel ID"
  3. Paste it into your .env file or setup script

You need TWO channel IDs:

1. Bot Commands Channel (DISCORD_BOT_CHANNEL_ID)
   - This is where admins will use the /admin command
   - Recommended: Create a private channel like #admin-bot
   - Only admins should have access to this channel
   
2. Audit Log Channel (DISCORD_AUDIT_CHANNEL_ID)
   - This is where all moderation actions will be logged
   - Recommended: Create a read-only channel like #admin-logs
   - Admins can read, but actions are logged automatically
   - Provides transparency and accountability

Example Configuration:
  DISCORD_BOT_CHANNEL_ID=1234567890123456789
  DISCORD_AUDIT_CHANNEL_ID=9876543210987654321

Tip: You can use the same channel for both, but it's better to keep
them separate to avoid clutter!

""")

# Check if .env exists and show current configuration
try:
    with open('.env', 'r') as f:
        env_content = f.read()
        
    print("Your current configuration:")
    print("="*60)
    
    for line in env_content.split('\n'):
        if 'DISCORD_BOT_CHANNEL_ID' in line or 'DISCORD_AUDIT_CHANNEL_ID' in line:
            print(f"  {line}")
    
    print("="*60)
    print()
    
except FileNotFoundError:
    print("⚠️  No .env file found. Run ./setup.sh to create one.")
    print()
