import discord
from discord.ext import commands, tasks
import keep_alive
import os, json
from discord import utils
import datetime, asyncio

prefix="b."
my_secret = os.environ['token']
owner_id=904682505104396329
bot=discord.Client()
intents=discord.Intents.all()
client=commands.Bot(command_prefix=prefix, help_command=None, pass_context=True, intents=intents)

async def getemote(arg, guild):
    emoji=utils.get(guild.emojis, name=arg.strip(":"))
    
    if emoji is not None:
        if emoji.animated:
            add = "a"
        else:
            add = ""
        return f"<{add}:{emoji.name}:{emoji.id}>"
    else:
        return None
        
async def getinstr(content):
        ret = []

        spc = content.split(" ")
        cnt = content.split(":")

        if len(cnt) > 1:
            for item in spc:
                if item.count(":") > 1:
                    wr = ""
                    if item.startswith("<") and item.endswith(">"):
                        ret.append(item)
                    else:
                        cnt = 0
                        for i in item:
                            if cnt == 2:
                                aaa = wr.replace(" ", "")
                                ret.append(aaa)
                                wr = ""
                                cnt = 0

                            if i != ":":
                                wr += i
                            else:
                                if wr == "" or cnt == 1:
                                    wr += " : "
                                    cnt += 1
                                else:
                                    aaa = wr.replace(" ", "")
                                    ret.append(aaa)
                                    wr = ":"
                                    cnt = 1

                        aaa = wr.replace(" ", "")
                        ret.append(aaa)
                else:
                    ret.append(item)
        else:
            return content

        return ret

    
def permcheck(guild):
    if not guild.me.guild_permissions.send_messages:
        return('Err')
    if not guild.me.guild_permissions.manage_messages:
        return('Err')
    if not guild.me.guild_permissions.embed_links:
        return('Err')
    if not guild.me.guild_permissions.attach_files:
        return('Err')
    if not guild.me.guild_permissions.external_emojis:
        return('Err')
    if not guild.me.guild_permissions.read_messages:
        return('Err')
    if not guild.me.guild_permissions.manage_webhooks:
        return('Err')
    else:
        return('Ok')
    
    

@tasks.loop(minutes=10)
async def status():
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f'{prefix}help in {len(client.guilds)} servers'))

@client.event
async def on_ready():
    keep_alive.keep_alive()
    await asyncio.sleep(1)
    if os.name=="nt":
        os.system('cls')
    else:
        os.system('clear')
    print(f"Connected to {client.user}")
    print(f"Guilds: {len(client.guilds)}")
    if os.path.isfile('guildconfig.json'):
        with open('guildconfig.json', 'r') as e:
            gc=json.load(e)
        os.remove('guildconfig.json')
    else:
        gc={}
    for i in client.guilds:
        if not i.id in gc.keys():
            gc[str(i.id)]=True
    with open('guildconfig.json', 'w+') as e:
        json.dump(gc, e)    
    status.start()

@client.command()
async def nitro(ctx):
    if not ctx.author.id==owner_id or not ctx.author.guild_permissions.administrator:
        return await ctx.reply('You need `Administrator` permissions to change this')
    with open('guildconfig.json') as e:
        gc=json.load(e)
    os.remove('guildconfig.json')
    if gc[str(ctx.guild.id)]:
        gc[str(ctx.guild.id)]=False
        await ctx.reply('Nitro mode turned off')
    else:
        gc[str(ctx.guild.id)]=True
        await ctx.reply('Nitro mode turned on')
    with open('guildconfig.json', 'w+') as e:
        json.dump(gc, e)

@client.command()
async def help(ctx):
  try:
    embed=discord.Embed(title="Embed Bot", color=discord.Colour.random())
    embed.add_field(name="\uD83E\uDDCA `"+prefix+"help`", value="Shows all commands' info", inline=False)
    img = ctx.message.author.avatar_url
    embed.set_thumbnail(url=img)
    embed.add_field(name="\uD83E\uDDCA `"+prefix+"embed <message>`", value="Sends embeded message\n*`(Requires 'Manage Messages' Permissions)`*", inline=False)
    embed.add_field(name="\uD83E\uDDCA `"+prefix+"nitro`", value="Turn nitro mode on or off for messages `(Always on for embeds)`", inline=False)
    embed.add_field(name="\uD83E\uDDCA `"+prefix+"about`", value="Shows info about the bot", inline=False)
    embed.add_field(name="\uD83E\uDDCA `"+prefix+"invite`", value="Invite the bot to your server", inline=False)
    embed.timestamp =datetime.datetime.utcnow()
    embed.set_footer(text="Requested by '{}'".format(ctx.author))
    await ctx.reply(embed=embed)
  except Exception:
    try:
      ctx.reply("I don't have enough permissions to work properly")
    except Exception:
          try:
              await ctx.author.send(f"I don't have enough permissions in that server")
          except Exception:
                pass

@client.command()
async def about(ctx):
  owner=utils.get(ctx.guild.members, id=owner_id)
  try:
    if not owner is None:
        embed = discord.Embed(title="About", description=f"I am Embed Bot. I am made by {owner.mention}", colour = discord.Colour.random())
    else:
        embed = discord.Embed(title="About", description="I am Embed Bot. I am made by **Βlank#8286**", colour = discord.Colour.random())
    await ctx.reply(embed=embed)
  except Exception:
    try:
      await ctx.reply("I don't have enough permissions to work properly")
    except Exception:
      try:
          await ctx.author.send(f"I don't have enough permissions in that server")
      except Exception:
          pass
                               
