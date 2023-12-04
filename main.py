import asyncio

import discord
from discord.ext import commands
import os
import utils

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True  # If you're using message content

cogs = ["events", "cogs"]

client = commands.Bot(command_prefix="!", intents=intents)


async def load_extensions():
    for filename in os.listdir("./events"):
        if filename.endswith(".py"):
            await client.load_extension(f"events.{filename[:-3]}")


async def main():
    async with client:
        await load_extensions()
        await client.start(utils.settings("BOT_TOKEN"))


asyncio.run(main())
