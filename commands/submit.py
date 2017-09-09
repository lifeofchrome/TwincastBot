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

    @commands.command(aliases=["s"], description="Submit a word.",
                      help="Submits a word.\nOnly 6 letter English words are submitted.", usage="<word>")
    # @commands.command is used to initialize the command
    @commands.cooldown(1, 8, BucketType.user)
    async def submit(self, ctx, word: str):  # the function's name is our command name.
        user_id = str(ctx.author.id)

        with open("english_words.txt") as word_file:
            english_words = set(word.strip().lower() for word in word_file)
            print("%s, %s" % (word, str(word.lower() in english_words)))
            if word.lower() in english_words:
                if len(word) > 5:
                    if "a" in word:
                        if "b" in word:
                            await ctx.send(
                                embed=Embed(description=":tada: Your word twincasted!",
                                            colour=0x00FFFF))

                            if r.table('users').get(user_id).run(self.connection):
                                if r.table('users').get(user_id).has_fields('twincasts').run(self.connection):
                                    r.table('users').get(user_id).update(
                                        {"twincasts":
                                            r.table('users').get(user_id)['twincasts'].run(self.connection) + 1}
                                    ).run(self.connection)
                                else:
                                    r.table('users').get(user_id).update({"twincasts": 1}).run(self.connection)
                            else:
                                r.table('users').insert({"id": user_id, "twincasts": 1}).run(self.connection)
                                print("added " + user_id + " to the db")
                            print(r.table('users').get(user_id).run(self.connection))

                            await self.bot.get_channel(232353777053728770).send(f"**{word}** ({ctx.author.name})")
                            await self.update_leaderboard()

                        else:
                            await ctx.send(embed=Embed(description=":white_check_mark: Your word, %s, was submitted and"
                                                                   " matched **fang**." % word,
                                                       colour=0x00FF00))
                            if r.table('users').get(user_id).run(self.connection):
                                if r.table('users').get(user_id).has_fields('single_casts').run(self.connection):
                                    r.table('users').get(user_id).update(
                                        {"single_casts":
                                            r.table('users').get(user_id)['single_casts'].run(self.connection) + 1}
                                    ).run(self.connection)
                                else:
                                    r.table('users').get(user_id).update({"single_casts": 1}).run(self.connection)
                            else:
                                r.table('users').insert({"id": user_id, "single_casts": 1}).run(self.connection)
                                print("added " + user_id + " to the db")
                            print(r.table('users').get(user_id).run(self.connection))
                            await self.bot.get_channel(232353685227831296).send(f"**{word}** ({ctx.author.name})")
                            await self.update_leaderboard()

                    elif "b" in word:
                        await ctx.send(embed=Embed(description=":white_check_mark: Your word, %s, was submitted and "
                                                               "matched **cabinet**." % word,
                                                   colour=0x00FF00))
                        if r.table('users').get(user_id).run(self.connection):
                            if r.table('users').get(user_id).has_fields('single_casts').run(self.connection):
                                r.table('users').get(user_id).update(
                                    {"single_casts":
                                        r.table('users').get(user_id)['single_casts'].run(self.connection) + 1}
                                ).run(self.connection)
                            else:
                                r.table('users').get(user_id).update({"single_casts": 1}).run(self.connection)
                        else:
                            r.table('users').insert({"id": user_id, "single_casts": 1}).run(self.connection)
                            print("added " + user_id + " to the db")
                        print(r.table('users').get(user_id).run(self.connection))
                        await self.bot.get_channel(232353744702930944).send(f"**{word}** ({ctx.author.name})")
                        await self.update_leaderboard()

                    else:
                        await ctx.send(embed=Embed(description=":no_entry_sign: Your word, %s, was submitted and "
                                                               "matched nothing." % word,
                                                   colour=0xFFFF00))
                        if r.table('users').get(user_id).run(self.connection):
                            if r.table('users').get(user_id).has_fields('failures').run(self.connection):
                                r.table('users').get(user_id).update(
                                    {"failures":
                                        r.table('users').get(user_id)['failures'].run(self.connection) + 1}
                                ).run(self.connection)
                            else:
                                r.table('users').get(user_id).update({"failures": 1}).run(self.connection)
                        else:
                            r.table('users').insert({"id": user_id, "failures": 1}).run(self.connection)
                            print("added " + user_id + " to the db")
                        print(r.table('users').get(user_id).run(self.connection))
                        await self.bot.get_channel(232353821932650496).send(f"**{word}** ({ctx.author.name})")
                        await self.update_leaderboard()
                else:
                    await ctx.send(
                        embed=Embed(description=":x: Your word, %s, isn't 6 or more characters long and wasn't "
                                                "submitted." % word, colour=0xFF0000))
            else:
                await ctx.send(embed=Embed(description=":x: Your word, %s, isn't a word and wasn't submitted." % word,
                                           colour=0xFF0000))

    async def create_leaderboard(self):
        conn = r.connect(db='twincastbot')
        await self.bot.get_channel(232937599537381377).send(embed=Embed(
            title="Top Twincasters", description=str(r.table('users').order_by(r.desc('twincasts')).limit(3).
                                                     run(conn))))

    async def update_leaderboard(self):
        conn = r.connect(db='twincastbot')
        lb_table = r.table('users').order_by(r.desc('twincasts')).limit(3).run(conn)
        # lb_table is the sorted leaderboard table
        lb_str = f"1st: {self.bot.get_user(int(lb_table[0]['id'])).name}, {lb_table[0]['twincasts']} twincasts\n" \
                 f"2nd: {self.bot.get_user(int(lb_table[1]['id'])).name}, {lb_table[1]['twincasts']} twincasts\n" \
                 f"3rd: {self.bot.get_user(int(lb_table[2]['id'])).name}, {lb_table[2]['twincasts']} twincasts"
        if await (self.bot.get_channel(232937599537381377).history()).next():
            history = self.bot.get_channel(232937599537381377).history()
            message = await history.next()
            await message.edit(embed=Embed(
                title="Top Twincasters", description=lb_str))
            # str(r.table('users').order_by(r.desc('twincasts')).limit(3).run(conn))
        else:
            await self.create_leaderboard()


def setup(bot):  # This function outside of the class initializes our extension/command and makes it readable by the
    # main file, TwincastBot.py
    bot.add_cog(Submit(bot))  # Well, yeah. adds the extension/command.
