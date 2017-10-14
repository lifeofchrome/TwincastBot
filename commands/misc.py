from discord.ext import commands
from discord.ext.commands import BucketType


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
        notifyrole = None
        for role in self.bot.get_guild(232353143038410753).roles:
            if role.name == 'new-round-notify':
                notifyrole = role
                break
        userroles = ctx.author.roles
        if notifyrole in ctx.author.roles:
            userroles.remove(notifyrole)
            await ctx.author.edit(roles=userroles)
        else:
            userroles.append(notifyrole)
            await ctx.author.edit(roles=userroles)
        await ctx.send(":white_check_mark: Done!")


def setup(bot):  # This function outside of the class initializes our extension/command and makes it readable by the
    # main file, TwincastBot.py
    bot.add_cog(Misc(bot))  # Well, yeah. adds the extension/command.
