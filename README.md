# UtilityDiscordBot
A Python based Discord bot!

## Description and functions
This Discord bot is designed to fill niche roles in managing a Discord server based on my own experience.

- Supports message logging:
messages sent in channels which the bot has access to read are saved to the log.csv file. Tired of that person who keeps on deleting messages, or want to have a backup of the messages sent on a server, this is the way to do it!
- Serverwide access to the message log (get_message_log):
this slash command allows anyone on the server with the perms to use slash commands to read up to approximately the last 50 messages. This provides transparency in message logging to the server.
- Pinging users (ping_user):
Pings a selected user or role for up to 100 times. Need to get the attention of someone? This is the tool to do it!
- Get your ping (get_ping):
Server feeling laggy in voice call? Use this tool to quickly check your Discord ping!
- Quotes (quote/add_quote/all_quotes):
Got a series of funny messages you want to save? Use this tool to save and randomly access these messages whenever you want.
- Fully customisable:
Don't like a function, want to add something else? This code serves as a template for you to customise yourself! There a variety of different command call structures as examples, and debugging tools available to help you along.

## How to use it yourself?
1) Download the source code.
2) Visit https://discord.com/developers/docs/intro to create a bot/application.
3) While there, be sure to save the application token and grant it the nesscary permissions (please ensure that the message intents is enabled). Other permissions are up to your discretion (you probably want to allow reading of messages and sending messages).
5) Run the main.py file using a python envrionment of your choice (make sure the packages in requirements.txt are satisfied).
6) When prompted, enter the token you saved from step 3.
7) Create an auth link in the developer portal to invite the bot to your server.
8) Voila! The bot should now be integrated to your server and ready for use!

## Example of usage
Use this link to add an example version of the bot to your server. The quote and get_message_log functions have been disabled for security:

https://discord.com/api/oauth2/authorize?client_id=1149769710649487462&permissions=19235213409360&scope=bot

If this bot is offline, to turn it on, simply visit:  http://henrytchen.com/UtilityDiscord

Author: Henry "TJ" Chen

Feel free to reach out to me with any questions or concerns!
