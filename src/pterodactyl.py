"""
Pterodactyl API client for sending commands to Minecraft server
Handles authentication, command execution, and error handling
"""

import aiohttp
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger('Pterodactyl')


class PterodactylClient:
    """Client for interacting with Pterodactyl Panel API"""
    
    def __init__(self, api_url: str, api_key: str, server_id: str):
        """
        Initialize Pterodactyl API client
        
        Args:
            api_url: Base URL of Pterodactyl panel (without trailing slash)
            api_key: Client API key from Pterodactyl
            server_id: Server identifier (UUID)
        """
        self.api_url = api_url.rstrip('/')
        self.api_key = api_key
        self.server_id = server_id
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        
    async def send_command(self, command: str) -> Dict[str, Any]:
        """
        Send a command to the Minecraft server via Pterodactyl
        
        Args:
            command: The command to execute (without leading /)
            
        Returns:
            Dict with 'success' (bool), 'message' (str), and optional 'error' (str)
        """
        url = f"{self.api_url}/api/client/servers/{self.server_id}/command"
        
        payload = {
            'command': command
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=self.headers, json=payload, timeout=aiohttp.ClientTimeout(total=30)) as response:
                    if response.status == 204:
                        # 204 No Content = command sent successfully
                        logger.info(f"Command sent successfully: {command}")
                        return {
                            'success': True,
                            'message': 'Command executed successfully'
                        }
                    elif response.status == 401:
                        error_msg = "Authentication failed - check API key"
                        logger.error(error_msg)
                        return {
                            'success': False,
                            'message': 'Failed to execute command',
                            'error': error_msg
                        }
                    elif response.status == 404:
                        error_msg = f"Server not found - check server ID: {self.server_id}"
                        logger.error(error_msg)
                        return {
                            'success': False,
                            'message': 'Failed to execute command',
                            'error': error_msg
                        }
                    elif response.status == 403:
                        error_msg = "Permission denied - API key lacks required permissions"
                        logger.error(error_msg)
                        return {
                            'success': False,
                            'message': 'Failed to execute command',
                            'error': error_msg
                        }
                    else:
                        error_text = await response.text()
                        error_msg = f"API returned status {response.status}: {error_text}"
                        logger.error(error_msg)
                        return {
                            'success': False,
                            'message': 'Failed to execute command',
                            'error': error_msg
                        }
                        
        except aiohttp.ClientError as e:
            error_msg = f"Network error: {str(e)}"
            logger.error(error_msg)
            return {
                'success': False,
                'message': 'Failed to execute command',
                'error': error_msg
            }
        except asyncio.TimeoutError:
            error_msg = "Request timeout - server took too long to respond"
            logger.error(error_msg)
            return {
                'success': False,
                'message': 'Failed to execute command',
                'error': error_msg
            }
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            logger.exception("Unexpected error sending command")
            return {
                'success': False,
                'message': 'Failed to execute command',
                'error': error_msg
            }
    
    async def get_server_status(self) -> Dict[str, Any]:
        """
        Get server status information
        
        Returns:
            Dict with server status info or error
        """
        url = f"{self.api_url}/api/client/servers/{self.server_id}/resources"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.headers, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            'success': True,
                            'data': data.get('attributes', {})
                        }
                    else:
                        error_text = await response.text()
                        logger.error(f"Failed to get server status: {response.status} - {error_text}")
                        return {
                            'success': False,
                            'error': f"API returned status {response.status}"
                        }
        except Exception as e:
            logger.exception("Error getting server status")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def get_online_players(self) -> Optional[list]:
        """
        Get list of online players from server console output
        Uses the 'list' command to fetch current players
        
        Returns:
            List of player names or None if unavailable
        """
        try:
            # First, send the 'list' command to get online players
            list_result = await self.send_command("list")
            
            if not list_result.get('success'):
                logger.warning("Could not send 'list' command to get players")
                return None
            
            # Get recent console logs to read the response
            url = f"{self.api_url}/api/client/servers/{self.server_id}/websocket"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.headers, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    if response.status == 200:
                        # We'll use a simpler approach - query server resources
                        # which sometimes includes player count
                        status = await self.get_server_status()
                        if status.get('success'):
                            # For now, return None - player list requires WebSocket connection
                            # which is complex. We'll implement a cached player list instead.
                            logger.info("Player list via WebSocket not yet implemented - using cached list")
                            return None
                    else:
                        return None
                        
        except Exception as e:
            logger.exception("Error fetching player list")
            return None
    
    async def get_cached_players(self) -> list:
        """
        Get cached list of recent players
        This will be populated from modal submissions
        
        Returns:
            List of recently used player names
        """
        # This will be managed by the bot class
        # For now, return empty list
        return []
    
    async def test_connection(self) -> bool:
        """
        Test connection to Pterodactyl API
        
        Returns:
            True if connection successful, False otherwise
        """
        logger.info("Testing Pterodactyl API connection...")
        result = await self.get_server_status()
        
        if result.get('success'):
            logger.info("✅ Pterodactyl API connection successful")
            return True
        else:
            logger.error(f"❌ Pterodactyl API connection failed: {result.get('error')}")
            return False
