from discord.ext import commands
from discord import Embed, Member
from discord.ext.commands import BucketType
import rethinkdb as r
# from rethinkdb.errors import RqlRuntimeError
import re


class Twincast:  # Inside this class we make our own command.

    def __init__(self, bot):
        self.bot = bot  # Makes this class a command/extension
        self.conn = r.connect(db='twincastbot')
        # try:
        #     r.db_create('twincastbot').run(self.connection)
        #     r.db('twincastbot').table_create('users').run(self.connection)
        #     r.db('twincastbot').table_create('words').run(self.connection)
        #     r.db('twincastbot').table_create('rounds').run(self.connection)
        #     print('Database \'twincastbot\' and tables \'users\', \'words\' created.')
        # except RqlRuntimeError:
        #     print('Database and tables already exist.')
        self.current_round = r.table('rounds').get(r.table('info').get(0)['current_round_id'].run(self.conn)).run(
            self.conn)

    @commands.command(aliases=["s"], description="Submit a word.",
                      help="Submits a word.\nOnly 6 letter English words are submitted.", usage="<word>")
    # @commands.command is used to initialize the command
    @commands.cooldown(1, 4, BucketType.user)
    async def submit(self, ctx, word: str):  # the function's name is our command name.
        user_id = str(ctx.author.id)

        with open("english_words.txt") as word_file:
            english_words = set(word.strip().lower() for word in word_file)
            print("%s, %s" % (word, str(word.lower() in english_words)))
            if len(word) > 5:
                if word.lower() in english_words:
                    if r.table('words').filter(r.row['word'] == word).count().run(self.conn) == 0:
                        if re.match(self.current_round['pattern1'], word):
                            if re.match(self.current_round['pattern2'], word):
                                await ctx.send(
                                    embed=Embed(description=":tada: Your word twincasted!",
                                                colour=0x00FFFF))

                                if r.table('users').get(user_id).run(self.conn):
                                    if r.table('users').get(user_id).has_fields('twincasts').run(self.conn):
                                        r.table('users').get(user_id).update(
                                            {"twincasts":
                                                r.table('users').get(user_id)['twincasts'].run(self.conn) + 1}
                                        ).run(self.conn)
                                    else:
                                        r.table('users').get(user_id).update({"twincasts": 1}).run(self.conn)
                                    if r.table('users').get(user_id).has_fields('twincasts_round_dev-2')\
                                            .run(self.conn):
                                        r.table('users').get(user_id).update(
                                            {"twincasts_round_dev-2":
                                                r.table('users').get(user_id)['twincasts_round_dev-2']
                                                .run(self.conn) + 1}).run(self.conn)
                                    else:
                                        r.table('users').get(user_id).update({"twincasts_round_dev-2": 1}).\
                                            run(self.conn)
                                else:
                                    r.table('users').insert({"id": user_id,
                                                             "twincasts": 1,
                                                             "twincasts_round_dev-2": 1}).run(self.conn)
                                    print("added " + user_id + " to the db")
                                print(r.table('users').get(user_id).run(self.conn))

                                await self.bot.get_channel(232353777053728770).send(f"**{word}** ({ctx.author.name})")
                                await self.update_leaderboard()

                            else:
                                await ctx.send(embed=Embed(description=f":white_check_mark: Your word, {word}, "
                                                                       f"was submitted and matched "
                                                                       f"**{self.current_round['word1']}**.",
                                                           colour=0x00FF00))
                                if r.table('users').get(user_id).run(self.conn):
                                    if r.table('users').get(user_id).has_fields('single_casts').run(self.conn):
                                        r.table('users').get(user_id).update(
                                            {"single_casts":
                                                r.table('users').get(user_id)['single_casts'].run(self.conn) + 1}
                                        ).run(self.conn)
                                    else:
                                        r.table('users').get(user_id).update({"single_casts": 1}).run(self.conn)
                                    if r.table('users').get(user_id).has_fields('single_casts_round_dev-2')\
                                            .run(self.conn):
                                        r.table('users').get(user_id).update(
                                            {"single_casts_round_dev-2":
                                                r.table('users').get(user_id)['single_casts_round_dev-2']
                                                .run(self.conn) + 1}).run(self.conn)
                                    else:
                                        r.table('users').get(user_id).update({"single_casts_round_dev-2": 1}).\
                                            run(self.conn)
                                else:
                                    r.table('users').insert({"id": user_id,
                                                             "single_casts": 1,
                                                             "single_casts_round_dev-2": 1}).run(self.conn)
                                    print("added " + user_id + " to the db")
                                print(r.table('users').get(user_id).run(self.conn))
                                await self.bot.get_channel(232353685227831296).send(f"**{word}** ({ctx.author.name})")

                        elif re.match(self.current_round['pattern2'], word):
                            await ctx.send(embed=Embed(description=f":white_check_mark: Your word, {word}, "
                                                                   f"was submitted and matched "
                                                                   f"**{self.current_round['word2']}**.",
                                                       colour=0x00FF00))
                            if r.table('users').get(user_id).run(self.conn):
                                if r.table('users').get(user_id).has_fields('single_casts').run(self.conn):
                                    r.table('users').get(user_id).update(
                                        {"single_casts":
                                             r.table('users').get(user_id)['single_casts'].run(self.conn) + 1}
                                    ).run(self.conn)
                                else:
                                    r.table('users').get(user_id).update({"single_casts": 1}).run(self.conn)
                                if r.table('users').get(user_id).has_fields('single_casts_round_dev-2') \
                                        .run(self.conn):
                                    r.table('users').get(user_id).update(
                                        {"single_casts_round_dev-2":
                                             r.table('users').get(user_id)['single_casts_round_dev-2']
                                                 .run(self.conn) + 1}).run(self.conn)
                                else:
                                    r.table('users').get(user_id).update({"single_casts_round_dev-2": 1}). \
                                        run(self.conn)
                            else:
                                r.table('users').insert({"id": user_id,
                                                         "single_casts": 1,
                                                         "single_casts_round_dev-2": 1}).run(self.conn)
                                print("added " + user_id + " to the db")
                            print(r.table('users').get(user_id).run(self.conn))
                            await self.bot.get_channel(232353744702930944).send(f"**{word}** ({ctx.author.name})")

                        else:
                            await ctx.send(embed=Embed(description=":no_entry_sign: Your word, %s, was submitted and "
                                                                   "matched nothing." % word,
                                                       colour=0xFFFF00))
                            if r.table('users').get(user_id).run(self.conn):
                                if r.table('users').get(user_id).has_fields('failures').run(self.conn):
                                    r.table('users').get(user_id).update(
                                        {"failures":
                                             r.table('users').get(user_id)['failures'].run(self.conn) + 1}
                                    ).run(self.conn)
                                else:
                                    r.table('users').get(user_id).update({"failures": 1}).run(self.conn)
                                if r.table('users').get(user_id).has_fields('failures_round_dev-2') \
                                        .run(self.conn):
                                    r.table('users').get(user_id).update(
                                        {"failures_round_dev-2":
                                             r.table('users').get(user_id)['failures_round_dev-2']
                                                 .run(self.conn) + 1}).run(self.conn)
                                else:
                                    r.table('users').get(user_id).update({"failures_round_dev-2": 1}). \
                                        run(self.conn)
                            else:
                                r.table('users').insert({"id": user_id,
                                                         "failures": 1,
                                                         "failures_round_dev-2": 1}).run(self.conn)
                                print("added " + user_id + " to the db")
                            print(r.table('users').get(user_id).run(self.conn))
                            await self.bot.get_channel(232353821932650496).send(f"**{word}** ({ctx.author.name})")
                    else:
                        await ctx.send(
                            embed=Embed(description=":x: Your word, %s, "
                                                    "has already been submitted." % word, colour=0xFF0000))
                    r.table('words').insert({'word': word}).run(self.conn)
                else:
                    await ctx.send(embed=Embed(description=":x: Your word, %s, isn't a word and wasn't submitted." % word,
                                           colour=0xFF0000))
            else:
                await ctx.send(
                    embed=Embed(description=":x: Your word, %s, isn't 6 or more characters long and wasn't "
                                "submitted." % word, colour = 0xFF0000))

    async def create_global_leaderboard(self, lb: str):
        await self.bot.get_channel(232937599537381377).send(embed=Embed(
            title="Top Twincasters", description=lb))

    async def create_round_leaderboard(self, round_name: str, lb: str):
        await self.bot.get_channel(232937599537381377).send(embed=Embed(title=f"Top Twincasters: Round {round_name}",
                                                                        description=lb, colour=0x0000FF))

    async def update_leaderboard(self):
        conn = r.connect(db='twincastbot')
        lb_table = r.table('users').order_by(r.desc('twincasts')).limit(5).run(conn)
        lb_round_table = r.table('users').order_by(r.desc('twincasts_round_dev-2')).limit(5).run(conn)
        # lb_table is the sorted leaderboard table
        # lb_round_table is the sorted leaderboard table for the current round
        prefixes = ['1st', '2nd', '3rd', '4th', '5th']
        lb_str = ""
        lb_round_str = ""
        for i in range(0, 4):
            lb_str = lb_str + f"{prefixes[i]}: {self.bot.get_user(int(lb_table[i]['id'])).name}, " \
                              f"{lb_table[i]['twincasts']} twincasts\n"
            lb_round_str = lb_round_str + f"{prefixes[i]}: {self.bot.get_user(int(lb_round_table[i]['id'])).name}, " \
                                          f"{lb_round_table[i]['twincasts_round_dev-2']} twincasts\n"

        # lb_str = f"1st: {self.bot.get_user(int(lb_table[0]['id'])).name}, {lb_table[0]['twincasts']} twincasts\n" \
        #          f"2nd: {self.bot.get_user(int(lb_table[1]['id'])).name}, {lb_table[1]['twincasts']} twincasts\n" \
        #          f"3rd: {self.bot.get_user(int(lb_table[2]['id'])).name}, {lb_table[2]['twincasts']} twincasts\n" \
        #          f"4th: {self.bot.get_user(int(lb_table[3]['id'])).name}, {lb_table[3]['twincasts']} twincasts\n" \
        #          f"5th: {self.bot.get_user(int(lb_table[4]['id'])).name}, {lb_table[4]['twincasts']} twincasts"
        # lb_round_str = f"1st: {self.bot.get_user(int(lb_round_table[0]['id'])).name}, " \
        #                f"{lb_round_table[0]['twincasts_round_dev-2']} twincasts\n" \
        #                f"2nd: {self.bot.get_user(int(lb_round_table[1]['id'])).name}, " \
        #                f"{lb_round_table[1]['twincasts_round_dev-2']} twincasts\n" \
        #                f"3rd: {self.bot.get_user(int(lb_round_table[2]['id'])).name}, " \
        #                f"{lb_round_table[2]['twincasts_round_dev-2']} twincasts\n" \
        #                f"4th: {self.bot.get_user(int(lb_round_table[3]['id'])).name}, " \
        #                f"{lb_round_table[3]['twincasts_round_dev-2']} twincasts\n" \
        #                f"5th: {self.bot.get_user(int(lb_round_table[4]['id'])).name}, " \
        #                f"{lb_round_table[4]['twincasts_round_dev-2']} twincasts"
        history = self.bot.get_channel(232937599537381377).history()
        round_name = r.table('rounds').get(r.table('info').get(0)['current_round_id'].
                                           run(self.conn))['round_name'].run(self.conn)
        if len(history) == 2:
            history.next().edit(embed=Embed(title="Top Twincasters (Global)", description=lb_str, colour=0x0000FF))
            history.next().edit(embed=Embed(title=f"Top Twincasters: Round {round_name}", description=lb_round_str,
                                            colour=0x0000FF))
        elif len(history) == 1:
            self.create_round_leaderboard(round_name, lb_round_str)
        elif len(history) == 0:
            self.create_round_leaderboard(round_name, lb_round_str)
            self.create_global_leaderboard(lb_round_str)


    @commands.command(aliases=["stats", "pinfo", "user", "u"], description="Get Twincast info about a user",
                      help="Shows how many twincasts, single casts, and failures a user has", usage="<user>",
                      brief="Get Twincast info about a user")
    @commands.cooldown(1, 8, BucketType.user)
    async def userinfo(self, ctx, user: Member = None):  # the function's name is our command name.
        if not user:
            user = ctx.author

        if r.table('users').get(str(user.id)).run(self.conn):
            if r.table('users').get(str(user.id)).has_fields('twincasts').run(self.conn):
                twincasts = r.table('users').get(str(user.id)).run(self.conn)['twincasts']
            else:
                twincasts = 0
        else:
            twincasts = 0
        if r.table('users').get(str(user.id)).run(self.conn):
            if r.table('users').get(str(user.id)).has_fields('single_casts').run(self.conn):
                single_casts = r.table('users').get(str(user.id)).run(self.conn)['single_casts']
            else:
                single_casts = 0
        else:
            single_casts = 0
        if r.table('users').get(str(user.id)).run(self.conn):
            if r.table('users').get(str(user.id)).has_fields('failures').run(self.conn):
                failures = r.table('users').get(str(user.id)).run(self.conn)['failures']
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
    bot.add_cog(Twincast(bot))  # Well, yeah. adds the extension/command.
