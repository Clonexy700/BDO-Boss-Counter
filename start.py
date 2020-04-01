from discord.ext import commands
import discord
# from discord import File, Member
# from discord.ext.commands import has_permissions, MissingPermissions
import bot_functions
# import os
from time_converter import TimeConverter
# import re
from datetime import datetime

time = datetime.now()
date_time = time.strftime("%d/%m/%Y %H:%M:%S")
hour = time.strftime("%H:%M:%S")

client = commands.Bot(command_prefix='bdo!')
functions = bot_functions.BotFunctions()
time_conv = TimeConverter()
client.remove_command("help")


@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord. {date_time}')

@client.event
async def on_command_error(self, exception):
    if isinstance(exception, commands.errors.CommandNotFound):
        pass

@client.command()
async def clear(ctx, amount=5):
    if(amount >= 0):
        await ctx.channel.purge(limit=amount+1)
    else:
        await ctx.send("Invalid argument")

@client.command()
async def notepad(ctx, name, message):
    await ctx.send(f"Zapisano wiadomość ```{name}``` ```{message}```")
    functions.save_notepad_message(name, message)


@client.command()
async def msg(ctx, name):
    await ctx.send(functions.show_notepad_message(name))

@client.event
async def on_message(message):
    if message.content.find("bdo!help") != -1:
        await message.channel.send(functions.help())

    elif message.content == "bdo!reset":
        nick = message.author.display_name
        await message.author.edit(nick=functions.resetNick(nick))

    elif message.content == "bdo!pt1":
        nick = message.author.display_name
        await message.author.edit(nick=functions.resetNick(nick))
        await message.author.edit(nick=functions.addParty(nick, party=1))

    elif message.content == "bdo!pt2":
        nick = message.author.display_name
        await message.author.edit(nick=functions.resetNick(nick))
        await message.author.edit(nick=functions.addParty(nick, party=2))

    elif message.content == "bdo!pt3":
        nick = message.author.display_name
        await message.author.edit(nick=functions.resetNick(nick))
        await message.author.edit(nick=functions.addParty(nick, party=3))

    elif message.content == "bdo!пользователи":
        await message.channel.send(f"Количество пользователей на сервере: {id.member_count}")

    elif message.content == "bdo!сегодня":
        await message.channel.send(embed=functions.all_todays_bosses())

    elif message.content == "bdo!завтра":
        await message.channel.send(embed=functions.all_tomorrows_bosses())

    elif message.content == "bdo!next":
        await message.channel.send(functions.todays_next_boss())

    await client.process_commands(message)

client.run('Njk0Nzg4NjY3NDMyMjM5MTg0.XoQ0qw.rnSuavvSPev-T5CpO44KKwV4DuM')
