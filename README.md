# SegfaultBot.py
I started working on a new Discord bot (again)

## This is a work in progress project I just started
A music bot that uses discord.py and Lavalink. I'll be updating it with some of the fun ideas I have in mind.

## How to run the bot yourself

1. Download the latest Lavalink release and paste it into the main directory of the project (https://github.com/lavalink-devs/Lavalink/releases)
2. Configure your 'application.yml' file or grab the example one from here https://lavalink.dev/configuration/ and run Lavalink 'java -jar Lavalink.jar'
3. Create a '.env' file containing the bot token as following: BOT_TOKEN=YOUR_TOKEN_GOES_HERE
4. Create a virtual environment for the bot (so you don't accidentally mess up some libs used by the system) - 'pipenv shell'
5. Install the required libs using pip install -r requirements.txt
6. Run the bot - 'python bot.py'

Stuff used for the project: discord.py (by Rapptz), Lavalink, Pomice wrapper (by cloudwithax)
