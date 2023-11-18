import discord
from discord import app_commands
from utils.open_json import *
import requests
import logging
import logging.handlers
import os

if os.path.exists("./discord.log"):
    os.remove("./discord.log")

# Set up logging
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
logging.getLogger('discord.http').setLevel(logging.INFO)

handler = logging.handlers.RotatingFileHandler(
    filename='discord.log',
    encoding='utf-8',
    maxBytes=32 * 1024 * 1024,  # 32 MiB
    backupCount=5,  # Rotate through 5 files
)
dt_fmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
handler.setFormatter(formatter)
logger.addHandler(handler)

# open config.json
config = open_json('./config/config.json')

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        # A CommandTree is a special type that holds all the application command
        # state required to make it work. This is a separate class because it
        # allows all the extra state to be opt-in.
        # Whenever you want to work with application commands, your tree is used
        # to store and work with them.
        # Note: When using commands.Bot instead of discord.Client, the bot will
        # maintain its own tree instead.
        self.tree = app_commands.CommandTree(self)


intents = discord.Intents.default()
client = MyClient(intents=intents)


@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')


@client.tree.command()
async def new(interaction: discord.Interaction):
    """Get the newest version"""
    newest = requests.get("https://github.com/burningtnt/HMCL-Snapshot-Update/raw/master/datas/snapshot.json")
    await interaction.response.send_message(f"最新的版本为：{newest.json()['version']}\n下载链接：{newest.json()['jar']}\nGitHub Commit：https://github.com/huanghongxun/HMCL/commit/{newest.json()['version'][8:]}")

client.run(config['token'], log_handler=None)