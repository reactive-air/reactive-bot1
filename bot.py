import discord
from discord.ext import commands
import random
from datetime import datetime, timedelta

TOKEN = "MTI3Mzk5NTczMjk4MjAzODU5OQ.G3xXfD.62LksTHFKnhUdyaaTSVTAtfj7jzftzkTpq0SJg"

USER_ID = 1128440474324172851  # You have infinite coins

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="reactive ", intents=intents)

balances = {}
daily_claims = {}

# Store items and user purchases
STORE_ITEMS = {
    "gus_drink": 2000,
    "vip_tag": 10000,
    "dark_aura": 30000,
    "luck_charm": 15000
}

purchases = {}

# Action GIFs
GIFS = {
    "hug": [
        "https://tenor.com/view/fire-country-hug-bro-hug-big-hugs-bode-leone-gif-3147301375950955437",
        "https://tenor.com/view/arthur-morgan-john-marston-gives-hat-gif-8837389336110965719",
        "https://tenor.com/view/ragnar-hug-vikings-manito-comforting-gif-11548739"
    ],
    "slap": [
        "https://tenor.com/view/shut-up-stfu-shut-your-mouth-slap-slapping-gif-8050553153066707611",
        "https://tenor.com/view/slap-slapping-slap-meme-slap-gif-slap-head-gif-14757072629767529364",
        "https://tenor.com/view/tf-3-smack-slap-face-slap-gif-1292010994896831756"
    ],
    "punch": [
        "https://tenor.com/view/punch-beat-up-pogger-gif-22865694",
        "https://tenor.com/view/rick-grimes-rick-punch-angry-gif-16878041",
        "https://tenor.com/view/arthur-morgan-lenny-summers-red-dead-redemption2-rdr2-rdr-gif-27378482"
    ],
    "salute": [
        "https://tenor.com/view/top-gun-top-gun-maverick-salute-tom-cruise-military-gif-26899454",
        "https://tenor.com/view/salute-yes-sir-soldier-respect-gif-15342227",
        "https://tenor.com/view/snake-salute-mgs3-gif-9277925",
        "https://tenor.com/view/caption-gif-23142074"  # Captain America Salute
    ],
    "smoke": [
        "https://tenor.com/view/brad-pitt-smoking-gif-5093845",
        "https://tenor.com/view/tyler-durden-gif-23897944",
        "https://tenor.com/view/tyler-durden-gif-5087139481756677869",
        "https://tenor.com/view/winston-churchill-gif-16729802791973356731",
        "https://tenor.com/view/the-sopranos-gif-22710838",
        "https://tenor.com/view/scarface-tony-montana-al-pacino-tony-montana-cigar-cigar-gif-5413278",
        "https://tenor.com/view/cigar-smoking-smoke-back-off-gif-17958464",
        "https://tenor.com/view/tony-soprano-smoking-a-cigar-tony-soprano-cigar-tony-soprano-cigar-gif-7705468042119447259",
        "https://tenor.com/view/joaquin-phoenix-joker-movie-joker-actor-famous-gif-15224220",
        "https://tenor.com/view/arthur-morgan-rdr2-smoking-cigarette-red-dead-redemption-gif-25082107",
        "https://tenor.com/view/arthur-morgan-smoking-rdr-2-swayer-gif-4927315448300151004",
        "https://tenor.com/view/play-station-dunyasi-arthur-morgan-sad-smoking-gif-22050126"
    ],
    "kill": [
        "https://tenor.com/view/mortal-kombat-homelander-omni-man-train-mk1-gif-18158926861667691769",
        "https://tenor.com/view/stab-knife-kifluggs-kill-murder-gif-24765587",
        "https://tenor.com/view/anakin-rots-gif-26028889",
        "https://tenor.com/view/avada-kadavra-star-wars-voldemort-spell-gif-16160198",
        "https://tenor.com/view/captain-america-punching-gif-14305216",
        "https://tenor.com/view/firing-weapon-din-djarin-the-mandalorian-shooting-weapon-firing-gun-gif-26760653",
        "https://tenor.com/view/star-wars-darth-vader-rogue-one-gif-25857060",
        "https://tenor.com/view/anakin-skywalker-choking-padme-amidala-gif-25456989",
        "https://tenor.com/view/bh187-justice-league-dc-superman-pissed-gif-20842940",
        "https://tenor.com/view/pewenzoo-gif-4550924347340756464",
        "https://tenor.com/view/batman-the-batman-beat-up-gif-23744969",
        "https://tenor.com/view/scary-hallway-batman-gif-7533698791581967967",
        "https://tenor.com/view/batman-gif-20459900",
        "https://tenor.com/view/batman-face-punch-bitch-slap-gif-13233664",
        "https://tenor.com/view/mortal-kombat-scorpion-gif-19916760",
        "https://tenor.com/view/mortal-kombat-mortal-kombat11-scorpion-fatality-netherrealm-studios-gif-13360868",
        "https://tenor.com/view/jax-blow-mk11-fatal-mortal-kombat-gif-17309266",
        "https://tenor.com/view/mortal-kombat-scorpion-gif-10389733",
        "https://tenor.com/view/homelander-the-boys-black-noir-homelander-kill-homelander-and-black-noir-gif-26428738",
        "https://tenor.com/view/dexter10-dexter-dexter-gi-fs-gif-6073052",
        "https://tenor.com/view/dexter-dexter-morgan-michael-c-hall-gif-16585241",
        "https://tenor.com/view/dexter-getting-ready-ready-to-kill-gif-3386755",
        "https://tenor.com/view/dexter-dexter-morgan-gif-17846891680191209609",
    ],
    "bruh": [
        "https://tenor.com/view/star-wars-dark-side-anakin-skywalker-darth-vader-revenge-of-the-sith-gif-25702979",
        "https://tenor.com/view/statue-sigma-guy-gif-7022164970276473532",
        "https://tenor.com/view/bruh-stare-looking-what-confuse-gif-17309681"
    ],
    "dexter": [
        "https://tenor.com/view/dexter-dance-dexter-morgan-dance-funny-dancing-gif-2933392233895180957",
        "https://tenor.com/view/dexter-dexter-morgan-micheal-c-hall-rita-rita-dexter-gif-17495988031212328128",
        "https://tenor.com/view/dexter-dexter-morgan-michael-c-hall-smile-gif-4431777"
    ],
    "dance": [
        "https://tenor.com/view/roblox-roblox-dance-roblox-emote-roblox-meme-roblox-face-gif-6922671201272284519",
        "https://tenor.com/view/шрек-gif-9529056951424479894",
        "https://tenor.com/view/cat-dance-animated-troll-trolled-gif-27617235",
        "https://tenor.com/view/sonic-fortnite-dance-dancing-sonic-the-hedgehog-gif-16311316"
        "https://tenor.com/view/rdr2-red-dead-redemption-2-dutch-dancing-red-dead-gif-9051765508016161872"
    ]
}
GIFS["moser"] = [
    "https://tenor.com/view/qzx-gif-4928371737620023086",
    "https://tenor.com/view/brian-moser-gif-5300612879759544061",
    "https://tenor.com/view/brian-moser-stalker-dexter-morgan-gif-14346807064989972511"
]
GIFS["burn"] = [
    "https://tenor.com/view/ghost-rider-gif-6197644357565647298",
    "https://tenor.com/view/torch-flame-gif-9093171",
    "https://tenor.com/view/rdr2-red-dead-redemption2-fire-flame-burning-gif-16737402",
    "https://tenor.com/view/red-dead-redemption-red-dead-redemption-2-rdr-john-marston-gif-2579497764844224153",
    "https://tenor.com/view/hanzo-genji-battle-brothers-ultimate-gif-13381737",
    "https://tenor.com/view/liu-kang-fire-mortal-kombat-fatality-gif-14057005",
    "https://tenor.com/view/doom-eternal-fire-scary-gif-12317762",
    "https://tenor.com/view/iron-man-mnk009-flame-ironman1-gif-20297436",
    "https://tenor.com/view/aran-tal-hunters-star-wars-hunters-star-wars-fire-gif-11457920401220105604",
    "https://tenor.com/view/tf2-pyro-teamfortress2-teamfortress2pyro-fire-gif-13656490",
    "https://tenor.com/view/flame-thrower-leonardo-dicaprio-lance-flamme-burn-burning-gif-21661296",
    "https://tenor.com/view/darth-vader-fire-obi-wan-kenobi-star-wars-red-gif-25841890",
    "https://tenor.com/view/burning-on-fire-lit-fire-scorpion-gif-14362531",
    "https://tenor.com/view/scorpionmk11-scorpion-scorpionwin-scorpionwinpose-scorpionvictorypose-gif-21133040",
    "https://tenor.com/view/mortal-kombat-mortal-kombat11-scorpion-hanzo-hasashi-gif-20646972",
    "https://tenor.com/view/scorpion-mortal-kombat13-fireball-heart-fatality-gif-5416991"
]
love_gifs = [
    "https://tenor.com/view/ghost-of-tsushima-ghost-tsushima-sucker-punch-productions-sucker-punch-gif-17231683",
    "https://tenor.com/view/ghost-of-tsushima-ghost-ready-to-fight-gif-22070870",
    "https://tenor.com/view/samurai-jin-sakai-ghost-of-tsushima-leaves-katana-gif-12350263285995295369",
    "https://tenor.com/view/fire-entrance-gif-11171869",
    "https://tenor.com/view/knight-gif-2106030393162683006",
    "https://tenor.com/view/got-jon-snow-ready-battle-army-gif-7195721"
]

