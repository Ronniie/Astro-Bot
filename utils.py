import discord
import json
import os
from dotenv import load_dotenv


def ensure_data_directory_exists():
    if not os.path.exists('data'):
        os.makedirs('data')


def read_cache():
    ensure_data_directory_exists()
    cache_file_path = 'data/cache.json'
    if not os.path.exists(cache_file_path):
        return {}

    try:
        with open(cache_file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error reading cache: {e}")
        return {}


def write_cache(new_data):
    ensure_data_directory_exists()
    cache_file_path = 'data/cache.json'

    # Read the existing cache
    existing_cache = read_cache()

    # Update the cache with new data
    # This will replace existing keys and add new ones
    existing_cache.update(new_data)

    # Write the updated cache back to the file
    try:
        with open(cache_file_path, 'w') as f:
            json.dump(existing_cache, f)
    except Exception as e:
        print(f"Error writing cache: {e}")


async def send_embeds_from_json(bot, channel_id, embeds_key, view=None):
    channel = bot.get_channel(channel_id)
    if not channel:
        print(f"Channel with ID {channel_id} not found.")
        return

    print(f"Sending embeds to {channel.name}")

    message_ids = []
    with open('data/embeds.json', 'r') as file:
        data = json.load(file)

        # Handle nested keys
        keys = embeds_key.split('.')
        for key in keys:
            data = data.get(key, {})
        embeds = data if isinstance(data, list) else []

        for i, embed_info in enumerate(embeds):
            embed = discord.Embed(
                title=embed_info.get("title", ""),
                description=embed_info.get("description", ""),
                color=int(embed_info.get("color", "#000000").strip("#"), 16)
            )

            # Add image if present
            if embed_info.get("image"):
                embed.set_image(url=embed_info["image"])

            # Add view to the last message
            current_view = view if i == len(embeds) - 1 else None

            message = await channel.send(embed=embed, view=current_view)
            message_ids.append(message.id)

    return message_ids


def settings(setting):
    # Load settings from .env, if it exists
    load_dotenv()

    # Return the setting, proper type depending on the setting
    if setting == "BOT_TOKEN":
        return os.getenv("BOT_TOKEN")
    else:
        return int(os.getenv(setting))
