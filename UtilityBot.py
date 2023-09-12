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

QOUTES = ['DefaultQuote1', 'DefaultQuote2', 'DefaultQuote3'
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
    async def on_message(message):
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
        with open('log'+server_id+'.csv', 'a', encoding='UTF8') as f:
            # create csv writer
            writer = csv.writer(f)

            writer.writerow(str_data)

    @client.hybrid_command(description='Find out your ping on Discord')
    async def get_ping(ctx):
        """Pings the user"""
        await ctx.send(f'Ping {round(client.latency * 1000)}ms')

    @client.hybrid_command(description='Get a random qoute')
    async def quote(ctx):
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
        await ctx.send(usr_qoute)

    @client.hybrid_command(description='Get all saved quotes')
    async def all_quote(ctx):
        """Get all saved quotes"""
        if os.path.isfile('quotes.txt'):
            with open('quotes.txt') as f:
                lines = f.readlines()
                if not lines:
                    usr_qoute = f'The quotes.txt file is empty, please first add qoutes using /add_qoute'
                else:
                    usr_qoute = lines
        else:
            usr_qoute = QOUTES
        await ctx.send(usr_qoute)

    @client.tree.command(name='ping_user')
    @app_commands.describe(who_to_ping="who would you like to ping ALOT", times="how many time to ping",
                           message="Set a custom message")
    async def ping_user(interaction: discord.Interaction, who_to_ping: str, times: str, message: str):
        """Pings the user up to 100 times"""
        if not times.isdigit():
            await interaction.response.send_message(f'Please make sure to set times as an integer')
            return

        num_times = int(times)

        if who_to_ping.startswith('<@'):
            await interaction.response.defer()
            await interaction.channel.send(f'Pinging in Progress')
            for _ in range(min(num_times, 100)):
                await interaction.channel.send(f'{message} {who_to_ping}')

            await interaction.followup.send('Pinging Complete')
        else:
            await interaction.response.send_message(f'Please make sure to @ the user')

    @client.tree.command(name='get_message_log')
    @app_commands.describe(num_messages="How many messages back would you like (max50)",
                           user="Specify a user or None for any")
    async def get_message_log(interaction: discord.Interaction, num_messages: str, user: str):
        """gets the last num_messages messages from the message log from user (or all users if None)"""
        await interaction.response.defer()
        if not num_messages.isdigit():
            await interaction.response.send_message(f'Please make sure to set num_messages as an integer')
            return

        guild_id = str(interaction.guild_id)

        if not os.path.isfile('log' + guild_id + '.csv'):
            await interaction.response.send_message(f'The message log for this server is empty')
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
                        await interaction.channel.send(f'{username} sent in {channel} at {time} the message: {usr_message}')
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

        await interaction.followup.send(f'Message log complete')

    @client.tree.command(name='add_quote')
    @app_commands.describe(quote="Quote you would like to add")
    async def add_quote(interaction: discord.Interaction, quote: str):
        """gets the last num_messages messages from the message log from user (or all users if None)"""
        await interaction.response.defer()
        with open('quotes.txt', 'a') as f:
            f.write(quote)
            f.write('\n')
        await interaction.followup.send('Quote has been added')

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
