import pomice
from typing import override

from discord.ext import commands

class Music(commands.Cog):
    """
    These are the bot's music commands
    """
    def __init__(self, bot) -> None:
        self.bot = bot
        self.pomice = pomice.NodePool()

    async def start_nodes(self) -> None:
        await self.pomice.create_node(bot=self.bot, host='127.0.0.1', port=3030, password='youshallnotpass', identifier='MAIN')
        print('Created MAIN node')

    @override
    async def cog_unload(self) -> None:
        identifiers = list(self.pomice.nodes.keys())
        print(identifiers)
        for id in identifiers:
            print('Disconnecting node: {}'.format(id))
            await self.pomice.nodes[id].disconnect() # Ensure that we disconnect all nodes on cog reload
        # Further features like saving the state of players may use that as well

    @commands.command(name='connect')
    async def connect(self, ctx: commands.Context):
        """
        Connects the bot to your current channel
        """
        channel = getattr(ctx.author.voice, 'channel', None)
        if not channel:
            return await ctx.send('You need to be connected to a VC')
        
        await ctx.author.voice.channel.connect(cls=pomice.Player)
        await ctx.send('Connected to: {}'.format(channel))

async def setup(bot):
    await bot.add_cog(Music(bot))
    await bot.cogs['Music'].start_nodes()
