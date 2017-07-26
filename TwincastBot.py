import discord
from discord.ext import commands # Imports the ability to use the command system
from discord import Embed

description = '''TwincastBot Alpha
Commands:''' # The description of the bot when typing chromebot help

# this specifies what extensions to load when the bot starts up
# so for example, "commands.ping" in this list, it will load the extension AKA command, commands/ping.py
startup_extensions = [
    "commands.ping",
    "commands.submit"
]

# the variable "bot" will define our Discord bot's commands.
# command_prefix is the prefix the bot will use when typing commands, for example >help  or  >ping  and so on. . .
# description is equal to the description of the >help command.
bot = commands.Bot(command_prefix='!', description=description)
client = discord.Client()

@bot.event
async def on_ready():
    # This is to show that the bot has successfully started.
    # It bot.user.name shows the bots name, and bot.user.id shows the bot's ID.
    print('Ready!')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return
#     print(message.content)
#     msg_content = message.content.lower()
#     if msg_content.startswith('[') and msg_content.endswith(']') and " " not in msg_content:
#         word = msg_content[1:-1]
#         submit_word(word)
#         await message.channel.send(embed=Embed(description=":white_check_mark: Submitted %s" % word, colour=0x00FF00))
#         await bot.process_commands(message)

# This if statement below checks for the extensions/commands to load up while starting the bot.
# In this case, it will load commands/ping.py (commands.ping)
if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e2: # If it fails to load the extension/command, it will print this exception.
            exc = '{}: {}'.format(type(e2).__name__, e2)
            print('Failed to load extension {}\n{}'.format(extension, exc))
    with open('token.txt', 'r') as tokenFile:
        token = tokenFile.read()
    bot.run(token)