@client.command()
async def embed(ctx, *, text=None):                    
    if ctx.author.guild_permissions.manage_messages == True or ctx.author.id==owner_id:
        if text is None:
            return await ctx.reply(f'Syntax:```\n{prefix}embed <your text>```')
        text=text.strip()
        if ":" in text:
            msg=await getinstr(text)
            ret = ""
            em = False
            smth = text.split(':')
            if len(smth) > 1:
                for word in msg:
                    if word.startswith(":") and word.endswith(":") and len(word) > 1:
                        emoji = await getemote(word, ctx.guild)
                        if emoji is not None:
                            em = True
                            ret += f" {emoji}"
                        else:
                            ret += f" {word}"
                    else:
                        ret += f" {word}"

            else:
                ret += msg
            if em:
                text=ret
        try:
          await ctx.message.delete()
          webhook = await ctx.channel.webhooks()
          webhook = utils.get(webhook, name = "Embed Bot")
          if webhook is None:
              webhook = await ctx.channel.create_webhook(name = "Embed Bot")
          embed = discord.Embed(description=text, colour= discord.Colour.random())
          await webhook.send(username=ctx.author.display_name, avatar_url=ctx.author.avatar_url, embed=embed)
        except Exception:
          try:
            await ctx.reply("I don't have enough permissions to work properly")
          except Exception:
            try:
                await ctx.author.send(f"I don't have enough permissions in that server")
            except Exception:
                pass
    else:
        try:
          await ctx.reply("You cannot use me since you don't have the required permissions. Tehehe!")
        except Exception:
          try:
              await ctx.author.send(f"I don't have enough permissions in that server")
          except Exception:
                pass
@client.event
async def on_message(message):
    if not isinstance(message.channel, discord.TextChannel):
        return
    if message.author.bot:
        return
    if message.content==f"<@!{client.user.id}>" or message.content==f"<@{client.user.id}>":
      try:
        em=discord.Embed(title=f"My prefix is `{prefix}`", colour=discord.Colour.random())
        return await message.reply(embed=em)
      except Exception:
        try:
              await message.author.send(f"I don't have enough permissions in that server")
        except Exception:
              pass
    with open('guildconfig.json') as e:
        gc=json.load(e)
    if gc[str(message.guild.id)]:
      if not message.content.startswith(f'{prefix}embed ') and not message.content.startswith(f'{prefix}about ') and not message.content.startswith(f'{prefix}invite ') and not message.content.startswith(f'{prefix}nitro ') and not message.content.startswith(f'{prefix}help '):
        if ":" in message.content:
            msg=await getinstr(message.content)
            ret = ""
            em = False
            smth = message.content.split(':')
            if len(smth) > 1:
                for word in msg:
                    if word.startswith(":") and word.endswith(":") and len(word) > 1:
                        emoji = await getemote(word, message.guild)
                        if emoji is not None:
                            em = True
                            ret += f" {emoji}"
                        else:
                            ret += f" {word}"
                    else:
                        ret += f" {word}"

            else:
                ret += msg
            if em:
                messagen=ret
                try:
                    await message.delete()
                except Exception:
                    pass
                webhook = await message.channel.webhooks()
                webhook = utils.get(webhook, name = "Embed Bot")
                if webhook is None:
                    webhook = await message.channel.create_webhook(name = "Embed Bot")
                if not message.author.guild_permissions.mention_everyone:
                    perms=discord.AllowedMentions(everyone=False, roles=False)
                else:
                    perms=discord.AllowedMentions(everyone=True, roles=False)
                await webhook.send(username=message.author.display_name, avatar_url=message.author.avatar_url, content=messagen, allowed_mentions=perms)
                return

    await client.process_commands(message)

@client.event
async def on_message_edit(before, after):
    if before!=after:
        await client.process_commands(after)
            
@client.command()
async def invite(ctx):
  try:
    em=discord.Embed(title="Do you want me in your server?", description=f"Click [here](https://discord.com/api/oauth2/authorize?client_id={client.user.id}&permissions=604040192&scope=bot) to invite me to your server", colour=discord.Colour.random())
    await ctx.reply(embed=em)
  except Exception:
    try:
      await ctx.reply("I don't have enough permissions to work properly")
    except Exception:
          try:
              await ctx.author.send(f"I don't have enough permissions in that server")
          except Exception:
                pass

@client.event
async def on_guild_join(guild):
    if permcheck(guild)=="Err":
        await guild.leave()
        return
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f'{prefix}help in {len(client.guilds)} servers'))
    await guild.me.edit(nick=guild.me.display_name+f" ({prefix})")
    with open('guildconfig.json') as e:
        gc=json.load(e)
    os.remove('guildconfig.json')
    gc[str(guild.id)]=True
    with open('guildconfig.json', 'w+') as e:
        json.dump(gc, e)
        
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        pass
        
@client.event
async def on_guild_remove(guild):
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f'{prefix}help in {len(client.guilds)} servers'))
    
client.run(my_secret)
