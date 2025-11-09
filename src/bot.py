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
                name="for moderation needs"
            )
        )
    
    async def on_error(self, event_method: str, *args, **kwargs):
        """Handle errors in event handlers"""
        logger.exception(f"Error in {event_method}")
    
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
            await self.show_admin_panel(interaction)
        
        logger.info("Commands registered")
    
    async def show_admin_panel(self, interaction: discord.Interaction):
        """
        Display the main admin panel with moderation action buttons
        
        Args:
            interaction: Discord interaction
        """
        # Check if command is used in the correct channel
        if interaction.channel_id != self.config.bot_channel_id:
            await interaction.response.send_message(
                f"❌ This command can only be used in <#{self.config.bot_channel_id}>",
                ephemeral=True
            )
            return
        
        # Check if user has admin permissions
        if self.config.admin_role_id:
            if not any(role.id == self.config.admin_role_id for role in interaction.user.roles):
                await interaction.response.send_message(
                    "❌ You don't have permission to use admin commands.",
                    ephemeral=True
                )
                return
        elif not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
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
                "🚫 **IP Ban** - Permanent ban\n"
                "🔇 **Mute** - Prevent chat\n"
                "⚠️ **Warn** - Issue warning\n"
                "❄️ **Freeze** - Stop game ticks\n"
                "✅ **Unfreeze** - Restore game ticks"
            ),
            inline=False
        )
        embed.set_footer(text="All actions are logged in the audit channel")
        
        # Create buttons (will be implemented in ui module)
        view = AdminActionView(self)
        
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
    
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


class AdminActionView(discord.ui.View):
    """View containing moderation action buttons"""
    
    def __init__(self, bot: AdminBot):
        super().__init__(timeout=300)  # 5 minute timeout
        self.bot = bot
    
    @discord.ui.button(label="Kill", style=discord.ButtonStyle.danger, emoji="🔴")
    async def kill_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            "⚠️ Kill action not yet implemented. Coming in next version!",
            ephemeral=True
        )
    
    @discord.ui.button(label="Kick", style=discord.ButtonStyle.danger, emoji="👢")
    async def kick_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            "⚠️ Kick action not yet implemented. Coming in next version!",
            ephemeral=True
        )
    
    @discord.ui.button(label="Temp Ban", style=discord.ButtonStyle.danger, emoji="⏰")
    async def tempban_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            "⚠️ Temp Ban action not yet implemented. Coming in next version!",
            ephemeral=True
        )
    
    @discord.ui.button(label="IP Ban", style=discord.ButtonStyle.danger, emoji="🚫")
    async def ipban_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            "⚠️ IP Ban action not yet implemented. Coming in next version!",
            ephemeral=True
        )
    
    @discord.ui.button(label="Mute", style=discord.ButtonStyle.primary, emoji="🔇")
    async def mute_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            "⚠️ Mute action not yet implemented. Coming in next version!",
            ephemeral=True
        )
    
    @discord.ui.button(label="Warn", style=discord.ButtonStyle.secondary, emoji="⚠️")
    async def warn_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            "⚠️ Warn action not yet implemented. Coming in next version!",
            ephemeral=True
        )
    
    @discord.ui.button(label="Freeze", style=discord.ButtonStyle.primary, emoji="❄️")
    async def freeze_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            "⚠️ Freeze action not yet implemented. Coming in next version!",
            ephemeral=True
        )
    
    @discord.ui.button(label="Unfreeze", style=discord.ButtonStyle.success, emoji="✅")
    async def unfreeze_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            "⚠️ Unfreeze action not yet implemented. Coming in next version!",
            ephemeral=True
        )
