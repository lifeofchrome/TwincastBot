from discord.ext import commands
from discord import Embed
from discord.ext.commands import BucketType
import time


class Ping:  # Inside this class we make our own command.
    def __init__(self, bot):
        self.bot = bot  # Makes this class a command/extension

    @commands.command(description="Check bot connection")  # @commands.command is used to initialize your command.
    @commands.cooldown(1, 8, BucketType.user)
    async def ping(self, ctx):  # the function's name is our command name.
            ping_time = int(round(time.time() * 1000))  # Picks the current time in milliseconds.
            em = Embed(description='Pinging...', colour=0xFF8000)
            ping_msg = await ctx.send(embed=em)  # sends a message in the same channel as the user
            ping = int(round(time.time() * 1000)) - ping_time  # picks the current time in milliseconds, again. and
            # subtracts with the old time.
            if ping > 500:
                await ping_msg.edit(embed=Embed(description="Pong! Response time: `{}ms`".format(ping), colour=0xFF0000))
            elif ping > 250:
                await ping_msg.edit(embed=Embed(description="Pong! Response time: `{}ms`".format(ping), colour=0xFFFF00))
            else:
                await ping_msg.edit(embed=Embed(description="Pong! Response time: `{}ms`".format(ping), colour=0x00FF00))
            # Edits the message to show the response time!


def setup(bot):  # This function outside of the class initializes our extension/command and makes it readable by the
    # main file, TwincastBot.py
    bot.add_cog(Ping(bot))  # Well, yeah. adds the extension/command.
