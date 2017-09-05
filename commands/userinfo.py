from discord.ext import commands
from discord import Embed, Member
from discord.ext.commands import BucketType
import rethinkdb as r


class UserInfo:  # Inside this class we make our own command.

    def __init__(self, bot):
        self.bot = bot  # Makes this class a command/extension
        self.connection = r.connect(db='twincastbot')

    @commands.command(aliases=["stats", "pinfo", "user", "u"], description="Get Twincast info about a user",
                      help="Shows how many twincasts, single casts, and failures a user has", usage="<user>",
                      brief="Get Twincast info about a user")
    @commands.cooldown(1, 8, BucketType.user)
    async def userinfo(self, ctx, user: Member = None):  # the function's name is our command name.
        if not user:
            user = ctx.author

        if r.table('users').get(str(user.id)).run(self.connection):
            if r.table('users').get(str(user.id)).has_fields('twincasts').run(self.connection):
                twincasts = r.table('users').get(str(user.id)).run(self.connection)['twincasts']
            else:
                twincasts = 0
        else:
            twincasts = 0
        if r.table('users').get(str(user.id)).run(self.connection):
            if r.table('users').get(str(user.id)).has_fields('single_casts').run(self.connection):
                single_casts = r.table('users').get(str(user.id)).run(self.connection)['single_casts']
            else:
                single_casts = 0
        else:
            single_casts = 0
        if r.table('users').get(str(user.id)).run(self.connection):
            if r.table('users').get(str(user.id)).has_fields('failures').run(self.connection):
                failures = r.table('users').get(str(user.id)).run(self.connection)['failures']
            else:
                failures = 0
        else:
            failures = 0

        if user:
            embed = Embed(
                author=user.name + "'s Twincast info",
                description="Twincasts: " + str(twincasts) + "\nSingle Casts: " +
                            str(single_casts) + "\nFailures: " + str(failures),
                colour=0xFFFF00)
            embed.set_author(name=user.name + "'s Twincast info", icon_url=user.avatar_url)
            await ctx.send(embed=embed)


def setup(bot):  # This function outside of the class initializes our extension/command and makes it readable by the
    # main file, TwincastBot.py
    bot.add_cog(UserInfo(bot))  # Well, yeah. adds the extension/command.
