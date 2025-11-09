"""
Core Discord bot client for Admin Action Bot
Handles Discord connection, events, and command registration
"""

import discord
from discord.ext import commands
from discord import app_commands
import logging
from typing import Optional

from .config import Config
from .pterodactyl import PterodactylClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('AdminBot')


class AdminBot(commands.Bot):
    """Main bot class for Admin Action Bot"""
    
    def __init__(self, config: Config):
        """
        Initialize the bot
        
        Args:
            config: Configuration instance
        """
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        
        super().__init__(
            command_prefix=config.command_prefix,
            intents=intents,
            help_command=None
        )
        
        self.config = config
        self.bot_channel: Optional[discord.TextChannel] = None
        self.audit_channel: Optional[discord.TextChannel] = None
        self.admin_guild: Optional[discord.Guild] = None
        
        # Initialize Pterodactyl client
        self.pterodactyl = PterodactylClient(
            api_url=config.pterodactyl_url,
            api_key=config.pterodactyl_key,
            server_id=config.server_id
        )
        
        # Cache for recent players (for dropdown selection)
        self.recent_players: list = []
        self.max_recent_players = 25  # Store last 25 unique players
        
    async def setup_hook(self):
        """Called when bot is starting up - setup commands and extensions"""
        logger.info("Setting up bot...")
        
        # Register slash commands
        await self.register_commands()
        
        logger.info("Setup complete")
    
    async def on_ready(self):
        """Called when bot successfully connects to Discord"""
        logger.info(f'Bot connected as {self.user} (ID: {self.user.id})')
        
        # Get guild and audit channel
        self.admin_guild = self.get_guild(self.config.guild_id)
        if not self.admin_guild:
            logger.error(f"Could not find guild with ID {self.config.guild_id}")
            return
        
        # Get bot command channel
        self.bot_channel = self.admin_guild.get_channel(self.config.bot_channel_id)
        if not self.bot_channel:
            logger.error(f"Could not find bot channel with ID {self.config.bot_channel_id}")
            return
        
        # Get audit log channel
        self.audit_channel = self.admin_guild.get_channel(self.config.audit_channel_id)
        if not self.audit_channel:
            logger.error(f"Could not find audit channel with ID {self.config.audit_channel_id}")
            return
        
        logger.info(f"Connected to guild: {self.admin_guild.name}")
        logger.info(f"Bot channel: #{self.bot_channel.name}")
        logger.info(f"Audit channel: #{self.audit_channel.name}")
        
        # Sync slash commands to guild
        try:
            synced = await self.tree.sync(guild=discord.Object(id=self.config.guild_id))
            logger.info(f"Synced {len(synced)} command(s) to guild")
        except Exception as e:
            logger.error(f"Failed to sync commands: {e}")
        
        # Set bot status
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="for moderation needs | /admin"
            )
        )
        
        # Test Pterodactyl connection
        await self.pterodactyl.test_connection()
        
        # Send welcome message to bot channel
        await self.send_welcome_message()
    
    async def on_error(self, event_method: str, *args, **kwargs):
        """Handle errors in event handlers"""
        logger.exception(f"Error in {event_method}")
    
    async def send_welcome_message(self):
        """Send welcome message to bot channel showing available commands"""
        if not self.bot_channel:
            logger.warning("Cannot send welcome message - bot channel not found")
            return
        
        try:
            embed = discord.Embed(
                title="🤖 Admin Action Bot Online",
                description="Minecraft server moderation tool is ready!",
                color=discord.Color.green()
            )
            
            embed.add_field(
                name="📋 Available Commands",
                value="</admin:0> - Open the admin action panel",
                inline=False
            )
            
            embed.add_field(
                name="🛡️ Available Actions",
                value=(
                    "• 🔴 **Kill** - Remove player instantly\n"
                    "• 👢 **Kick** - Disconnect player from server\n"
                    "• ⏰ **Temp Ban** - Temporary ban with duration\n"
                    "• 🚫 **Ban** - Permanent ban\n"
                    "• ❄️ **Freeze** - Freeze game ticks\n"
                    "• ✅ **Unfreeze** - Restore game ticks"
                ),
                inline=False
            )
            
            embed.add_field(
                name="📍 Usage",
                value=f"Use `/admin` in this channel to open the moderation panel.\nAll actions are logged in <#{self.config.audit_channel_id}>",
                inline=False
            )
            
            embed.set_footer(text=f"Version 0.2.2 • Logged actions appear in #audit-logs")
            embed.timestamp = discord.utils.utcnow()
            
            await self.bot_channel.send(embed=embed)
            logger.info("Welcome message sent to bot channel")
            
        except Exception as e:
            logger.error(f"Failed to send welcome message: {e}")
    
    async def register_commands(self):
        """Register slash commands and UI components"""
        # Main admin panel command
        @self.tree.command(
            name="admin",
            description="Open the admin action panel",
            guild=discord.Object(id=self.config.guild_id)
        )
        async def admin_panel(interaction: discord.Interaction):
            """Show the main admin panel with moderation buttons"""
            # Defer immediately in the command itself to minimize delay
            try:
                await interaction.response.defer(ephemeral=True)
            except discord.errors.NotFound:
                # Interaction already expired - log and return
                logger.error("Interaction expired before defer - user may have slow connection")
                return
            
            await self.show_admin_panel(interaction)
        
        logger.info("Commands registered")
    
    async def show_admin_panel(self, interaction: discord.Interaction):
        """
        Display the main admin panel with moderation action buttons
        
        Args:
            interaction: Discord interaction (already deferred)
        """
        # Check if command is used in the correct channel
        if interaction.channel_id != self.config.bot_channel_id:
            await interaction.followup.send(
                f"❌ This command can only be used in <#{self.config.bot_channel_id}>",
                ephemeral=True
            )
            return
        
        # Check if user has admin permissions
        if self.config.admin_role_id:
            if not any(role.id == self.config.admin_role_id for role in interaction.user.roles):
                await interaction.followup.send(
                    "❌ You don't have permission to use admin commands.",
                    ephemeral=True
                )
                return
        elif not interaction.user.guild_permissions.administrator:
            await interaction.followup.send(
                "❌ You need administrator permissions to use this command.",
                ephemeral=True
            )
            return
        
        # Create embed
        embed = discord.Embed(
            title="🛡️ Admin Action Panel",
            description="Select a moderation action below:",
            color=discord.Color.blue()
        )
        embed.add_field(
            name="Available Actions",
            value=(
                "🔴 **Kill** - Remove player instantly\n"
                "👢 **Kick** - Disconnect player\n"
                "⏰ **Temp Ban** - Temporary ban\n"
                "🚫 **Ban** - Permanent ban\n"
                "❄️ **Freeze** - Stop game ticks\n"
                "✅ **Unfreeze** - Restore game ticks"
            ),
            inline=False
        )
        embed.set_footer(text="All actions are logged in the audit channel")
        
        # Create buttons (will be implemented in ui module)
        view = AdminActionView(self)
        
        # Use followup since we already deferred the interaction
        await interaction.followup.send(embed=embed, view=view, ephemeral=True)
    
    async def log_action(
        self,
        admin: discord.Member,
        action: str,
        target: str,
        reason: Optional[str] = None,
        duration: Optional[int] = None,
        success: bool = True,
        error: Optional[str] = None
    ):
        """
        Log a moderation action to the audit channel
        
        Args:
            admin: The administrator who performed the action
            action: The action type (kill, kick, etc.)
            target: The target player
            reason: The reason for the action
            duration: Duration in minutes (for temp bans)
            success: Whether the action was successful
            error: Error message if action failed
        """
        if not self.audit_channel:
            logger.warning("Audit channel not available for logging")
            return
        
        # Determine color based on success
        color = discord.Color.green() if success else discord.Color.red()
        
        # Create embed
        embed = discord.Embed(
            title=f"{'✅' if success else '❌'} {action.upper()}",
            color=color,
            timestamp=discord.utils.utcnow()
        )
        
        embed.add_field(name="Administrator", value=admin.mention, inline=True)
        embed.add_field(name="Target Player", value=target, inline=True)
        embed.add_field(name="Status", value="Success" if success else "Failed", inline=True)
        
        if reason:
            embed.add_field(name="Reason", value=reason, inline=False)
        
        if duration:
            embed.add_field(name="Duration", value=f"{duration} minutes", inline=True)
        
        if error:
            embed.add_field(name="Error", value=f"```{error}```", inline=False)
        
        embed.set_footer(text=f"Admin ID: {admin.id}")
        
        try:
            await self.audit_channel.send(embed=embed)
            logger.info(f"Logged {action} by {admin.name} on {target}")
        except Exception as e:
            logger.error(f"Failed to send audit log: {e}")
    
    def add_recent_player(self, player_name: str):
        """
        Add a player to the recent players cache
        
        Args:
            player_name: The player's username
        """
        if not player_name or len(player_name) > 16:
            return
        
        # Remove if already exists (to move to front)
        if player_name in self.recent_players:
            self.recent_players.remove(player_name)
        
        # Add to front of list
        self.recent_players.insert(0, player_name)
        
        # Keep only max_recent_players
        if len(self.recent_players) > self.max_recent_players:
            self.recent_players = self.recent_players[:self.max_recent_players]
        
        logger.debug(f"Added {player_name} to recent players cache ({len(self.recent_players)} total)")
    
    def get_recent_players(self) -> list:
        """
        Get list of recent players for dropdown
        
        Returns:
            List of recent player names
        """
        return self.recent_players.copy()


