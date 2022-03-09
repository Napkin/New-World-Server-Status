from numpy import str_
import config
import requests
from bs4 import BeautifulSoup, Tag

import discord
from discord.ext import tasks, commands

from datetime import datetime

try:
    lastTimeChecked: tuple[datetime, str]
except:
    lastTimeChecked = None


zones_array = ['US WEST', 'US EAST', 'SA EAST', 'EU CENTRAL', 'AP SOUTHEAST']
zones_arr = {}
ts = 0

bot = commands.Bot(command_prefix='$')




def get_status(server):
    zone_class = "ags-ServerStatus-content-responses-response"
    server_class = zone_class + "-server"
    server_name_class = server_class + "-name"
    server_status_class = server_class + "-status"

    URL = "https://www.newworld.com/en-us/support/server-status"

    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    timeChunk: Tag = soup.find("div", class_="ags-ServerStatus-content-lastUpdated")  
    timeChunk: str = timeChunk.contents[0].split(":", 1)[1].strip()[:-7]

    dt = datetime.strptime(timeChunk, "%B %d, %Y %H:%M:%S")

    if lastTimeChecked:
        if dt <= lastTimeChecked[0]:
            return lastTimeChecked[1]

    chunks = soup.find_all("div", class_=server_class)
    for chunk in chunks:
        if server in chunk.find("div", class_=server_name_class).text:
            status = chunk.find("div", class_=server_status_class)
            server_status = ""
            if ((server_status_class + "--down") in status.attrs.get("class")):
                server_status = "Down"
            elif ((server_status_class + "--maintenance") in status.attrs.get("class")):
                server_status = "Maintenance"
            else:
                server_status = "Up"
            lastTimeChecked = (dt, server_status)
            return server_status
    return "Unknown"

async def send_message_to_channel(channel_id: int, text: str):
    channel: TextChannel = bot.get_channel(channel_id)
    await channel.send(text)

class my_cog(commands.Cog):

    def __init__(self, bot):
        self.our_server = config.our_server
        self.our_status = "Up"
        self.bot = bot
        self.scrapper.start()

    def cog_unload(self):
        self.scrapper.cancel()

    @tasks.loop(seconds=180.0)
    async def scrapper(self):
        new_status = get_status(self.our_server)
        if self.our_status != new_status:
            precise_now = datetime.now().strftime("%Y_%m_%d-%H:%M:%S")
            hmonly_now = datetime.now().strftime("%H:%M")
            print("I changed status from {} to {} ({}).".format(self.our_status, new_status, precise_now))
            self.our_status = new_status
            await send_message_to_channel(config.channel_id, "My status is now \"{}\"! {} ({} CET)".format(self.our_status, config.emoji_status[self.our_status], hmonly_now))

    @scrapper.before_loop
    async def before_scrapper(self):
        print('Connecting...')
        await self.bot.wait_until_ready()

async def multiprint(ctx, text):
        i = 0
        tText = []
        pText = ""
        tOffset = 0
        for c in text:
                pText += c
                i+=1
                lastPos = text.find('\n',i)
                if i == 2000 or (c=='\n' and lastPos > 2000):
                        tText.append(pText)
                        i = 0
                        tOffset += 2000
                        pText = ""
        if pText != "":
                tText.append(pText)

        for t in tText:
                await ctx.send(t)

#print our user name
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

#gets all the zones
@bot.command()
async def zones(ctx):
        text = ""
        for x in zones_array:
                text += x.title() + '\r\n'
        await multiprint(ctx, text)

#gets all the servers
@bot.command()
async def all(ctx):
        arr = server_scrape()
        text = ""
        for x in arr.keys():
                text += x.title() + "\r\n"
                for server in arr[x]:
                        text += '\t' + server["name"] + ": " + server["status"] + " " + config.emoji_status[server["status"]] + "\r\n"

        await multiprint(ctx, text)
	
#gets specific server
@bot.command()
async def server(ctx, *,arg):
        temp_arr = server_scrape()
        temp_arr = [[x for x in v if x['name'].upper() == arg.upper()] for v in temp_arr.values()]
        temp_arr = [x for x in temp_arr if x]
        if temp_arr:
                temp_arr = temp_arr[0][0]
                text = temp_arr["name"] + ': ' + temp_arr["status"] + " " + config.emoji_status[temp_arr["status"]]
        else:
                text = "No server found!"

        await multiprint(ctx,text)

#gets specific zone servers
@bot.command()
async def zone(ctx, *,arg):
        arr = server_scrape()
        text = ""
        print("Requested zone: " + arg)
        arg = arg.upper()
        if arg in arr.keys():
                for server in arr[arg]:
                        text += server["name"] + ": " + server["status"] + " " + config.emoji_status[server["status"]] + "\r\n"
        else:
                text = "No zone found!"

        await multiprint(ctx,text)

def server_scrape():
        global zones_arr
        global ts

        if datetime.timestamp(datetime.now()) - ts < (5 * 60 * 1000):
                return zones_arr

        zone_class = "ags-ServerStatus-content-responses-response"
        server_class = zone_class + "-server"
        server_name_class = server_class + "-name"
        server_status_class = server_class + "-status"

        URL = "https://www.newworld.com/it-it/support/server-status"
        page = requests.get(URL)

        soup = BeautifulSoup(page.content, "html.parser")
        zones = soup.find_all("div", class_=zone_class)
        zones_arr = {}

        for zone in zones:
                servers = zone.find_all("div", class_=server_class)
                servers_arr = []
                for server in servers:
                        name = server.find("div", class_=server_name_class)
                        status = server.find("div", class_=server_status_class)
                        server_status = ""
                        server_obj = {}
                        if ((server_status_class + "--up") in status.attrs.get("class")):
                                server_status = "Up"
                        elif ((server_status_class + "--down") in status.attrs.get("class")):
                                server_status = "Down"
                        elif ((server_status_class + "--full") in status.attrs.get("class")):
                                server_status = "Full"
                        elif ((server_status_class + "--maintenance") in status.attrs.get("class")):
                                server_status = "Maintenance"
                        elif ((server_status_class + "--noTransfer") in status.attrs.get("class")):
                                server_status = "NoTransfer"
                        else:
                                server_status = "Unknown"
                        server_obj['name'] = name.text.replace("\n","").replace("\r","").replace(" ","")
                        server_obj['status'] = server_status
                        servers_arr.append(server_obj)
                zones_arr[(zones_array[int(zone.attrs.get('data-index'))])] = servers_arr

        ts = datetime.timestamp(datetime.now())
        return zones_arr

cog = my_cog(bot)
bot.run(config.key)
