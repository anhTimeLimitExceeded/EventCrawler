import asyncio
import discord
import datetime
from discord.ext import commands, tasks
import logging
import json

logging.basicConfig(handlers=[logging.FileHandler(filename="main.log",
                                                  encoding='utf-8', mode='a+')],
                    format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
                    datefmt='%H:%M:%S',
                    level=logging.INFO)

logger = logging.getLogger('discord-bot')


class DiscordBot(commands.Bot):

    def __init__(self, command_prefix, self_bot, dataHolder):
        commands.Bot.__init__(self, command_prefix=command_prefix, self_bot=self_bot)
        self.dataHolder = dataHolder
        self.add_commands()
        self.sendTodayFreeFood.start(self)

    async def on_ready(self):
        print(f'We have logged in as {self.user}')

    def add_commands(self):
        @self.command(name="status", pass_context=True)
        async def status(ctx):
            await ctx.channel.send('alive')

        @self.command(name="all", pass_context=True)
        async def getAllFood(ctx):
            embed = discord.Embed()
            embed.description = self.dataHolder.getFreeFoods(5)
            await ctx.channel.send(embed=embed)

        @self.command(name="today", pass_context=True)
        async def getFood(ctx):
            embed = discord.Embed()
            embed.description = self.dataHolder.getTodayFreeFood()
            if not embed.description:
                await ctx.channel.send("nothing for today")
            else:
                await ctx.channel.send("TODAY'S FOOD")
                await ctx.channel.send(embed=embed)

        @self.command(name="tomorrow", pass_context=True)
        async def getFood(ctx):
            embed = discord.Embed()
            embed.description = self.dataHolder.getTomorrowFreeFood()
            await ctx.channel.send(embed=embed)

    @tasks.loop(seconds=30)
    async def sendTodayFreeFood(self, ctx):
        if datetime.datetime.now().hour == 9:
            channeltest = ctx.get_channel(890062399904825366)
            if channeltest is not None:
                embed = discord.Embed()
                embed.description = self.dataHolder.getTodayFreeFood()
                if not embed.description:
                    await ctx.channel.send("nothing for today")
                else:
                    await ctx.channel.send("TODAY'S FOOD")
                    await ctx.channel.send(embed=embed)
                await asyncio.sleep(82800)  # 23 hours


def run(dataHolder):
    bot = DiscordBot(command_prefix="!", self_bot=False, dataHolder=dataHolder)
    discord_config = json.load(open('discord_config.json', 'r'))
    TOKEN = discord_config["token"]
    bot.run(TOKEN)
