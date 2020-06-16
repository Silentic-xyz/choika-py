import discord
from discord.ext import commands
import json 
import random

class choika(commands.Bot):
    def __init__(self):
        self.prefix = 'PREFIX'
        super().__init__(commands.when_mentioned_or(self.prefix), case_insensitive = True)
        



    async def read_json(self, fn: str):
        with open(fn) as f:
            return json.load(f)
            



    async def write_json(self, fn: str, data):
        with open(fn, 'w') as f:
            json.dump(data, f)


    async def is_owner(self,member):
        app = await self.application_info()
        if app.team:
            return member.id in [x.id for x in app.team.members]
        else:
            return member.id == app.owner.id


    async def on_ready(self):
        self.load_extension('jishaku')
        self.load_extension('cog')
        print('imma a choika')


    async def on_message(self, msg):
        await self.process_commands(msg)
        if msg.author.bot:return
        prefixes=['!','dev$','ext$','stable$','user$',self.prefix,'sct$','..','n.','r.','r/','s?',
            'z/','+','?','>','d.','f.','j.','nd.','s.','u!','x!','a>',';','.','-',',','cj.','gg!', 'sc$', 'snake$']
        for i in prefixes:
            if msg.content.startswith(i): return
        if random.randint(0,20) == 0:
            l = await self.read_json('ai.json')
            l.append(msg.content)
            await self.write_json('ai.json',l)
            print('added ', msg.content)



bot = choika()
bot.run('TOKEN', bot=True, reconnect=True)
