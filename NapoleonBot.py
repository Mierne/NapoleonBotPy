# NapoleonBot Dev Version 1.0 REVISED
# Build By: Mierne
# By Mierne

import discord
import random
import asyncio
from discord.ext import commands

NP = commands.Bot(command_prefix="!")
NP.remove_command("help")
# FILTER DOES NOT WORK, SOMETIMES DOES IDFK
#f = open("filters.txt","r")
#filtered_words = f.readlines()

filtered_words = []
@NP.event
async def on_ready():
    print("NapoleonBot Dev 1.0 REVISED online.")

# FUN COMMANDS
@NP.command()
async def pingstat(ctx):
    await ctx.send("Ahoy.")

# HELP COMMANDS
@NP.group(invoke_without_command=True)
async def help(ctx):
    em = discord.Embed(title = "Help", description = "use !help <command> for information regarding that command.",color = ctx.author.color)

    em.add_field(name= "Purge", value = "Deletes messages, 5 uses per 30 seconds.")
    em.add_field(name= "Kick", value = "Kicks the specified user.")
    em.add_field(name= "Ban", value = "Bans the specified user.")

    await ctx.send(embed = em)

@help.command()
async def purge(ctx):
    em = discord.Embed(title = "Purge", description = "Deletes specified amount of messages",color = ctx.author.color)

    em.add_field(name= "**Usage**", value= "!purge 25")
    em.add_field(name= "Cooldown", value= "Command can be used 5 times before cooldown.")

    await ctx.send(embed = em)

@help.command()
async def kick(ctx):
    em = discord.Embed(title = "Kick", description = "Kicks specified user",color = ctx.author.color)

    em.add_field(name= "**Usage**", value= "!kick <user> [reason]")
    em.add_field(name= "Cooldown", value= "Can be used 5 times before cooldown.")

    await ctx.send(embed = em)

@help.command()
async def ban(ctx):
    em = discord.Embed(title = "Ban", description = "Bans specified user",color = ctx.author.color)

    em.add_field(name= "**Usage**", value= "!ban <user> [reason]")
    em.add_field(name= "Cooldown", value= "Can be used 5 times before cooldown.")

    await ctx.send(embed = em)

# MODERATION COMMANDS
@NP.command(aliases=['clr'])
@commands.has_permissions(manage_messages = True)
@commands.cooldown(5,30,commands.BucketType.user)
async def purge(ctx,amount=2):
    await ctx.channel.purge(limit = amount)

@NP.command(aliases=['kck'])
@commands.has_permissions(kick_members = True)
async def kick(ctx,member : discord.Member,*,reason= "no reason given"):
    await member.send("You have been kicked from The Hidden Arms for reason "+reason)
    await member.kick(reason=reason)

@NP.command(aliases=['bn'])
@commands.has_permissions(ban_members = True)
async def ban(ctx,member : discord.Member,*,reason= "no reason given"):
    await ctx.send(member.name + " has been banned for " +reason)
    await member.send("You have been banned from The Hidden Arms for reason "+reason)
    await member.ban(reason=reason)

@NP.event
async def on_message(msg):
    for word in filtered_words:
        if word in msg.content:
            await msg.delete()
            
    await NP.process_commands(msg)
    

# ERROR HANDLING
@pingstat.error
async def pingstat_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('There was an error running the command..')

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('You either mistyped the username, the user is an admin or this user is not in the Server.')

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('You either mistyped the username, the user is an admin or this user is not in the Server.')

@purge.error
async def purge_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = '**You are on cooldown.**, please try again in {:.2f}s'.format(error.retry_after)
        await ctx.send(msg)

# STATUS ROTATIONS
async def st():
    await NP.wait_until_ready()

    statuses = ["Napoleon Total War", "The British"]

    while not NP.is_closed():
        status = random.choice(statuses)

        await NP.change_presence(activity=discord.Game(name=status))

        await asyncio.sleep(120)


    
NP.loop.create_task(st())
# TOKEN
NP.run('')
