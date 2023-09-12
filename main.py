"""Discord Bot for emphasizing that Patrick is a Simp for Mercy

This file will run the bot
"""
import UtilityBot
import os


def run_utility_bot():
    """runs the bot"""
    if os.path.isfile('token.txt'):
        with open('token.txt', 'r') as f:
            lines = f.readlines()
            token = lines[0]
    else:
        token = input("Please enter the token")

    UtilityBot.run_discord_bot(token)


if __name__ == '__main__':
    # run the bot
    run_utility_bot()
