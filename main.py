# External libraries
import os
import logging
from dotenv import load_dotenv
load_dotenv()
import discord
from discord import channel
from mcstatus import MinecraftServer
import requests


# Custom logger class
class CustomFormatter(logging.Formatter):
    """Logging Formatter to add colors and count warning / errors"""

    grey = "\x1b[38;21m"
    yellow = "\x1b[33;21m"
    red = "\x1b[31;21m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

# Create logger with application name
logger = logging.getLogger("Status_Bot")
logger.setLevel(logging.DEBUG)

# Create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

ch.setFormatter(CustomFormatter())

logger.addHandler(ch)

# Load token from .env
TOKEN = os.environ.get("TOKEN")
logger.info("Loaded Token From .env")

client = discord.Client()

# Log ready event
@client.event
async def on_ready():
    logger.info('Logged in as {0.user}'.format(client))


# Get server status
IP = os.environ.get("IP")
s=IP
server = MinecraftServer.lookup(IP)
status = server.status()
logger.info("Got server status")


# Server status command
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$status'):
        data = {
            "content" : "",
            "username" : "SkyMineMC Status Bot",
            "avatar_url" : "https://cdn.iconscout.com/icon/free/png-256/bot-138-505021.png"
        }

        data["embeds"] = [
            {
                "description" : "The server has `{0}` players and replied in `{1}` ms".format(status.players.online, status.latency),
                "title" : f"The current status for `{s}` is:",
                
                "color": "15552334"
            }
        ]
        URL = os.environ.get("URL")
        result = requests.post(URL, json = data)
        try:
            result.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)
        else:
            logger.info("Payload delivered successfully, code {}.".format(result.status_code))

        

client.run(TOKEN)