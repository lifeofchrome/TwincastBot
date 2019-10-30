# TwincastBot
Discord bot to automate Twincast group puzzles.

## What is Twincast?
Twincast is a group puzzle where the goal is to cast a word that satisfies two sets of criteria, which are referred to by an example word that fufills only that criteria.

Example:
**ball** and **squeak**
In this example, ball's criteria is having two of the same letter and squeak's is having a triple vowel.
The following words would cast **ball**: caterpillar, shatters, clapped
The following words would cast **squeak**: hideout, quiet, adieu

The following words would ***twincast***: erroneous, bouillon, tonneau

## How does this bot work?
This bot isn't intended for general-purpose use in multiple servers, and many discord snowflake IDs are hardcoded. I have a server setup that I run the bot in and its channels are intertwined with the bot.

Here's the channel setup I have (the bot sends messages to each channel):
#announcements for the current round and round history
#leaderboard for the leaderboard of successes per user on individual word casts and twincasts, round independent
#twincasts for successful twincasts
#pretentiousness for successful casts of the first word (note: channel name changes each round)
#cooperated for successful casts of the second word (note: channel name changes each round)
#failures for unsuccessful casts

Currently, there are only 3 commands:
 - `!submit <word>`: Submits a word. The word must be of the English language and be 6 or more characters in length.
 - `!ping`: Gets the bot's ping.
 - `!notify`: Toggles notifications of new rounds.

## Credits
Primary development/management - lifeofchrome
Idea - SethBling
Bot Help - @srgood#8363 , @Damien Moon#2025 , everyone else who has helped

## Run this bot yourself

 - Note: this bot is very old, hasn't been updated in forever, and even I don't understand parts of it. Use with caution.
 
 ### Requirements:
  - Python
  - discord.py
  - RethinkDB
  
  1. Create a discord developer application, copy the token and put it in `token.txt` in your main bot directory
  2. Edit constants in the code for the leaderboard/announcements channel/etc.
  3. Specify rounds in the `rounds` table using regex
  4. Add `english-words.txt` to your main bot directory containing a list of English words. You can use this word list: http://www-01.sil.org/linguistics/wordlists/english/wordlist/wordsEn.txt
  I don't remember what else you would need to do for setup, but hopefully you can figure it out from the context of the code. 
