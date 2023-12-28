"""The utility bot"""

import discord
from discord import app_commands
from discord.ext import commands

import csv
import datetime
import random
import os

intents = discord.Intents.default()
intents.message_content = True

QOUTES = ['Example qoute 1', 'Example qoute 2'
          ]

client = commands.Bot(command_prefix='/', intents=intents)


def run_discord_bot(token: str):
    """Runs the Discord Bot"""
    intents = discord.Intents.default()
    intents.message_content = True

    # when the bot gets started, it will call this
    @client.event
    async def on_ready():
        """When the bot gets started, it will call this"""
        activity = discord.Game(name='Visit https://github.com/LatinScribe/UtilityDiscordBot for more info', type=1)
        await client.change_presence(status=discord.Status.online, activity=activity)
        print(f'{client.user} is now running!')
        try:
            synced = await client.tree.sync()
            print(f'Synced {len(synced)} command(s)')
        except Exception as e:
            print(e)

    @client.event
    async def on_message(message: discord.Message):
        """Handle the messages"""
        # make sure the author is not the bot to prevent inifinite loop
        if message.author == client.user:
            return

        server_id = str(message.guild.id)
        server_name = str(message.guild)
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)
        time = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        str_data = [server_id, server_name, username, user_message, channel, time]

        print(f"{username} said: '{user_message}' ({channel}) ({time}) in {server_name} ({server_id})")
        with open('log' + server_id + '.csv', 'a', encoding='UTF8') as f:
            # create csv writer
            writer = csv.writer(f)

            writer.writerow(str_data)

    @client.event
    async def on_message_edit(before: discord.Message, after: discord.Message):
        """Handle the message edit"""
        # make sure the author is not the bot to prevent inifinite loop
        if before.author == client.user or after.author == client.user:
            return

        server_id = str(after.guild.id)
        server_name = str(after.guild)
        username = str(after.author)
        after_message = str(after.content)
        before_message = str(before.content)
        channel = str(after.channel)
        time = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        str_data = [server_id, server_name, username, after_message, channel, time]

        print(f"{username} said: '{after_message}' ({channel}) ({time}) in {server_name} ({server_id})")
        with open('log' + server_id + '.csv', 'a', encoding='UTF8') as f:
            # create csv writer
            writer = csv.writer(f)

            writer.writerow(str_data)

        embed = discord.Embed(title=f'{str(after.author)} edited a Message', colour=discord.Colour.gold())
        embed.set_author(name=after.author, icon_url=after.author.avatar)
        embed.add_field(name="Edited Message", value=after_message)
        embed.add_field(name="Original Message", value=before_message, inline=False)
        # await after.channel.send(f'{username} edited message {before_message} to read {after_message}')
        await after.channel.send(embed=embed)

    @client.event
    async def on_message_delete(message: discord.Message):
        """Handle the message edit"""
        # make sure the author is not the bot to prevent inifinite loop
        if message.author == client.user:
            return

        deleter = None
        async for entry in message.guild.audit_logs(limit=1):
            deleter = entry.user

        username = str(message.author)
        pfp = deleter.avatar
        id = str(message.author.id)
        print(id)
        after_message = str(message.content)
        # pfp = message.guild.get_member(id).avatar_url
        print(pfp)

        embed = discord.Embed(title=f'{str(deleter)} Deleted a Message', description=f'{username}\'s message was deleted!', colour=discord.Colour.red())
        embed.set_author(name=deleter, icon_url=pfp)
        embed.add_field(name="Deleted Message", value=after_message)
        # embed.set_image(url=pfp)

        # await message.channel.send(f'{username}\'s message was deleted. Original message: {after_message}')
        await message.channel.send(embed=embed)

    @client.hybrid_command(description='Find out your ping on Discord')
    async def get_ping(ctx: discord.ext.commands.Context):
        """Pings the user"""
        await ctx.send(f'Ping {round(client.latency * 1000)}ms')

    @client.hybrid_command(description='Get a random qoute')
    async def quote(ctx: discord.ext.commands.Context):
        """Get a random quote"""
        if os.path.isfile('quotes.txt'):
            with open('quotes.txt') as f:
                lines = f.readlines()
                if not lines:
                    usr_qoute = f'The qoutes.txt file is empty, please first add qoutes using /add_qoute'
                else:
                    usr_qoute = random.choice(lines)
        else:
            usr_qoute = random.choice(QOUTES)
        embed = discord.Embed(title=usr_qoute, colour=discord.Colour.random())
        await ctx.send(embed=embed)
        # await ctx.send(usr_qoute)

    @client.hybrid_command(description='Get all saved quotes')
    async def all_quote(ctx: discord.ext.commands.Context):
        """Get a random qoute"""
        await ctx.defer()

        embed = discord.Embed(title="All Saved Qoutes", colour=discord.Colour.random())

        if os.path.isfile('qoutes.txt'):
            with open('qoutes.txt') as f:
                lines = f.readlines()
                if not lines:
                    usr_qoute = f'The qoutes.txt file is empty, please first add qoutes using /add_qoute'
                    embed.add_field(name="ERROR", value=usr_qoute)
                    await ctx.send(embed=embed)
                else:
                    for line in range(0, len(lines)):
                        embed.add_field(name=f'Qoute {line}', value=lines[line], inline=False)

        else:
            usr_qoute = QOUTES
            for line in range(0, len(usr_qoute)):
                embed.add_field(name=f'Qoute {line}', value=usr_qoute[line], inline=False)

        await ctx.send(embed=embed)
        # await ctx.send(usr_qoute)

    @client.tree.command(name='ping_user')
    @app_commands.describe(who_to_ping="who would you like to ping ALOT", times="how many time to ping",
                           message="Set a custom message")
    async def ping_user(interaction: discord.Interaction, who_to_ping: str, times: str, message: str):
        """Pings the user up to 100 times"""
        if not times.isdigit():
            embed = discord.Embed(title="Please make sure to set times as an integer", colour=interaction.user.accent_color)
            await interaction.response.send_message(embed=embed)
            # await interaction.response.send_message(f'Please make sure to set times as an integer')
            return

        num_times = int(times)

        if who_to_ping.startswith('<@'):
            await interaction.response.defer()
            await interaction.channel.send(f'Pinging in Progress')
            for _ in range(min(num_times, 100)):
                await interaction.channel.send(f'{message} {who_to_ping}')

            embed = discord.Embed(title="Pinging Complete", colour=interaction.user.accent_color)
            await interaction.followup.send(embed=embed)
        else:
            # await interaction.response.send_message(f'Please make sure to @ the user')
            embed = discord.Embed(title="Please make sure to @ the user", colour=interaction.user.accent_color)
            await interaction.response.send_message(embed=embed)

    @client.tree.command(name='get_message_log')
    @app_commands.describe(num_messages="How many messages back would you like (max50)",
                           user="Specify a user or None for any")
    async def get_message_log(interaction: discord.Interaction, num_messages: str, user: str):
        """gets the last num_messages messages from the message log from user (or all users if None)"""
        await interaction.response.defer()

        if not num_messages.isdigit():
            embed = discord.Embed(title="Please make sure to set num_messages as an integer", colour=interaction.user.accent_color)
            await interaction.response.send_message(embed=embed)
            # await interaction.response.send_message(f'Please make sure to set num_messages as an integer')
            return

        guild_id = str(interaction.guild_id)

        if not os.path.isfile('log' + guild_id + '.csv'):
            embed = discord.Embed(title="The message log for this server is empty",
                                  colour=interaction.user.accent_color)
            await interaction.response.send_message(embed=embed)
            # await interaction.response.send_message(f'The message log for this server is empty')
            return

        num_times = (int(num_messages)) * 2 + 1

        with open('log' + guild_id + '.csv', 'r') as f:
            messages = f.readlines()

        real_num = min(100, num_times, len(messages))
        if user == 'None':
            for num in range(1, real_num):
                message = messages[-num]
                message_data = message.split(',')
                if not len(message_data) < 6:
                    server_id = message_data[0]
                    # server_name = message_data[1]
                    username = message_data[2]
                    usr_message = message_data[3]
                    channel = message_data[4]
                    time = message_data[5]
                    if guild_id == str(server_id):
                        await interaction.channel.send(
                            f'{username} sent in {channel} at {time} the message: {usr_message}')
        else:
            for num in range(1, real_num):
                message = messages[-num]
                message_data = message.split(',')
                if not len(message_data) < 6:
                    server_id = message_data[0]
                    # server_name = message_data[1]
                    username = message_data[2]
                    usr_message = message_data[3]
                    channel = message_data[4]
                    time = message_data[5]
                    if username == user and guild_id == str(server_id):
                        await interaction.channel.send(
                            f'{username} sent in {channel} at {time} the message: {usr_message}')

        embed = discord.Embed(title="Message log complete", colour=interaction.user.accent_color)
        await interaction.followup.send(embed=embed)
        # await interaction.followup.send(f'Message log complete')

    @client.tree.command(name='add_quote')
    @app_commands.describe(quote="Quote you would like to add")
    async def add_quote(interaction: discord.Interaction, quote: str):
        """gets the last num_messages messages from the message log from user (or all users if None)"""
        await interaction.response.defer()
        with open('quotes.txt', 'a') as f:
            f.write(quote)
            f.write('\n')
        # await interaction.followup.send('Quote has been added')
        embed = discord.Embed(title="Quote has been added", colour=interaction.user.accent_color)
        await interaction.followup.send(embed=embed)


    # @client.command()
    # async def test(ctx):
    #     await ctx.channel.send('Hello!')

    @client.command()
    async def ping_me_alot(ctx):
        """Welcomes the user"""
        for _ in range(20):
            await ctx.channel.send(f'Welcome {ctx.author.mention}')

    @client.command()
    async def debug(ctx):
        """Debugging Tool"""
        await ctx.send(f'The context is {ctx} \nChannel Name: {ctx.channel.name}'
                       f'\nChennel ID: {ctx.channel.id}'
                       f'\nServer name {ctx.guild.name}'
                       f'\nServer ID: {ctx.guild.id}')

    @client.command(aliases=['se'])
    async def sampleembed(ctx):
        """Example of embed"""
        embed = discord.Embed(title='Title', description='Text')
        await ctx.send(embed=embed)

    client.run(token)
