"""
Tests for configuration management
"""

import pytest
import os
from unittest.mock import patch
from src.config import Config


# Complete valid environment for tests
VALID_ENV = {
    'DISCORD_BOT_TOKEN': 'test_token_1234567890123456789012345678901234567890',
    'DISCORD_GUILD_ID': '123456789',
    'DISCORD_BOT_CHANNEL_ID': '111111111',
    'DISCORD_AUDIT_CHANNEL_ID': '987654321',
    'PTERODACTYL_API_URL': 'https://panel.example.com',
    'PTERODACTYL_API_KEY': 'test_api_key',
    'PTERODACTYL_SERVER_ID': 'server_123',
    'CMD_KILL': 'kill {player}',
    'CMD_KICK': 'kick {player} {reason}',
    'CMD_TEMPBAN': 'tempban {player} {duration}m {reason}',
    'CMD_IPBAN': 'ban {player} {reason}',
    'CMD_MUTE': 'mute {player} {reason}',
    'CMD_WARN': 'warn {player} {reason}',
    'CMD_FREEZE': 'tick freeze',
    'CMD_UNFREEZE': 'tick unfreeze',
}


class TestConfig:
    """Test suite for Config class"""
    
    @patch.dict(os.environ, VALID_ENV, clear=True)
    def test_config_loads_successfully(self):
        """Test that configuration loads with valid environment variables"""
        config = Config()
        
        assert config.discord_token == 'test_token_1234567890123456789012345678901234567890'
        assert config.guild_id == 123456789
        assert config.bot_channel_id == 111111111
        assert config.audit_channel_id == 987654321
        assert config.pterodactyl_url == 'https://panel.example.com'
        assert config.pterodactyl_key == 'test_api_key'
        assert config.server_id == 'server_123'
    
    @patch('src.config.load_dotenv')  # Mock dotenv to prevent loading from file
    @patch.dict(os.environ, {}, clear=True)
    def test_config_fails_without_required_vars(self, mock_dotenv):
        """Test that configuration raises error when required vars are missing"""
        with pytest.raises(ValueError, match="Required environment variable"):
            Config()
    
    @patch.dict(os.environ, {**VALID_ENV, 'PTERODACTYL_API_URL': 'https://panel.example.com/'}, clear=True)
    def test_pterodactyl_url_strips_trailing_slash(self):
        """Test that trailing slash is removed from Pterodactyl URL"""
        config = Config()
        assert config.pterodactyl_url == 'https://panel.example.com'
    
    @patch.dict(os.environ, VALID_ENV, clear=True)
    def test_get_command_formats_correctly(self):
        """Test that command templates are formatted correctly"""
        config = Config()
        
        kill_cmd = config.get_command('kill', player='Steve')
        assert kill_cmd == 'kill Steve'
        
        kick_cmd = config.get_command('kick', player='Alex', reason='Cheating')
        assert kick_cmd == 'kick Alex Cheating'
    
    @patch.dict(os.environ, VALID_ENV, clear=True)
    def test_validate_passes_with_valid_config(self):
        """Test that validation passes with valid configuration"""
        config = Config()
        assert config.validate() is True
    
    @patch.dict(os.environ, {
        'DISCORD_BOT_TOKEN': 'short',
        'DISCORD_GUILD_ID': '123456789',
        'DISCORD_BOT_CHANNEL_ID': '111111111',
        'DISCORD_AUDIT_CHANNEL_ID': '987654321',
        'PTERODACTYL_API_URL': 'invalid_url',
        'PTERODACTYL_API_KEY': 'test_api_key',
        'PTERODACTYL_SERVER_ID': 'server_123',
        'CMD_KILL': 'kill {player}',
        'CMD_KICK': 'kick {player} {reason}',
        'CMD_TEMPBAN': 'tempban {player} {duration}m {reason}',
        'CMD_IPBAN': 'ban {player} {reason}',
        'CMD_MUTE': 'mute {player} {reason}',
        'CMD_WARN': 'warn {player} {reason}',
        'CMD_FREEZE': 'tick freeze',
        'CMD_UNFREEZE': 'tick unfreeze',
    }, clear=True)
    def test_validate_fails_with_invalid_config(self):
        """Test that validation fails with invalid configuration"""
        config = Config()
        assert config.validate() is False
    
    @patch.dict(os.environ, VALID_ENV, clear=True)
    def test_freeze_commands_work_without_player_placeholder(self):
        """Test that freeze/unfreeze commands don't require {player} placeholder"""
        config = Config()
        assert config.commands['freeze'] == 'tick freeze'
        assert config.commands['unfreeze'] == 'tick unfreeze'
        assert config.validate() is True
    
    @patch.dict(os.environ, {
        **VALID_ENV,
        'CMD_KILL': 'kill',  # Missing {player} placeholder
    }, clear=True)
    def test_validate_fails_when_player_required_command_missing_placeholder(self):
        """Test that validation fails when player-required commands miss {player} placeholder"""
        config = Config()
        assert config.validate() is False
