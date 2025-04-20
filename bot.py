import asyncio
import discord
import os
import configparser
import logging
import logging.handlers

from discord.ext import commands
from dotenv      import load_dotenv
from aiohttp     import ClientSession

logger = logging.getLogger('discord')

load_dotenv() # Loading environment variables

class SegfaultBot(commands.Bot):

    def __init__(self, *args, web_client: ClientSession, **kwargs):
        super().__init__(*args, **kwargs)
        self.web_client = web_client
        
    async def setup_hook(self) -> None:

        cogs = os.listdir('cogs')

        for cog in cogs:
            if cog.endswith('.py'):
                await self.load_extension('cogs.{}'.format(cog[:-3]))
                logger.info('Loaded cog: {}'.format(cog))


async def main():

    bot_intents = discord.Intents.default()
    bot_intents.message_content = True

    # Load configuration file
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Configuration of the logging functionality
    logger.setLevel(logging.INFO)

    file_handler = logging.handlers.RotatingFileHandler(
        filename='discord.log',
        encoding='utf-8',
        maxBytes=50 * 1024 * 1024,
        backupCount=5
    )

    console_handler = logging.StreamHandler()

    time_format = '%d-%m-%Y %H:%M:%S'
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s -> %(message)s', time_format)
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Providing a web client for future use
    # and performance in mind
    async with ClientSession() as client:
        
        async with SegfaultBot(
            commands.when_mentioned_or(config['BotConfig']['prefix']),
            web_client=client,
            intents=bot_intents
        ) as bot:
            await bot.start(os.getenv('BOT_TOKEN'))

asyncio.run(main())
