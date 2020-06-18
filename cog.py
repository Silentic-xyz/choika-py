import discord
from discord.ext import commands
import random


class Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="$")
    async def ai(self, ctx, *, msg):
        embed = discord.Embed(
            color=discord.Colour.gold(),
            description=random.Random(msg.__hash__()).choice(
                await self.bot.read_json("ai.json")
            ),
        )
        embed.set_footer(
            text=f"Invoced by {ctx.author.name}", icon_url=ctx.author.avatar_url
        )
        await ctx.send(embed=embed)
        if random.randint(0, self.bot.config["minor"]) == 0:
            l = await self.bot.read_json("ai.json")
            l.append(msg)
            await self.bot.write_json("ai.json", l)
            print("added ", msg)
            await ctx.message.add_reaction("➕")

    @commands.command(name="force")
    @commands.is_owner()
    async def force(self, ctx, *, phrase):

        l = await self.bot.read_json("ai.json")
        l.append(phrase)
        await self.bot.write_json("ai.json", l)
        await ctx.message.add_reaction('✅')

    @commands.command(name="remove")
    @commands.is_owner()
    async def remove(self, ctx, *, phrase):

        l = await self.bot.read_json("ai.json")
        try: 
            l.remove(phrase)
            await self.bot.write_json("ai.json", l)
            await ctx.message.add_reaction('✅')
        except:
            await ctx.message.add_reaction('❌')
    @commands.command(name="help")
    async def thelp(self, ctx):
        embed = discord.Embed(
            color=discord.Colour.gold(), description="`help`,`$`,`license`,`invite`"
        )
        embed.set_footer(
            text=f"Invoced by {ctx.author.name}", icon_url=ctx.author.avatar_url
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def license(self, ctx):
        embed = discord.Embed(
            title="Лицензирование каналов",
            description="Вы можете лицензировать свой канал для обучения",
            color=discord.Color.light_grey(),
        )
        embed.add_field(
            name="Требования",
            value="1. Сообщить ID канала;\n2. Записать префиксы всех ботов на сервере\n3. Ограничить доступ ботам к каналу обучения (необезательно)",
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def invite(self, ctx):
        """ Пригласите бота на ваш сервер """

        emb = discord.Embed(
            title="Кастомизируйте права бота",
            description=f"[Приглашение со всеми правами](https://discordapp.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=-1&scope=bot)",
            color=discord.Colour.gold(),
        )
        emb.set_author(
            name=ctx.message.author.name, icon_url=str(ctx.author.avatar_url)
        )
        emb.set_footer(text=f"{ctx.prefix}{ctx.command}")
        emb.add_field(
            name="Пригласите бота без прав",
            value=f"[Бот не создаёт свою личную роль](https://discordapp.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=0&scope=bot)",
            inline=False,
        )
        emb.add_field(
            name="Пригласите бота с правом администратора",
            value=f"[Бот будет иметь права администратора](https://discordapp.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=8&scope=bot)",
            inline=False,
        )
        emb.add_field(
            name="Саппорт сервер",
            value="[Silentic.xyz](https://discord.gg/8hDcNHs), Автор бота: TL",
            inline=False,
        )

        await ctx.send(embed=emb)


def setup(bot):
    bot.add_cog(Cog(bot))
