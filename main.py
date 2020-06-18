import discord
from discord.ext import commands
import json
import random
import os

class choika(commands.Bot):
    def __init__(self):
        self.prefix = "$"
        super().__init__(commands.when_mentioned_or(self.prefix), case_insensitive=True)

        self.remove_command("help")

    async def read_json(self, fn: str):
        with open(fn) as f:
            return json.load(f)

    async def write_json(self, fn: str, data):
        with open(fn, "w") as f:
            json.dump(data, f)

    async def is_owner(self, member):
        app = await self.application_info()
        if app.team:
            return member.id in [x.id for x in app.team.members]
        else:
            return member.id == app.owner.id

    async def on_ready(self):
        self.load_extension("jishaku")
        self.load_extension("cog")
        self.config = await self.read_json("config.json")
        print("imma a choika")

    async def on_message(self, msg):
        await self.process_commands(msg)
        if msg.channel.id not in self.config["licensed"]:
            return
        if msg.author.bot:
            return
        if msg.mentions:
            if (
             msg.content.startswith(msg.mentions[0].mention)
            and msg.mentions[0].bot
            ):return
        for i in self.config["prefixes"]:
            if msg.content.startswith(i):
                return
        if msg.author.id in (await self.read_json('blocklist.json'))["users"]: return

        if random.randint(0, self.config["standart"]) == 0:
            l = await self.read_json("ai.json")
            content = msg.content
            for i in msg.mentions:
                content = content.replace(i.mention,i.name) 
            l.append(content)
            await self.write_json("ai.json", l)
            print("added ", msg.content)
            await msg.add_reaction("➕")

    async def on_message_edit(self,before,msg):
        if not msg.author.guild_permissions.send_messages: return
        await self.process_commands(msg)

    def restart(self):
        os.system('python 3.8 main.py')
        exit

bot = choika()
bot.run(
    "NzA3NzUyNjAyMDQ5MTgzNzY2.Xuj9tw.mWPXih34l-HH8q8l4ZRqcHbG9ug",
    bot=True,
    reconnect=True,
)
