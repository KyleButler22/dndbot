import discord
import random
import re
import csv
from discord.ext import commands


#get token
TOKEN = "MTA5MjU0NDQxMTgzOTI1MDQ2Mw.GHZE7w.ezCAxAD-nKc62IJBI6OB99lxcjO51UCoujnWgU"

#AndrewDiceBotClay "MTE4MDU0NzU2NzI2MDU0MTAzMA.Gg4hgf.9AAlU9S4dDjtkkGOTBa7bJTqsukl3fMtl4DZ0g"
#Rollo "MTA5MjU0NDQxMTgzOTI1MDQ2Mw.GHZE7w.ezCAxAD-nKc62IJBI6OB99lxcjO51UCoujnWgU"

#set intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='.', intents=intents)

@bot.event
async def on_ready():
    # when started, verify in terminal that it has connected to discord and list guilds
    print(f'{bot.user} has connected to Discord!')
    for guild in bot.guilds:
        print(f'{bot.user} is in guild {guild}')

@bot.command()
async def honk(ctx):
    # respond "honk honk'
    await ctx.send('honk honk')

@bot.command()
async def r(ctx, *args):
    arg = ''.join(args)
    arg.strip('.r')
    try:
        #get input and strip whitespace
        roll = arg.strip()
        #search for #d to get all dice, strip d and convert to int
        dice = re.findall('\d*d', roll)
        for i in range(len(dice)):
            if dice[i] == 'd':
                dice[i] = 1
            else:
                dice[i] = int(dice[i].strip('d'))
        if not dice:
            raise ValueError
        #repeat for sides looking for d#
        sides = re.findall('d\d*', roll)
        for i in range(len(sides)):
            sides[i] = int(sides[i].strip('d'))
        if not sides:
            raise ValueError
        #remove #d# from string
        roll = re.sub('\d*d\d*', '', roll)
        #extract the mod and operator
        try:
            modandop = re.search('\S\d+', roll)
            modandop = modandop.group()
            operator = modandop[0]
            mod = int(modandop[1:])
        except (ValueError, AttributeError):
            mod = 0
            operator = 0
    #send error message and exit if input invalid
    except ValueError:
            await ctx.send('Invalid Input. Roll must follow input of "(dice)d(sides)[+,-,/,x](modifier). Operator and mod optional')
            exit()

    #create empty results set
    results =[]

    #loop through each set of dice
    for i in range(len(dice)):
        #roll results for each set of dice
        for j in range(dice[i]):
            roll = random.randint(1,sides[i])
            if sides[i] == 20 and roll == 20:
                crit_list = ["Critical Hit!", "Crit!", "Natty Twenzonie"]
                await ctx.send(random.choice(crit_list))
            if sides[i] == 20 and roll == 1:
                fumble_list = ["Fumble!", "Natty 1!", "Oof"]
                await ctx.send(random.choice(fumble_list))
            results.append(roll)

    #include mod if operator and mod are present
    if operator == '+':
        total = sum(results) + mod
    elif operator == '-':
        total = sum(results) - mod
    elif operator == '/':
        total = round(int((sum(results) / mod)))
    elif operator == 'x':
        total = sum(results) * mod
    else:
        total = sum(results)

    #print die results and total
    await ctx.send(results)
    await ctx.send(total)


@bot.command()
async def helpp(ctx):
    #respond with all command options
    await ctx.send('Command Options: \n.honk: HONK HONK \n.r: Roll dice (format "xdx + modifier") \n.newcharacter: Rolls stats for a new Pathfinder character (6 stats, 4d6 drop the lowest) \nconfusion: Roll for confusion effects \nrules: Lookup rules (i.e. ".rules cmb") \ncrit: Generate a crit (format .crit magic/melee/ranged) \nfumble: Generate a fumble (format .fumble magic/melee/ranged)' )

@bot.command()
async def newcharacter(ctx):
    for i in range(6):
        results = []
        for j in range(4):
            roll = random.randint(1,6)
            results.append(roll)
        await ctx.send(results)
        results.remove(min(results))
        total = sum(results)
        await ctx.send(total)

@bot.command()
async def confusion(ctx):
    roll = random.randint(1,100)
    await ctx.send(roll)
    if roll<=25:
        await ctx.send('Act Normally')
    if 26<=roll<=50:
        await ctx.send('Babble Incoherently')
    if 51<=roll<=75:
        await ctx.send('Deal 1d8+Str to self')
    if 76<=roll<=100:
        await ctx.send('Attack nearest creature')

@bot.command()
async def rules(ctx, *args):
    #join all words in the command and force lowercase
    arg =  ''.join(args).strip().lower()
    #open csv and look for match in first column
    with open('rules.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            # if the first row matches the command, send the second column
            if row[0] == arg:
                await ctx.send(row[1])


@bot.command()
async def crit(ctx, arg):
    arg = arg.strip().lower()
    if arg == 'melee':
        roll = random.randint(1,100)
        await ctx.send(roll)
        with open('meleecrit.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            #match roll to row #
            for row in csv_reader:
                if int(row[0]) == roll:
                    #print name and description of crit
                    await ctx.send(row[1])
                    await ctx.send(row[2])
    if arg == 'magic':
        roll = random.randint(1,100)
        await ctx.send(roll)
        with open('magiccrit.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            #match roll to row #
            for row in csv_reader:
                if int(row[0]) == roll:
                    #print name and description of crit
                    await ctx.send(row[1])
                    await ctx.send(row[2])
    if arg == 'ranged':
        roll = random.randint(1,100)
        await ctx.send(roll)
        with open('rangedcrit.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            #match roll to row #
            for row in csv_reader:
                if int(row[0]) == roll:
                    #print name and description of crit
                    await ctx.send(row[1])
                    await ctx.send(row[2])

@bot.command()
async def fumble(ctx, arg):
    arg = arg.strip().lower()
    if arg == 'melee':
        roll = random.randint(1,100)
        await ctx.send(roll)
        with open('meleefumble.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            #match roll to row #
            for row in csv_reader:
                if int(row[0]) == roll:
                    #print name and description of crit
                    await ctx.send(row[1])
                    await ctx.send(row[2])
    if arg == 'magic':
        roll = random.randint(1,100)
        await ctx.send(roll)
        with open('magicfumble.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            #match roll to row #
            for row in csv_reader:
                if int(row[0]) == roll:
                    #print name and description of crit
                    await ctx.send(row[1])
                    await ctx.send(row[2])
    if arg == 'ranged':
        roll = random.randint(1,100)
        await ctx.send(roll)
        with open('rangedfumble.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            #match roll to row #
            for row in csv_reader:
                if int(row[0]) == roll:
                    #print name and description of crit
                    await ctx.send(row[1])
                    await ctx.send(row[2])




bot.run(TOKEN)