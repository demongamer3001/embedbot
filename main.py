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
    status.start()

@client.command()
async def help(ctx):
  try:
    embed=discord.Embed(title="Embed Bot", color=discord.Colour.random())
    embed.add_field(name="\uD83E\uDDCA `"+prefix+"help`", value="Shows all commands' info", inline=False)
    img = ctx.message.author.avatar_url
    embed.set_thumbnail(url=img)
    embed.add_field(name="\uD83E\uDDCA `"+prefix+"embed <message>`", value="Sends embeded message\n*`(Requires 'Manage Messages' Permissions)`*", inline=False)
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
              await ctx.author.send(f"I don't have enough permissions in "+ctx.channel.mention)
          except Exception:
                pass

@client.command()
async def about(ctx):
  owner=utils.get(ctx.guild.members, id=owner_id)
  try:
    if not owner is None:
        embed = discord.Embed(title="About", description=f"I am Embed Bot. I am made by {owner.mention}", colour = discord.Colour.random())
    else:
        embed = discord.Embed(title="About", description=f"I am Embed Bot. I am made by **{await client.fetch_user(owner_id)}**", colour = discord.Colour.random())
    await ctx.reply(embed=embed)
  except Exception:
    try:
      await ctx.reply("I don't have enough permissions to work properly")
    except Exception:
      try:
          await ctx.author.send(f"I don't have enough permissions in "+ctx.channel.mention)
      except Exception:
          pass
                               
@client.command()
async def embed(ctx, *, text=None):
    if ctx.author.guild_permissions.manage_messages == True or ctx.author.id==owner_id:
        if not ctx.guild.me.guild_permissions.embed_links:
            try:
                await ctx.reply('I don\'t have enough permissions in this channel')
            except Exception:
                try:
                    await ctx.author.send(f'I don\'t have enough permissions in {ctx.channel.mention}')
                except Exception:
                    try:
                        await ctx.message.add_reactions('❌')
                    except Exception:
                        pass
            finally:
                return
                
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
                await ctx.author.send(f"I don't have enough permissions in "+ctx.channel.mention)
            except Exception:
                pass
    else:
        try:
          await ctx.reply("You cannot use me since you don't have the required permissions. Tehehe!")
        except Exception:
          try:
              await ctx.author.send(f"I don't have enough permissions in "+ctx.channel.mention)
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
              await message.author.send(f"I don't have enough permissions in "+ctx.channel.mention)
        except Exception:
              pass

    await client.process_commands(message)

@client.event
async def on_message_edit(before, after):
    if before!=after:
        await client.process_commands(after)
            
@client.command()
async def invite(ctx):
  try:
    em=discord.Embed(title="Do you want me in your server?", description=f"Click [here](https://discord.com/api/oauth2/authorize?client_id={client.user.id}&permissions=604040320&scope=bot) to invite me to your server", colour=discord.Colour.random())
    await ctx.reply(embed=em)
  except Exception:
    try:
      await ctx.reply("I don't have enough permissions to work properly")
    except Exception:
          try:
              await ctx.author.send(f"I don't have enough permissions in "+ctx.channel.mention)
          except Exception:
                pass

@client.event
async def on_guild_join(guild):
    async for i in guild.audit_logs(action=discord.AuditLogAction.bot_add):
        if i.target==client.user:
            if permcheck(guild)=="Err":
                try:
                    await i.user.send(f"You didn't gave me the permissions I asked so I am leaving!\n😡")
                except Exception:
                    pass
                await guild.leave()
                return
            try:
                await i.user.send(f'Thanks for inviting me to **{guild.name}**. Can I call it my permanent home?')
                await i.user.send('https://tenor.com/view/blushing-anime-anime-girl-anime-cat-girl-gif-23131378')
            except Exception:
                pass
            break
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f'{prefix}help in {len(client.guilds)} servers'))
    await guild.me.edit(nick=guild.me.display_name+f" ({prefix})")
        
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        pass
        
@client.event
async def on_guild_remove(guild):
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f'{prefix}help in {len(client.guilds)} servers'))
    
client.run(my_secret)