class AdminActionView(discord.ui.View):
    """View containing moderation action buttons"""
    
    def __init__(self, bot: AdminBot):
        super().__init__(timeout=None)  # No timeout - persistent view
        self.bot = bot
    
    @discord.ui.button(label="Kill", style=discord.ButtonStyle.danger, emoji="🔴", custom_id="admin_action:kill")
    async def kill_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = PlayerActionModal(self.bot, "kill", "Kill Player")
        await interaction.response.send_modal(modal)
    
    @discord.ui.button(label="Kick", style=discord.ButtonStyle.danger, emoji="👢", custom_id="admin_action:kick")
    async def kick_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = PlayerActionModal(self.bot, "kick", "Kick Player", require_reason=True)
        await interaction.response.send_modal(modal)
    
    @discord.ui.button(label="Temp Ban", style=discord.ButtonStyle.danger, emoji="⏰", custom_id="admin_action:tempban")
    async def tempban_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = PlayerActionModal(self.bot, "tempban", "Temporary Ban", require_reason=True, require_duration=True)
        await interaction.response.send_modal(modal)
    
    @discord.ui.button(label="Ban", style=discord.ButtonStyle.danger, emoji="🚫", custom_id="admin_action:ban")
    async def ban_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = PlayerActionModal(self.bot, "ban", "Ban Player", require_reason=True)
        await interaction.response.send_modal(modal)
    
    @discord.ui.button(label="Freeze", style=discord.ButtonStyle.primary, emoji="❄️", custom_id="admin_action:freeze")
    async def freeze_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Freeze doesn't require player input
        await interaction.response.defer(ephemeral=True)
        
        command = self.bot.config.get_command("freeze")
        result = await self.bot.pterodactyl.send_command(command)
        
        if result['success']:
            await interaction.followup.send("✅ Game frozen successfully!", ephemeral=True)
            await self.bot.log_action(
                admin=interaction.user,
                action="freeze",
                target="Game",
                success=True
            )
        else:
            await interaction.followup.send(
                f"❌ Failed to freeze game: {result.get('error', 'Unknown error')}",
                ephemeral=True
            )
            await self.bot.log_action(
                admin=interaction.user,
                action="freeze",
                target="Game",
                success=False,
                error=result.get('error')
            )
    
    @discord.ui.button(label="Unfreeze", style=discord.ButtonStyle.success, emoji="✅", custom_id="admin_action:unfreeze")
    async def unfreeze_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Unfreeze doesn't require player input
        await interaction.response.defer(ephemeral=True)
        
        command = self.bot.config.get_command("unfreeze")
        result = await self.bot.pterodactyl.send_command(command)
        
        if result['success']:
            await interaction.followup.send("✅ Game unfrozen successfully!", ephemeral=True)
            await self.bot.log_action(
                admin=interaction.user,
                action="unfreeze",
                target="Game",
                success=True
            )
        else:
            await interaction.followup.send(
                f"❌ Failed to unfreeze game: {result.get('error', 'Unknown error')}",
                ephemeral=True
            )
            await self.bot.log_action(
                admin=interaction.user,
                action="unfreeze",
                target="Game",
                success=False,
                error=result.get('error')
            )


