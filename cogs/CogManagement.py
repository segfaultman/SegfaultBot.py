import logging
import os
from discord.ext import commands

logger = logging.getLogger('discord')

class CogManagement(commands.Cog):
    """
    These are commands for the bot administrator(s) related to extension management
    """

    def __init__(self, bot) -> None:
        self.bot: commands.Bot = bot

    @commands.command(name='reload_cog', hidden=True)
    async def reload_cog(self, ctx: commands.Context, cog_name: str = None):
        """
        Used to reload any cog. Reloads all cogs if no arguments are given
        """

        if not await self.bot.is_owner(ctx.author):
            return await ctx.send("This command can only be used by the bot administrator.")

        if cog_name:
            try:
                await self.bot.reload_extension('cogs.{}'.format(cog_name))
                return await ctx.send('Successfully reloaded extension: `{}`'.format(cog_name))
            except commands.errors.ExtensionNotLoaded:
                return await ctx.send('The specified cog was not loaded')
            except commands.errors.ExtensionError as err:
                return await ctx.send('Error reloading extension: `{}`'.format(err))

        for cog in self.bot.cogs:
            await self.bot.reload_extension('cogs.{}'.format(cog))
            logger.info('Reloaded extension: {}'.format(cog))

        # TODO: Error checking?
        # Any specific cog reload behaviour is defined in an
        # override cog_unload method in the cog itself btw

    @commands.command(name='load_cog', hidden=True)
    async def load_cog(self, ctx, cog_name: str = None):
        """
        Used to load a new cog. The cog must be in the cogs directory
        """

        if not await self.bot.is_owner(ctx.author):
            return await ctx.send("This command can only be used by the bot administrator.")

        if not cog_name:
            return await ctx.send('You need to specify the extension name!')
        
        file_path = 'cogs/{}.py'.format(cog_name)
        
        if not os.path.exists(file_path):
            return await ctx.send('Cog file not found in cogs directory')
        
        try:
            await self.bot.load_extension('cogs.{}'.format(cog_name))
            await ctx.send('Seccessfully loaded extension at `{}`'.format(file_path))
        except commands.errors.ExtensionAlreadyLoaded:
            return await ctx.send('The extension is already loaded. Maybe try using `reload_cog`')
        
    @commands.command(name='unload_cog', hidden=True)
    async def unload_cog(self, ctx, cog_name: str = None):
        """
        Used to unload any cog. A valid cog name must be provided.
        """

        if not await self.bot.is_owner(ctx.author):
            return await ctx.send("This command can only be used by the bot administrator.")

        if not cog_name:
            return await ctx.send('You need to specify the extension name!')

        try:
            await self.bot.unload_extension('cogs.{}'.format(cog_name))
            return await ctx.send('Successfully unloaded extension: `{}`'.format(cog_name))
        except commands.errors.ExtensionNotLoaded:
            return await ctx.send('The specified extension is not loaded')
        except commands.errors.ExtensionError as err:
            return await ctx.send('Error unloading extension: {}'.format(err))
        
    @commands.command(name='list_cogs', hidden=True)
    async def list_cogs(self, ctx):
        """
        Provides a list of all the currently loaded extensions
        """
        
        if not await self.bot.is_owner(ctx.author):
            return await ctx.send("This command can only be used by the bot administrator.")

        await ctx.send('List of loaded extensions:\n`{}`'.format(list(self.bot.cogs.keys())))

async def setup(bot):
    await bot.add_cog(CogManagement(bot))
