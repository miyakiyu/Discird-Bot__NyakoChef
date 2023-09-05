import discord
import json
import random
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix = "!", intents = intents)

#打開
def load():
    try:
        with open("wishlists.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

#關掉
def save():
    with open("wishlists.json", "w") as file:
        json.dump(wishlists, file,ensure_ascii=False)

#偵測關鍵字
def contains_keyword(message, keyword):
    return keyword in message.content.lower()

#BOT 啟動!
@bot.event
async def on_ready():
    print(f"目前登入身份 --> {bot.user}")
    global wishlists
    wishlists = load()

#Embed
@bot.command()
async def use(ctx):
    embed = discord.Embed(
        title="Command Help Book",
        description="各指令快速指南！",
        color=0x00FFFF
    )
    embed.add_field(name="!roll + 區域", value="在指定區域隨機選擇今天的餐點！", inline=False)
    embed.add_field(name="!add + 餐廳名 + 區域", value="增加新餐廳/餐點至該區域裡")
    embed.add_field(name="!delete + 餐廳名 + 區域", value="從指定區域刪除餐廳/餐點")
    embed.add_field(name="!show", value="瀏覽目前所有登錄的餐廳/餐點")
    await ctx.send(embed=embed)

#添加
@bot.command()
async def add(ctx, item, loc):
    user = str(ctx.author.id)

    if user not in wishlists:
        wishlists[user] = {}
    if loc not in wishlists[user]:
        wishlists[user][loc] = []

    wishlists[user][loc].append(item)
    save()
    await ctx.send(f"新增 '{item}' 到 '{loc}'! (｢･ω･)｢")

#刪除清單內容
@bot.command()
async def delete(ctx,item, loc):
    user = str(ctx.author.id)

    if user in wishlists and loc in wishlists[user] and item in wishlists[user][loc]:
        wishlists[user][loc].remove(item)
        save()
        await ctx.send("刪除成功！")
        await ctx.send(f"Say good bye to '{item}' (･ω･)/")
    else:
        await ctx.send("找不到該餐廳(･x･)?")

#列出清單
@bot.command()
async def show(ctx):
    pic = discord.File('C:\\Users\\s9708\\Desktop\\dc_bot\\pic\\no_item.png')
    user = str(ctx.author.id)

    if user in wishlists:
        embed = discord.Embed(
            title="Resturants Collector",
            color=0x00FF00
        )
        for loc, restaurants in wishlists[user].items():
            if restaurants:
                restaurant_list = "\n".join(restaurants)
                embed.add_field(
                    name=f"Location: {loc}",
                    value=restaurant_list,
                    inline=True
                )
        await ctx.send(embed=embed)
    else:
        await ctx.send(file=pic)

#隨機選擇
@bot.command()
async def roll(ctx, loc):
    pic = discord.File('C:\\Users\\s9708\\Desktop\\dc_bot\\pic\\no_item.png')
    user = str(ctx.author.id)

    if user in wishlists and loc in wishlists[user] and wishlists[user][loc]:
        chosen_item = random.choice(wishlists[user][loc])
        await ctx.send(f"今天吃：{chosen_item}(｢･ω･)｢")
    else:
        await ctx.send(file=pic)

#Keyword
@bot.event
async def on_message(message):
    if not message.author.bot:
        if contains_keyword(message, '安安'):
            await message.channel.send(f'{message.author.mention}, 安安逆好 (b･ω･)b!')
        elif contains_keyword(message, "晚安安"):
            await message.channel.send(f'{message.author.mention},晚安安(」-ω-)」Zzz')
        elif contains_keyword(message, '88'):
            await message.channel.send(f'{message.author.mention}, 88888888 (･ω･)/')
        elif contains_keyword(message, '哭哭'):
            await message.channel.send(f'{message.author.mention}, 不哭不哭眼淚是珍珠 (･ω･)/"')
            
    await bot.process_commands(message)



#以下TOKEN勿動    
bot.run("MTE0NTIyMTA4MjExOTQyMTk1NA.GVl44m.V54vA_amn4cpd6V0HvWBMr25ZFWhsgtCwjD18Y")