class PlayerActionModal(discord.ui.Modal):
    """Modal for collecting player name and action details"""
    
    def __init__(self, bot: AdminBot, action: str, title: str, require_reason: bool = False, require_duration: bool = False):
        super().__init__(title=title)
        self.bot = bot
        self.action = action
        self.require_reason = require_reason
        self.require_duration = require_duration
        
        # Check if we have recent players for dropdown
        recent_players = self.bot.get_recent_players()
        
        if recent_players and len(recent_players) > 0:
            # Show info that dropdown will appear after modal
            self.info_text = discord.ui.TextInput(
                label="Player Selection",
                placeholder="Click Submit to see player dropdown...",
                required=False,
                default="Players available in dropdown - click Submit",
                max_length=50
            )
            self.add_item(self.info_text)
        else:
            # Player name field (manual input if no cached players)
            self.player_input = discord.ui.TextInput(
                label="Player Name",
                placeholder="Enter the player's username",
                required=True,
                max_length=16  # Minecraft username max length
            )
            self.add_item(self.player_input)
        
        # Reason field (optional)
        if require_reason:
            self.reason_input = discord.ui.TextInput(
                label="Reason",
                placeholder="Enter the reason for this action",
                required=True,
                style=discord.TextStyle.paragraph,
                max_length=500
            )
            self.add_item(self.reason_input)
        
        # Duration field (for temp bans)
        if require_duration:
            self.duration_input = discord.ui.TextInput(
                label="Duration (minutes)",
                placeholder="Enter duration in minutes (e.g., 60 for 1 hour)",
                required=True,
                max_length=10
            )
            self.add_item(self.duration_input)
    
    async def on_submit(self, interaction: discord.Interaction):
        """Handle modal submission"""
        recent_players = self.bot.get_recent_players()
        
        # If we have recent players, show dropdown selection
        if recent_players and len(recent_players) > 0:
            await interaction.response.defer(ephemeral=True)
            
            # Get reason and duration from modal
            reason = self.reason_input.value.strip() if self.require_reason else None
            duration = None
            
            if self.require_duration:
                try:
                    duration = int(self.duration_input.value.strip())
                    if duration <= 0:
                        await interaction.followup.send("❌ Duration must be a positive number!", ephemeral=True)
                        return
                except ValueError:
                    await interaction.followup.send("❌ Duration must be a valid number!", ephemeral=True)
                    return
            
            # Show player dropdown
            view = PlayerSelectionView(self.bot, self.action, reason, duration)
            embed = discord.Embed(
                title=f"🎯 Select Player for {self.action.title()}",
                description="Choose a player from the list below:",
                color=discord.Color.blue()
            )
            embed.add_field(
                name="Recent Players",
                value=f"**{len(recent_players)}** players available",
                inline=False
            )
            if reason:
                embed.add_field(name="Reason", value=reason, inline=False)
            if duration:
                embed.add_field(name="Duration", value=f"{duration} minutes", inline=True)
            
            await interaction.followup.send(embed=embed, view=view, ephemeral=True)
        else:
            # No cached players - use manual input
            await interaction.response.defer(ephemeral=True)
            
            player = self.player_input.value.strip()
            reason = self.reason_input.value.strip() if self.require_reason else None
            duration = None
            
            # Validate duration if required
            if self.require_duration:
                try:
                    duration = int(self.duration_input.value.strip())
                    if duration <= 0:
                        await interaction.followup.send("❌ Duration must be a positive number!", ephemeral=True)
                        return
                except ValueError:
                    await interaction.followup.send("❌ Duration must be a valid number!", ephemeral=True)
                    return
            
            # Execute the action
            await self._execute_action(interaction, player, reason, duration)
    
    async def _execute_action(self, interaction: discord.Interaction, player: str, reason: Optional[str], duration: Optional[int]):
        """Execute the moderation action"""
        # Add player to recent cache
        self.bot.add_recent_player(player)
        
        # Get command template and format it
        command = self.bot.config.get_command(self.action, player=player, reason=reason, duration=duration)
        
        # Send command via Pterodactyl
        result = await self.bot.pterodactyl.send_command(command)
        
        if result['success']:
            # Success message
            success_msg = f"✅ Successfully executed {self.action} on **{player}**"
            if reason:
                success_msg += f"\nReason: {reason}"
            if duration:
                success_msg += f"\nDuration: {duration} minutes"
            
            await interaction.followup.send(success_msg, ephemeral=True)
            
            # Log to audit channel
            await self.bot.log_action(
                admin=interaction.user,
                action=self.action,
                target=player,
                reason=reason,
                duration=duration,
                success=True
            )
        else:
            # Failure message
            error_msg = f"❌ Failed to execute {self.action} on **{player}**\n"
            error_msg += f"Error: {result.get('error', 'Unknown error')}"
            
            await interaction.followup.send(error_msg, ephemeral=True)
            
            # Log failure to audit channel
            await self.bot.log_action(
                admin=interaction.user,
                action=self.action,
                target=player,
                reason=reason,
                duration=duration,
                success=False,
                error=result.get('error')
            )
    
    async def on_error(self, interaction: discord.Interaction, error: Exception):
        """Handle modal errors"""
        logger.exception(f"Error in {self.action} modal")
        try:
            await interaction.response.send_message(
                f"❌ An error occurred: {str(error)}",
                ephemeral=True
            )
        except:
            await interaction.followup.send(
                f"❌ An error occurred: {str(error)}",
                ephemeral=True
            )


