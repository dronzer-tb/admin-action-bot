"""
Configuration management for Admin Action Bot
Loads and validates environment variables and configuration
"""

import os
from typing import Dict, Optional
from dotenv import load_dotenv


class Config:
    """Configuration loader and validator"""
    
    def __init__(self):
        """Load configuration from environment variables"""
        load_dotenv()
        
        # Discord Configuration
        self.discord_token: str = self._get_required("DISCORD_BOT_TOKEN")
        self.guild_id: int = int(self._get_required("DISCORD_GUILD_ID"))
        self.bot_channel_id: int = int(self._get_required("DISCORD_BOT_CHANNEL_ID"))
        self.audit_channel_id: int = int(self._get_required("DISCORD_AUDIT_CHANNEL_ID"))
        
        # Pterodactyl Configuration
        self.pterodactyl_url: str = self._get_required("PTERODACTYL_API_URL").rstrip('/')
        self.pterodactyl_key: str = self._get_required("PTERODACTYL_API_KEY")
        self.server_id: str = self._get_required("PTERODACTYL_SERVER_ID")
        
        # Bot Configuration
        self.admin_role_id: Optional[int] = self._get_optional_int("ADMIN_ROLE_ID")
        self.command_prefix: str = os.getenv("COMMAND_PREFIX", "!")
        
        # Custom Command Mappings
        self.commands: Dict[str, str] = {
            "kill": os.getenv("CMD_KILL", "kill {player}"),
            "kick": os.getenv("CMD_KICK", "kick {player} {reason}"),
            "tempban": os.getenv("CMD_TEMPBAN", "tempban {player} {duration}m {reason}"),
            "ipban": os.getenv("CMD_IPBAN", "ban {player} {reason}"),
            "mute": os.getenv("CMD_MUTE", "mute {player} {reason}"),
            "warn": os.getenv("CMD_WARN", "warn {player} {reason}"),
            "freeze": os.getenv("CMD_FREEZE", "tick freeze"),
            "unfreeze": os.getenv("CMD_UNFREEZE", "tick unfreeze"),
        }
        
        # Commands that require {player} placeholder
        self.player_required_commands = ["kill", "kick", "tempban", "ipban", "mute", "warn"]
        # Commands that don't require {player} (game-wide commands)
        self.global_commands = ["freeze", "unfreeze"]
    
    def _get_required(self, key: str) -> str:
        """Get required environment variable or raise error"""
        value = os.getenv(key)
        if not value:
            raise ValueError(f"Required environment variable '{key}' is not set")
        return value
    
    def _get_optional_int(self, key: str) -> Optional[int]:
        """Get optional integer environment variable"""
        value = os.getenv(key)
        return int(value) if value else None
    
    def validate(self) -> bool:
        """Validate configuration values"""
        errors = []
        
        # Validate Discord token format (basic check)
        if len(self.discord_token) < 50:
            errors.append("DISCORD_BOT_TOKEN appears to be invalid (too short)")
        
        # Validate Pterodactyl URL
        if not self.pterodactyl_url.startswith(('http://', 'https://')):
            errors.append("PTERODACTYL_API_URL must start with http:// or https://")
        
        # Validate command templates based on command type
        for cmd_name, cmd_template in self.commands.items():
            # Commands that target specific players must have {player} placeholder
            if cmd_name in self.player_required_commands:
                if "{player}" not in cmd_template:
                    errors.append(
                        f"Command template for '{cmd_name}' must include {{player}} placeholder. "
                        f"Current: '{cmd_template}'"
                    )
            # Global commands (freeze/unfreeze) don't need {player}
            # No validation needed for global commands
        
        if errors:
            print("Configuration validation errors:")
            for error in errors:
                print(f"  - {error}")
            return False
        
        return True
    
    def get_command(self, action: str, **kwargs) -> str:
        """
        Get formatted command for a specific action
        
        Args:
            action: The moderation action (kill, kick, tempban, etc.)
            **kwargs: Parameters to format into the command template
        
        Returns:
            Formatted command string
        """
        template = self.commands.get(action)
        if not template:
            raise ValueError(f"Unknown action: {action}")
        
        return template.format(**kwargs)


# Global config instance (initialized when imported)
config: Optional[Config] = None


def load_config() -> Config:
    """Load and validate configuration"""
    global config
    config = Config()
    
    if not config.validate():
        raise ValueError("Configuration validation failed. Please check your .env file.")
    
    return config