# Gambling result GIFs
WIN_GIF = "https://media.tenor.com/XYdzM5I1CcgAAAAC/anakin-skywalker-star-wars.gif"
LOSE_GIF = "https://media.tenor.com/HWvnCt6kFmwAAAAC/anakin-panakin.gif"

def get_balance(user_id):
    if user_id == USER_ID:
        return 999999999999  # infinite coins for you
    return balances.get(user_id, 0)

def update_balance(user_id, amount):
    if user_id == USER_ID:
        return  # your balance doesn't change
    balances[user_id] = get_balance(user_id) + amount

def format_coin(number):
    return f"{number:,}"

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}!")

@bot.command()
async def balance(ctx, member: discord.Member = None):
    member = member or ctx.author
    bal = get_balance(member.id)
    await ctx.send(f"💰 {member.display_name}'s balance: {format_coin(bal)} coins.")

@bot.command()
async def addmoney(ctx, amount: int):
    if ctx.author.id != USER_ID:
        return await ctx.send("❌ You can't use this command.")
    if amount <= 0:
        return await ctx.send("❌ Amount must be positive.")
    update_balance(ctx.author.id, amount)
    bal = get_balance(ctx.author.id)
    await ctx.send(f"✅ Added {format_coin(amount)} coins. New balance: {format_coin(bal)} coins.")