class PlayerSelectionView(discord.ui.View):
    """View for selecting a player from dropdown"""
    
    def __init__(self, bot: AdminBot, action: str, reason: Optional[str], duration: Optional[int]):
        super().__init__(timeout=180)  # 3 minute timeout for selection
        self.bot = bot
        self.action = action
        self.reason = reason
        self.duration = duration
        
        # Add player dropdown
        self.add_item(PlayerDropdown(bot, action, reason, duration))
        
        # Add manual input button
        manual_button = discord.ui.Button(
            label="Enter Manually",
            style=discord.ButtonStyle.secondary,
            emoji="⌨️"
        )
        manual_button.callback = self.manual_input_callback
        self.add_item(manual_button)
    
    async def manual_input_callback(self, interaction: discord.Interaction):
        """Show manual input modal"""
        modal = ManualPlayerInputModal(self.bot, self.action, self.reason, self.duration)
        await interaction.response.send_modal(modal)


class PlayerDropdown(discord.ui.Select):
    """Dropdown for selecting a player"""
    
    def __init__(self, bot: AdminBot, action: str, reason: Optional[str], duration: Optional[int]):
        self.bot = bot
        self.action = action
        self.reason = reason
        self.duration = duration
        
        # Get recent players
        recent_players = bot.get_recent_players()
        
        # Create options (max 25 for Discord)
        options = [
            discord.SelectOption(
                label=player,
                value=player,
                emoji="👤"
            )
            for player in recent_players[:25]
        ]
        
        super().__init__(
            placeholder="Select a player...",
            min_values=1,
            max_values=1,
            options=options
        )
    
    async def callback(self, interaction: discord.Interaction):
        """Handle player selection"""
        await interaction.response.defer(ephemeral=True)
        
        player = self.values[0]
        
        # Get command template and format it
        command = self.bot.config.get_command(self.action, player=player, reason=self.reason, duration=self.duration)
        
        # Send command via Pterodactyl
        result = await self.bot.pterodactyl.send_command(command)
        
        if result['success']:
            # Success message
            success_msg = f"✅ Successfully executed {self.action} on **{player}**"
            if self.reason:
                success_msg += f"\nReason: {self.reason}"
            if self.duration:
                success_msg += f"\nDuration: {self.duration} minutes"
            
            await interaction.followup.send(success_msg, ephemeral=True)
            
            # Log to audit channel
            await self.bot.log_action(
                admin=interaction.user,
                action=self.action,
                target=player,
                reason=self.reason,
                duration=self.duration,
                success=True
            )
        else:
            # Failure message
            error_msg = f"❌ Failed to execute {self.action} on **{player}**\n"
            error_msg += f"Error: {result.get('error', 'Unknown error')}"
            
            await interaction.followup.send(error_msg, ephemeral=True)
            
            # Log failure to audit channel
            await self.bot.log_action(
                admin=interaction.user,
                action=self.action,
                target=player,
                reason=self.reason,
                duration=self.duration,
                success=False,
                error=result.get('error')
            )


