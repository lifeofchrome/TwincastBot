from discord.ext import commands
from discord.ext.commands import BucketType
import discord.utils


class Misc:  # Inside this class we make our own command.
    def __init__(self, bot):
        self.bot = bot  # Makes this class a command/extension

    @commands.command(help="Get notified of new twincast rounds with the new-round-notify role. This role isn't"
                           "publicly mentionable. Send command again to remove the role.",
                      brief="Get notified of new rounds",
                      description="Get notified of new rounds")
    # @commands.command is used to initialize your command.
    @commands.cooldown(1, 8, BucketType.user)
    async def notify(self, ctx):  # the function's name is our command name.
        notifyrole = discord.utils.get(self.bot.get_guild(232353143038410753).roles, name='new-round-notify')
        if notifyrole in ctx.author.roles:
            await ctx.author.remove_roles(notifyrole)
            await ctx.send(embed=Embed(description=":white_check_mark: No longer notifying you of new rounds.", colour=0x00FF00))
        else:
            await ctx.author.add_roles(notifyrole)
            await ctx.send(embed=Embed(description=":white_check_mark: Now notifying you of new rounds.", colour=0x00FF00))


def setup(bot):  # This function outside of the class initializes our extension/command and makes it readable by the
    # main file, TwincastBot.py
    bot.add_cog(Misc(bot))  # Well, yeah. adds the extension/command.
