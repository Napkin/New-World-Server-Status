# New World Server Status
Discord bot to know the status of the New World game server status

This bot is intented to only know the status of the servers of the various regions. I don't own any of the data provided by the bot, it is all obtained by scraping the support page of the official game here: https://www.newworld.com/en-us/support/server-status

Actually, it's taken from https://www.newworld.com/it-it/support/server-status because that localized version has less bugs.

The bot returns the status of each server according to the support page:

`Up ✅`: The server is on.

`Down ❌`: The server is down.

`Full ⛔`: The server is full and doesn't accept new player for now.

`Maintenance ⚠️`: The server is down for maintenance.

`NoTransfer 🛂`: The server is on but doesn't allow character transfers.

`Unknown ❓`: In case AGS adds new stati in the future.

# Setup

This bot is written in python, and uses the following libraries:

[BeautifulSoap4](https://pypi.org/project/beautifulsoup4/)

[Discord.py](https://pypi.org/project/discord.py/)

[requests](https://pypi.org/project/requests/)

# Discord Setup

I suggest to follow the guide at [Discord.py](https://discordpy.readthedocs.io/en/stable/index.html) on how to create the bot in the Discord [Developer Portal](https://discord.com/developers/applications).

When using the OAuth2 URL Generator, as far as I can tell, this bot only needs permissions to 'Read Messages/View Channels' and 'Send Messages'.

# Functions

The bot can filter by Zone and by Server, so you can get all the servers in a zone and a specific server. Remember that this bot is case unsensitive for the commands arguments, so you can write "US WEST" and "us west", it will be the same for it.

# Usage

`$zone [zone]` - gets all servers of the provided zone.

`$server [server]` - gets the provided server.

`$zones` - gets all the available zones.

`$all` - gets all servers divided by zone.

For full game info go to https://www.newworld.com/

Examples:

```
$zone US West

Aarnivalkea: Up ✅
Adlivun: Up ✅
Aeaea: Up✅
...
```
```
$server Atvatabar

Atvatabar: Full⛔
```
```
$zones

US West
AP Southeast
...
```
```
$all

Us East
    Aarnivalkea: Up ✅
    Adlivun: Up ✅
    Aeaea: Up ✅
...
```
