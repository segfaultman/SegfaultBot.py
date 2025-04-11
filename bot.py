import discord
import os
from discord.ext import commands
from dotenv      import load_dotenv

load_dotenv()
bot_intents = discord.Intents.default()
bot_intents.message_content = True


class Bot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix='?', intents=bot_intents)

    async def on_ready(self) -> None:
        print('SegfaultBot is running!')

        print('Loading cogs...')

        cogs = os.listdir('cogs')

        for cog in cogs:
            if cog.endswith('.py'):
                await bot.load_extension('cogs.{}'.format(cog[:-3]))
                print('Loaded cog: {}'.format(cog))


bot = Bot()
bot.run(os.getenv('BOT_TOKEN'))
