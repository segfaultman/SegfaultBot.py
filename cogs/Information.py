from discord.ext import commands

class Information(commands.Cog):
    """
    These are some commands related to bot information
    """

    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(name='ping', aliases=['latency'])
    async def ping(self, ctx: commands.Context):
        """
        Shows the websocket latency in milliseconds
        """
        await ctx.send("Pong! Websocket latency is {}ms.".format(self.bot.latency * 1000))

async def setup(bot):
    await bot.add_cog(Information(bot))