@bot.command()
async def give(ctx, member: discord.Member, amount: int):
    giver_id = ctx.author.id
    if amount <= 0:
        return await ctx.send("❌ Amount must be positive.")
    if giver_id != USER_ID and amount > get_balance(giver_id):
        return await ctx.send("❌ You don't have enough coins.")
    if member.bot:
        return await ctx.send("❌ You can't give coins to bots.")
    if giver_id != USER_ID:
        update_balance(giver_id, -amount)
    update_balance(member.id, amount)
    await ctx.send(f"💸 {ctx.author.mention} gave {format_coin(amount)} coins to {member.mention}.")

@bot.command()
async def daily(ctx):
    user_id = ctx.author.id
    now = datetime.utcnow()
    last_claim = daily_claims.get(user_id)
    if last_claim and now - last_claim < timedelta(hours=24):
        remaining = timedelta(hours=24) - (now - last_claim)
        hrs, rem = divmod(remaining.seconds, 3600)
        mins, secs = divmod(rem, 60)
        return await ctx.send(f"⏳ You already claimed your daily coins. Try again in {hrs}h {mins}m.")
    reward = random.randint(500, 1000)
    update_balance(user_id, reward)
    daily_claims[user_id] = now
    await ctx.send(f"📅 {ctx.author.mention}, you claimed your daily **{format_coin(reward)}** coins!")

