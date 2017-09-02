from discord.ext import commands
from discord import Embed
from discord.ext.commands import BucketType
import rethinkdb as r
from rethinkdb.errors import RqlRuntimeError


class Submit:  # Inside this class we make our own command.

    def __init__(self, bot):
        self.bot = bot  # Makes this class a command/extension
        self.connection = r.connect(db='twincastbot')
        try:
            r.db_create('twincastbot').run(self.connection)
            r.db('twincastbot').table_create('users').run(self.connection)
            print('Database \'twincastbot\' and table \'users\' created.')
        except RqlRuntimeError:
            print('Database and table already exist.')

    @commands.command(aliases=["s"], description="Submit a word")  # @commands.command is used to initialize the command
    @commands.cooldown(1, 8, BucketType.user)
    async def submit(self, ctx, word: str):  # the function's name is our command name.
        user_id = ctx.author.id

        with open("english_words.txt") as word_file:
            english_words = set(word.strip().lower() for word in word_file)
            print("%s, %s" % (word, str(word.lower() in english_words)))
            if word.lower() in english_words:
                if "a" in word:
                    if "b" in word:
                        await ctx.send(
                            embed=Embed(description=":tada: Your word twincasted!",
                                        colour=0x00FFFF))

                        if r.table('users').get(user_id).run(self.connection):
                            r.table('users').get(user_id).update(
                                {"twincasts": r.table('users').get(user_id)['twincasts'].run(self.connection) + 1}).run(self.connection)
                        else:
                            r.table('users').insert({"id": user_id, "twincasts": 1}).run(self.connection)
                            print("added " + user_id + " to the db")
                        print(r.table('users').get(user_id).run(self.connection))

                    else:
                        await ctx.send(embed=Embed(description=":white_check_mark: Your word, %s, was submitted and "
                                                               "matched **fang**." % word,
                                                   colour=0x00FF00))
                elif "b" in word:
                    await ctx.send(embed=Embed(description=":white_check_mark: Your word, %s, was submitted and "
                                                           "matched **cabinet**." % word,
                                               colour=0x00FF00))
                else:
                    await ctx.send(embed=Embed(description=":white_check_mark: Your word, %s, was submitted and "
                                                           "matched nothing." % word,
                                               colour=0x00FF00))
            else:
                await ctx.send(embed=Embed(description=":x: Your word, %s, isn't a word and wasn't submitted." % word,
                                           colour=0xFF0000))


def setup(bot):  # This function outside of the class initializes our extension/command and makes it readable by the
    # main file, TwincastBot.pye
    bot.add_cog(Submit(bot))  # Well, yeah. adds the extension/command.
