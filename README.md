# TwincastBot
Discord bot to automate Twincast group puzzles.

## Run this bot yourself

 - Note: this bot is very old, hasn't been updated in forever, and even I don't understand parts of it. Use with caution.
 
 ### Requirements:
  - Python
  - discord.py
  - RethinkDB
  
  1. Create a discord developer application, copy the token and put it in `token.txt` in your main bot directory
  2. Edit constants in the code for the leaderboard/announcements channel/etc.
  3. Specify rounds in the `rounds` table using regex
  I don't remember what else you would need to do for setup, but hopefully you can figure it out from the context of the code. 