@bot.command()
async def slots(ctx, amount: int):
    user_id = ctx.author.id
    if amount <= 0:
        return await ctx.send("❌ Amount must be positive.")
    if user_id != USER_ID and amount > get_balance(user_id):
        return await ctx.send("❌ You don't have enough coins to gamble that amount.")

    emojis = ["🍒", "🍋", "🍊", "🍉", "⭐", "7️⃣"]
    result = [random.choice(emojis) for _ in range(3)]

    win = 0
    if result[0] == result[1] == result[2]:
        win = amount * 3
    elif (result[0] == result[1] and result[0] != result[2]) or \
        (result[1] == result[2] and result[1] != result[0]) or \
        (result[0] == result[2] and result[0] != result[1]):
        win = amount * 2

    if user_id != USER_ID:
        update_balance(user_id, -amount)
        update_balance(user_id, win)

    embed = discord.Embed(title="🎰 Slots 🎰", description=" | ".join(result), color=0x00ff00)
    if win > 0:
        embed.add_field(name="🎉 You won!", value=f"💰 {format_coin(win)} coins!", inline=False)
        embed.set_image(url=WIN_GIF)
    else:
        embed.add_field(name="💸 You lost!", value=f"You lost {format_coin(amount)} coins.", inline=False)
        embed.set_image(url=LOSE_GIF)

    await ctx.send(embed=embed)

@bot.command()
async def coinflip(ctx, amount: int, choice: str):
    user_id = ctx.author.id
    choice = choice.lower()
    if choice not in ["heads", "tails"]:
        return await ctx.send("❌ Please choose 'heads' or 'tails'.")
    if amount <= 0:
        return await ctx.send("❌ Amount must be positive.")
    if user_id != USER_ID and amount > get_balance(user_id):
        return await ctx.send("❌ You don't have enough coins to gamble that amount.")

    flip = random.choice(["heads", "tails"])
    win = 0
    if choice == flip:
        win = amount * 2
        if user_id != USER_ID:
            update_balance(user_id, win)
        result_msg = f"🎉 You won! The coin landed on {flip}."
        gif_url = WIN_GIF
    else:
        if user_id != USER_ID:
            update_balance(user_id, -amount)
        result_msg = f"😞 You lost! The coin landed on {flip}."
        gif_url = LOSE_GIF

    embed = discord.Embed(title="🪙 Coinflip 🪙", description=result_msg, color=0x00ff00 if win > 0 else 0xff0000)
    embed.set_image(url=gif_url)
    await ctx.send(embed=embed)

# Helper to send random action gif
async def send_action_gif(ctx, action, target: discord.Member):
    if not target:
        return await ctx.send("❌ You must mention a user for this command.")
    gif = random.choice(GIFS[action])
    await ctx.send(f"{ctx.author.mention} {action}s {target.mention}!\n{gif}")

# Action commands
@bot.command()
async def hug(ctx, member: discord.Member = None):
    await send_action_gif(ctx, "hug", member or ctx.author)

@bot.command()
async def slap(ctx, member: discord.Member = None):
    await send_action_gif(ctx, "slap", member or ctx.author)

@bot.command()
async def punch(ctx, member: discord.Member = None):
    await send_action_gif(ctx, "punch", member or ctx.author)

@bot.command()
async def salute(ctx, member: discord.Member = None):
    await send_action_gif(ctx, "salute", member or ctx.author)

@bot.command()
async def smoke(ctx, member: discord.Member = None):
    await send_action_gif(ctx, "smoke", member or ctx.author)