class ManualPlayerInputModal(discord.ui.Modal):
    """Modal for manual player name input"""
    
    def __init__(self, bot: AdminBot, action: str, reason: Optional[str], duration: Optional[int]):
        super().__init__(title=f"Enter Player Name - {action.title()}")
        self.bot = bot
        self.action = action
        self.reason = reason
        self.duration = duration
        
        self.player_input = discord.ui.TextInput(
            label="Player Name",
            placeholder="Enter the player's username",
            required=True,
            max_length=16
        )
        self.add_item(self.player_input)
    
    async def on_submit(self, interaction: discord.Interaction):
        """Handle manual input submission"""
        await interaction.response.defer(ephemeral=True)
        
        player = self.player_input.value.strip()
        
        # Add to recent players cache
        self.bot.add_recent_player(player)
        
        # Get command template and format it
        command = self.bot.config.get_command(self.action, player=player, reason=self.reason, duration=self.duration)
        
        # Send command via Pterodactyl
        result = await self.bot.pterodactyl.send_command(command)
        
        if result['success']:
            success_msg = f"✅ Successfully executed {self.action} on **{player}**"
            if self.reason:
                success_msg += f"\nReason: {self.reason}"
            if self.duration:
                success_msg += f"\nDuration: {self.duration} minutes"
            
            await interaction.followup.send(success_msg, ephemeral=True)
            
            await self.bot.log_action(
                admin=interaction.user,
                action=self.action,
                target=player,
                reason=self.reason,
                duration=self.duration,
                success=True
            )
        else:
            error_msg = f"❌ Failed to execute {self.action} on **{player}**\n"
            error_msg += f"Error: {result.get('error', 'Unknown error')}"
            
            await interaction.followup.send(error_msg, ephemeral=True)
            
            await self.bot.log_action(
                admin=interaction.user,
                action=self.action,
                target=player,
                reason=self.reason,
                duration=self.duration,
                success=False,
                error=result.get('error')
            )

