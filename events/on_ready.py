import json

import discord
from discord.ext import commands
from discord.ui import Button, View
import utils


class VerificationView(View):
    def __init__(self, role_id):
        super().__init__()
        self.role_id = role_id

    @discord.ui.button(label="Verify", style=discord.ButtonStyle.green)
    async def verify_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            guild = interaction.guild
            if guild:
                role = guild.get_role(self.role_id)
                if role:
                    member = interaction.user
                    if member:
                        if role not in member.roles:
                            await member.add_roles(role)
                            await interaction.response.send_message(f"You have been verified with {role.mention}!", ephemeral=True)
                        else:
                            await interaction.response.send_message(f"You already have {role.mention}!", ephemeral=True)
                    else:
                        await interaction.response.send_message("Member not found in the guild.", ephemeral=True)
                else:
                    await interaction.response.send_message("Role not found.", ephemeral=True)
            else:
                await interaction.response.send_message("Guild not found.", ephemeral=True)
        except Exception as e:
            print(f"Error in verify_button: {e}")
            await interaction.response.send_message("An error occurred.", ephemeral=True)


class OnReadyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Logged in as {self.bot.user}")

        game = discord.Game("Hunting Trophies 🏆")
        await self.bot.change_presence(status=discord.Status.online, activity=game)

        cache = utils.read_cache()
        prev_message_ids = cache.get("verification_message_ids", [])

        # Delete previous messages
        channel = self.bot.get_channel(utils.settings("VERIFICATION_CHANNEL_ID"))
        if channel:
            for msg_id in prev_message_ids:
                try:
                    msg = await channel.fetch_message(msg_id)
                    await msg.delete()
                except Exception as e:
                    print(f"Error deleting message {msg_id}: {e}")

        try:
            # Send new welcome embeds and store their IDs
            message_ids = await utils.send_embeds_from_json(
                self.bot,
                utils.settings("VERIFICATION_CHANNEL_ID"),
                "on_ready.welcome",
                VerificationView(utils.settings("VERIFICATION_ROLE_ID"))
            )

            # Update cache with new message IDs
            utils.write_cache({"verification_message_ids": message_ids})
        except Exception as e:
            print(f"Error while sending message: {e}")

        # Send new rules embeds and store their IDs
        try:
            # Get previous message IDs
            prev_message_ids = cache.get("rules_message_ids", [])

            # Delete previous messages
            channel = self.bot.get_channel(utils.settings("RULES_CHANNEL_ID"))

            if channel:
                for msg_id in prev_message_ids:
                    try:
                        msg = await channel.fetch_message(msg_id)
                        await msg.delete()
                    except Exception as e:
                        print(f"Error deleting message {msg_id}: {e}")

            message_ids = await utils.send_embeds_from_json(
                self.bot,
                utils.settings("RULES_CHANNEL_ID"),
                "on_ready.rules"
            )

            # Update cache with new message IDs
            utils.write_cache({"rules_message_ids": message_ids})

        except Exception as e:
            print(f"Error while sending message: {e}")


async def setup(client):
    await client.add_cog(OnReadyCog(client))