@bot.command()
async def kill(ctx, member: discord.Member = None):
    await send_action_gif(ctx, "kill", member or ctx.author)

@bot.command()
async def bruh(ctx, member: discord.Member = None):
    await send_action_gif(ctx, "bruh", member or ctx.author)

@bot.command()
async def dexter(ctx):
    gif = random.choice(GIFS["dexter"])
    await ctx.send(f"{gif}")

@bot.command(name="iwin")
async def iwin(ctx):
    await ctx.send("https://tenor.com/view/anakin-skywalker-smiling-obi-wan-kenobi-hayden-christensen-smile-gif-25967887")

@bot.command(name="ilose")
async def ilose(ctx):
    await ctx.send("https://tenor.com/view/anakin-skywalker-crying-because-he-doesnt-want-to-lose-padme-gif-1361251639282343324")

@bot.command()
async def dance(ctx):
    gif = random.choice(GIFS["dance"])
    await ctx.send(f"{ctx.author.mention} is dancing! 💃\n{gif}")

@bot.command()
async def store(ctx):
    embed = discord.Embed(title="🛒 REACTIVE STORE", color=0xFFD700)
    for item, price in STORE_ITEMS.items():
        embed.add_field(name=item.replace("_", " ").title(), value=f"{format_coin(price)} coins", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def buy(ctx, item_name: str):
    user_id = ctx.author.id
    item_name = item_name.lower()

    if item_name not in STORE_ITEMS:
        return await ctx.send("❌ Item not found in the store.")

    price = STORE_ITEMS[item_name]
    if user_id != USER_ID and get_balance(user_id) < price:
        return await ctx.send("❌ You don’t have enough coins.")

    if user_id != USER_ID:
        update_balance(user_id, -price)

    purchases.setdefault(user_id, []).append(item_name)

    if item_name == "gus_drink":
        await ctx.send("🥤 You drank Gus's drink...")
        await gus_drink_effect(ctx)

    elif item_name == "vip_tag":
        role_name = "Special Role"  # اسم الرتبة التي تريدها
        guild = ctx.guild
        role = discord.utils.get(guild.roles, name=role_name)

        if not role:
            # إنشاء الرتبة لو مش موجودة
            role = await guild.create_role(
                name=role_name,
                colour=discord.Colour.gold(),
                reason="Created for VIP Tag purchase"
            )

        # إعطاء الرتبة للمستخدم
        await ctx.author.add_roles(role)
        await ctx.send(f"🎉 Congrats {ctx.author.mention}, you got the **{role_name}** role!")

    elif item_name == "dark_aura":
        await ctx.send(f"🌑 You bought the **Dark Aura**! Something mysterious surrounds you...")

    elif item_name == "luck_charm":
        await ctx.send(f"🍀 You bought the **Luck Charm**! Your luck just improved!")

    else:
        await ctx.send(f"✅ You bought **{item_name.replace('_', ' ').title()}**!")

async def gus_drink_effect(ctx):
    # Example effect: add random coins as bonus
    bonus = random.randint(1000, 5000)
    user_id = ctx.author.id
    if user_id != USER_ID:
        update_balance(user_id, bonus)
    await ctx.send(f"🎉 You got a bonus of {format_coin(bonus)} coins from Gus's drink!")

@bot.command()
async def who_are_you(ctx):
    video_url = "https://cdn.discordapp.com/attachments/1388538199994798110/1389735613657256006/9258af710e645623415266055766cd9f.mp4"

    await ctx.send(f"🎥 Here's who I am...\n{video_url}")

    await ctx.send("🕶️ **You think you know me...**\nBut I'm the shadow you fear, the silence you ignore...\nI am the glitch in your reality — *reactive.*")

@bot.command(name="who_is_the_best_jedi")
async def who_is_the_best_jedi(ctx):
    video_url = "https://cdn.discordapp.com/attachments/1388538199994798110/1391062766252724365/40410e5d2de6deccfe2096977babfcd62.mp4"

    await ctx.send(f"💫 Who's the best Jedi?\n{video_url}")

    await ctx.send("🧠 **No council... no rulebook... only instinct and the Force.**\nReactive stands where legends fall.")

@bot.command(name="who_is_your_family")
async def who_is_your_family(ctx):
    video_url = "https://cdn.discordapp.com/attachments/1388538199994798110/1391062767187923087/2d480d3a9dc9bf2ee9fee1cf5d56ffec2.mp4"

    await ctx.send(f"🩸 Who is your family?\n{video_url}")

    await ctx.send("👁‍🗨 **I don’t have a family... I have a bloodline.**\nThey don’t walk beside me... they haunt behind me.")

@bot.command(name="why_did_you_go_to_the_dark_side")
async def why_did_you_go_to_the_dark_side(ctx):
    video_url = "https://cdn.discordapp.com/attachments/1388538199994798110/1391062764830720020/12d2403d88b02a8c65aa0913282a616b.mp4"

    await ctx.send("🌑 Why did you go to the dark side?\n" + video_url)

    await ctx.send("🕯️ **They called me a fallen angel...**\nBut they never asked why I fell.\nI didn’t choose the dark — I was pushed into it.")

from discord.ext import commands
import discord

from discord.ext import commands
import discord

class CustomHelp(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        embed = discord.Embed(
            title="🤖 𝙍𝙀𝘼𝘾𝙏𝙄𝙑𝙀 𝘾𝙊𝙈𝙈𝘼𝙉𝘿𝙎 𝙇𝙄𝙎𝙏",
            color=0xFFD700,
            description=(
                "💰 COINS & GAMBLING**\n"
                "balance, daily, give, addmoney, slots, coinflip\n\n"

                "🛒 STORE SYSTEM**\n"
                "store, buy\n\n"

                "🎭 **REACTION ACTIONS**\n"
                "> hug, slap, punch, salute\n"
                "> smoke, kill, bruh, dance\n"
                "> ouch, **burn** 🔥\n\n"


                "🩸 DEXTER COMMANDS**\n"
                "dexter_wake_up, dexter_who_is_you, dexter_i_know\n"
                "🎥 DEXTER GIFs**\n"
                "dexter → Sends a random Dexter GIF\n\n"

                "🧠 BRIAN MOSER COMMANDS**\n"
                "brian_who_am_i, brian_my_baby_boy, brian\n"
                "moser → Sends a random Brian Moser GIF\n\n"

                "💀 HELLO, YOU (Joe the Killer)\n"
                "joe, joe_maybe, joe_edit, m_not_joe\n\n"

                "🎞 DUTCH SPECIALS**\n"
                "dutch, we_need_money, dutch_what, dutch_tf, put_line_to_this, troll_gng, real_gng\n\n"

                "🌌 ANAKIN SPECIALS**\n"
                "who_are_you, who_is_the_best_jedi, who_is_your_family, why_did_you_go_to_the_dark_side\n\n"

                "🏆 MOOD EXPRESSIONS**\n"
                "iwin, ilose\n\n"

                "🔮 OTHER**\n"
                "help, reactive\n\n"

                "💝 Made with rage, pain & power by REACTIVE AIR —\n"
                "a full currency + reaction bot for the fallen ones 💝"
            )
        )
        await self.get_destination().send(embed=embed)

bot.help_command=CustomHelp()

@bot.command()
async def dutch(ctx):
    await ctx.send("https://tenor.com/view/dutch-van-der-linde-rdr2-gif-22768333")

@bot.command()
async def we_need_money(ctx):
    await ctx.send("https://tenor.com/view/we-need-money-gif-8439223390928650892")

@bot.command()
async def dutch_what(ctx):
    await ctx.send("https://tenor.com/view/dutch-van-der-linde-rdr2-red-dead-redemption-wtf-gif-4632380853254771942")

@bot.command()
async def dutch_tf(ctx):
    await ctx.send("https://tenor.com/view/dutch-dutch-van-der-linde-rdr2-red-dead-redemption-red-dead-redemption-2-gif-15492877128851228773")
    await ctx.send("https://tenor.com/view/dutch-van-der-linde-red-dead-redemption-gif-22961528")

@bot.command()
async def ouch(ctx):
    await ctx.send("https://tenor.com/view/dutch-gif-26490072")

@bot.command()
async def put_line_to_this(ctx):
    await ctx.send("https://tenor.com/view/dutch-van-der-linde-red-dead-redemption-revolver-gif-19290150")

@bot.command()
async def troll_gng(ctx):
    await ctx.send("Dutch Van Der Linde Gang 😈🔥")
    await ctx.send("https://cdn.discordapp.com/attachments/1388553115476819969/1392199363438313674/35db16f4b232f922d13923c6ee3ac14b.mp4")

@bot.command()
async def real_gng(ctx):
    await ctx.send("Dutch's Real Gang 💀💰")
    await ctx.send("https://cdn.discordapp.com/attachments/1388553115476819969/1392199363069087864/64ade610e09f07cd11c110c1b2607297.mp4")

@bot.command()
async def dexter_wake_up(ctx):
    await ctx.send("https://cdn.discordapp.com/attachments/1394644971902075031/1394828168296136887/2b1bcd0e2e1ede5aa539c7d5eb9e10ae.mp4")

@bot.command()
async def dexter_who_is_you(ctx):
    await ctx.send("https://cdn.discordapp.com/attachments/1394644971902075031/1394827686249234553/49e2b9077fc9d684c783ca3df59d023b.mp4")

@bot.command()
async def dexter_i_know(ctx):
    await ctx.send("https://cdn.discordapp.com/attachments/1394644971902075031/1394828779603624127/21b602db0602f9e50bcd554c62522897.mp4")

@bot.command()
async def brian_who_am_i(ctx):
    await ctx.send("https://cdn.discordapp.com/attachments/1394644971902075031/1394828199589974086/83406c211d66f3fc97a87876b35c471d.mp4")

@bot.command()
async def brian_my_baby_boy(ctx):
    await ctx.send("https://cdn.discordapp.com/attachments/1394644971902075031/1394829921821659277/c3a104cb5a8214fd865e6a2d58f61980.mp4")

@bot.command()
async def brian(ctx):
    await ctx.send("https://cdn.discordapp.com/attachments/1394644971902075031/1394827176410480670/3541edfbf0b91e18699295bb388568a3.mp4")

joe_gifs = [
    "https://tenor.com/view/joe-goldberg-gif-27002005",
    "https://tenor.com/view/joe-goldberg-you-stare-joe-gif-13791327826155408442",
    "https://tenor.com/view/you-show-joe-goldberg-wave-greetings-hi-gif-13222093"
]

@bot.command(name="joe")
async def joe(ctx):
    await ctx.send(random.choice(joe_gifs))

@bot.command(name="joe_maybe")
async def joe_maybe(ctx):
    await ctx.send("https://cdn.discordapp.com/attachments/1394644969855123508/1394857283078455397/ii.ftq_7517422826282945800.mp4")

@bot.command(name="joe_edit")
async def joe_edit(ctx):
    await ctx.send("https://cdn.discordapp.com/attachments/1394644969855123508/1394857766195040336/anikixdd_7495436996874226952.mp4")

@bot.command(name="m_not_joe")
async def m_not_joe(ctx):
    await ctx.send("https://cdn.discordapp.com/attachments/1394644969855123508/1394858180521099276/mainzz_77_7317657842041900320.mp4")

@bot.command()
async def burn(ctx, member: discord.Member = None):
    await send_action_gif(ctx, "burn", member or ctx.author)

@bot.command()
async def what_would_you_do_for_love(ctx):
    gif = random.choice(love_gifs)
    await ctx.send("# **What would you do for love?**\n" + gif)


bot.run(TOKEN)

