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
            description=await self.bot.get_phrase(msg)
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

    @commands.command()
    async def add(self, ctx, *, phrase):
        cost = len(phrase)*2
        credit = await self.bot.read_json('credits.json')
        try: creditUser = credit[str(ctx.author.id)]
        except KeyError: credit[str(ctx.author.id)] = 0; creditUser = credit[str(ctx.author.id)]
        if creditUser - cost < 0:
            await ctx.send(f'> <:emblemerror:723113966678835242> У вас недостаточно средств на счету\n> Для оплаты требуется {cost} монет, вам нехватает {abs(creditUser-cost)} монет')
            return
        credit[str(ctx.author.id)] = creditUser - cost
        l = await self.bot.read_json("ai.json")
        l.append(phrase)
        await self.bot.write_json('credits.json', credit)
        await self.bot.write_json("ai.json", l)
        stats = await self.bot.read_json('stats.json')
        stats["used"] += cost
        await ctx.message.add_reaction('<:checkmark:723113966246690817>')


    @commands.command(aliases=['addCredits','addC'])
    @commands.is_owner()
    async def addCoins(self,ctx,user: discord.User, howmany:int):
        l = await self.bot.read_json("credits.json") 
        try: l[str(user.id)]
        except KeyError: l[str(user.id)] = 0
        l[str(user.id)] += howmany
        await self.bot.write_json("credits.json", l)
        stats = await self.bot.read_json('stats.json')
        stats["added"] += howmany
        await self.bot.write_json('stats.json',stats)
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


    @commands.command(aliases=['balanceF','balanceS'])
    async def balance(self,ctx):
        s = await self.bot.read_json('credits.json')
        try: s[str(ctx.author.id)]
        except KeyError: s[str(ctx.author.id)] = 0
        await ctx.send(f'> Choika Coins: {s[str(ctx.author.id)]}')
def setup(bot):
    bot.add_cog(Cog(bot))
