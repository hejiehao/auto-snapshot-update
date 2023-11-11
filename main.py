import discord
from discord import app_commands
from utils.open_json import *
import requests

# open config.json
config = open_json('./config/config.json')

MY_GUILD = discord.Object(id=config['guild_id'])  # replace with your guild id

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

    # In this basic example, we just synchronize the app commands to one guild.
    # Instead of specifying a guild to every command, we copy over our global commands instead.
    # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)


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
    await interaction.response.send_message(f"最新的版本为：{newest.json()['version']}\n下载链接：{newest.json()['jar']}")

client.run(config['token'])