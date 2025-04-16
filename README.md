# SegfaultBot.py
I started working on a new Discord bot (again)

## This is a work in progress project I just started
A music bot that uses discord.py and Lavalink. I'll be updating it with some of the fun ideas I have in mind.

## Requirements to run the bot

1. Python 3.8 or newer
2. Latest LTS release of Java

## How to run the bot yourself

1. [Download the latest Lavalink release](https://github.com/lavalink-devs/Lavalink/releases) and paste it into the main directory of the project.
2. Configure `application.yml` config file for Lavalink or [grab the example one](https://lavalink.dev/configuration/) and run Lavalink:
```
java -jar Lavalink.jar
```
3. Create a `.env` file containing the bot token and the Lavalink server credentials as following:
```
BOT_TOKEN=YOUR_BOT_TOKEN_GOES_HERE
LAVALINK_HOST=LAVALINK_HOST_ADDRESS_GOES_HERE
LAVALINK_PORT=LAVALINK_PORT_GOES_HERE
LAVALINK_PASS=LAVALINK_PASSWORD_GOES_HERE
```
4. Create a virtual environment for the bot (so you don't accidentally mess up some libs used by the system):
```
pipenv shell
```
5. Install all project dependencies:
```
pip install -r requirements.txt
```
6. Run the bot:
```
python bot.py
```

Stuff used for the project: discord.py (by Rapptz), Lavalink, Pomice wrapper (by cloudwithax)
