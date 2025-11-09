#!/usr/bin/env python3
"""
Admin Action Bot - Main Entry Point
Starts the Discord bot with configured settings
"""

import sys
import logging
from src.config import load_config
from src.bot import AdminBot

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('Main')


def main():
    """Main entry point for the bot"""
    try:
        # Load configuration
        logger.info("Loading configuration...")
        config = load_config()
        logger.info("Configuration loaded successfully")
        
        # Create and run bot
        logger.info("Starting bot...")
        bot = AdminBot(config)
        bot.run(config.discord_token)
        
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        logger.error("Please check your .env file and ensure all required variables are set")
        logger.error("See .env.example for reference")
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.exception(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
