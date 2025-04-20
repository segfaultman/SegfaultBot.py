import pomice
import os
import logging

from typing      import override
from discord.ext import commands

logger = logging.getLogger('discord')

class Music(commands.Cog):
    """
    These are the bot's music commands
    """
    def __init__(self, bot) -> None:
        self.bot: commands.Bot = bot
        self.pomice = pomice.NodePool()

        bot.loop.create_task(self.start_main_node())


    async def start_main_node(self) -> None:

        await self.bot.wait_until_ready()

        await self.pomice.create_node(
            bot=self.bot,
            host=os.getenv('LAVALINK_HOST'),
            port=int(os.getenv('LAVALINK_PORT')),
            password=os.getenv('LAVALINK_PASS'),
            identifier='MAIN'
        )

        logger.info('Created MAIN Lavalink node')
    
    @override
    async def cog_unload(self) -> None:

        identifiers = list(self.pomice.nodes.keys())

        # Ensure that we disconnect all nodes on cog reload
        # Future features like saving the state of players
        # may use that as well
        for id in identifiers:
            logger.info('Disconnecting node: {}'.format(id))
            await self.pomice.nodes[id].disconnect()

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

    @commands.command(name='disconnect')
    async def disconnect(self, ctx: commands.Context):
        """
        Disconnect the bot from the current channel
        """

        if not ctx.voice_client:
            return await ctx.send('Currently not connected to any VC')
        
        await ctx.voice_client.disconnect()
        await ctx.send('Disconnected')

    @commands.command(name='play', aliases=['p'])
    async def play(self, ctx: commands.Context, *, song: str = None):
        """
        Searches and plays the specified song
        """

        if not ctx.voice_client:
            await ctx.invoke(self.connect)

        if not song:
            return await ctx.send('Command usage: `?play [song title]`')

        player = ctx.voice_client

        results = await player.get_tracks(
            query='{}'.format(song),
            search_type=pomice.enums.SearchType.scsearch
        )

        if not results:
            return await ctx.send('Could not find any song matching that title')
        
        if isinstance(results, pomice.Playlist):
            track: pomice.objects.Track = results.tracks[0]
        else:
            track: pomice.objects.Track = results[0]

        await player.play(track)
        await ctx.send('Now playing: {}'.format(track))

    @commands.command(name='stop')
    async def stop(self, ctx: commands.Context):
        """
        Stops the current song
        """

        if not ctx.voice_client:
            return await ctx.send('Not even connected to a VC lmao')
        
        player = ctx.voice_client

        if not player.is_playing:
            return await ctx.send('There is nothing playing at the moment')
        
        await player.stop()
        await ctx.send('Stopped the player')

    @commands.command(name='volume', aliases=['v'])
    async def volume(self, ctx: commands.Context, volume: int):
        """
        Sets the volume of the player to the specified value from 0 to 500
        """

        if not ctx.voice_client:
            return await ctx.send('Not even connected to a VC lmao')
        
        player = ctx.voice_client

        await player.set_volume(volume=volume)
        await ctx.send('Volume set to {}%'.format(volume))

    @commands.command(name='pause')
    async def pause(self, ctx: commands.Context):
        """
        Pauses the bot player
        """

        if not ctx.voice_client:
            return await ctx.send('Not even connected to a VC lmao')
        
        player = ctx.voice_client

        await player.set_pause(pause=True)
        await ctx.send('The player is paused')

    @commands.command(name='resume')
    async def resume(self, ctx: commands.Context):
        """
        Resumes the bot player
        """

        if not ctx.voice_client:
            return await ctx.send('Not even connected to a VC lmao')
        
        player = ctx.voice_client

        await player.set_pause(pause=False)
        await ctx.send('The player is resumed')


async def setup(bot: commands.Bot):
    await bot.add_cog(Music(bot))
