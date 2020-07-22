import discord
import asyncio
import os
import math
from discord.ext import commands
import subprocess
import os
import sys
import ast
token = os.getenv('TOKEN')
bot = commands.Bot(command_prefix='<')
meid = 725390906647380148 #upload
chanid = 724793239600758885#724782647410425907 upload
owner = [674813875291422720]
glist=[724643561408168007]
jiwon=724794234846183524#722839399158513825
jiwonpri=725498508559253555
ticketlog=725116897049313391#722834701806600315
trash=724794592582434886#722837198063272028
warpchan=724794730386423848#724782647410425907 #announce
warpme=725120253851598879#724785078122840237  #announce
annlogchan=725118765506756638
annlogme=725122332829548576
startlog=725116861208854559#722834657799831602
bot.remove_command('help')
def insert_returns(body):
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)
@bot.event
async def on_ready():
    print('ready')
    await bot.get_channel(startlog).send(f"Ready, Logined as {bot.user}")
    bot.loop.create_task(bg_change_playing())
@bot.command()
async def clear(ctx,limit:int):
  await ctx.send("Clearing...")
  if ctx.message.author.id not in owner: return
  await ctx.channel.purge(limit=limit+2)
def insert_returns(body):
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)
class owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("config.json")
        self._last_result = None
        self.normal_color = 0x00fa6c
        self.error_color = 0xff4a4a
    @commands.command(name = 'eval')
    async def eval_fn(self, ctx, *, cmd):
      if ctx.author.id in [674813875291422720,714486865939660860]:
        try:
            fn_name = "_eval_expr"
            cmd = cmd.strip("` ")
            cmd = "\n".join(f"    {i}" for i in cmd.splitlines())
            body = f"async def {fn_name}():\n{cmd}"
            parsed = ast.parse(body)
            body = parsed.body[0].body
            insert_returns(body)
            env = {
                'bot': self.bot,
                'discord': discord,
                'commands': commands,
                'ctx': ctx,
                '__import__': __import__
                }
            exec(compile(parsed, filename="<ast>", mode="exec"), env)

            result = (await eval(f"{fn_name}()", env))
            await ctx.send(result)
        except Exception as a:
            await ctx.send(a)
      else:
        await ctx.send("어디서 감히 eval을 쓸려고")
    @commands.command()
    async def sudo(self,ctx, user : discord.Member,*, command : str):
      if ctx.author.id in [674813875291422720]:
        message = ctx.message
        message.author = user
        message.content = command
        await self.bot.process_commands(message)
    @commands.command(name = 'sudo2')
    async def sudo2(self, ctx, *, cmd):
      if ctx.author.id in [674813875291422720,714486865939660860]:
            cmds = cmd.split(' ')
            if cmds[0] == 'eval':
                await self.eval_fn(ctx = ctx, cmd = cmds[1])
            elif cmds[0] == '리로드':
                await self.reloadall(ctx = ctx)

    @commands.command()
    async def shell(self, ctx, *cmd) :
      if ctx.author.id in [674813875291422720,714486865939660860]:
          try :
            cmd = " ".join(cmd[:])
            res = subprocess.check_output(cmd, shell=True, encoding='utf-8')
            embed=discord.Embed(title="**Command Sent!**", description=f"Input : **{cmd}**", color=self.normal_color)
            embed.add_field(name="Output", value=f"```{res}```")
            await ctx.send(embed=embed)
          except (discord.errors.HTTPException) :
            await ctx.send ('글자수가 많아 일반 텍스트로 전송합니다.')
            cmd = " ".join(cmd[:])
            res = subprocess.check_output(cmd, shell=True, encoding='utf-8')
            await ctx.send("```" + res + "```")
          except (subprocess.CalledProcessError) :
            embed=discord.Embed(title="**Command Error!**", description="명령어 처리 도중 오류 발생!",color=self.error_color)
            await ctx.send(embed=embed)
def setup(bot):
    bot.add_cog(owner(bot))
@bot.command()
async def help(ctx):
  await ctx.send("```목록수정 ----- 제작자만\nupload\n채널수정\n이채널수정\nclose\nuploadmessage ----- 제작자만\ndelete ----- 제작자만\neval ----- 제작자만\nclear ----- 제작자만```")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.CommandNotFound):
      return
    elif isinstance(error, discord.ext.commands.MissingRequiredArgument):
        return
    else:
      pass #await ctx.send("알 수 없는 오류입니다.\nEndBot 등급이 부족할 수 있습니다.")
    raise error
roleid=724796434733596673#720570799890890813
@bot.event
async def on_raw_reaction_add(payload):
    guild = bot.get_guild(payload.guild_id)
    warp = discord.utils.get(guild.categories, name = "upload")
    warpp = discord.utils.get(guild.categories, name ='private-upload')
    member = guild.get_member(payload.user_id)
    print(payload.emoji.name)
    if payload.message_id == meid:
        if str (payload.emoji) == "📩":
            msg = await bot.get_channel(chanid).fetch_message(meid)
            await msg.remove_reaction('📩', member)
            ticket = await warpp.create_text_channel(f'📂{member.id}', topic=f'{member.id}')
            await ticket.set_permissions(member, read_messages=True, send_messages=True)
            role1 = discord.utils.get(guild.roles, id=roleid)
            await ticket.set_permissions(role1, read_messages=True, send_messages=True)
            await ticket.set_permissions(guild.default_role, read_messages=False)
            embed = discord.Embed(colour=0xff00, title="Upload Channel Created", description="✅ A new channel has been created.\nAfter uploading data to this channel, please specify the parent and sub directories. Example: ```Parent directory\n:warning:Top directory\nSub directory\n#📂minecraft#📂skateboard#deleted-channel#📂nol``` Enter `<close` to move the channel to the Recycle-Bin.")
            embed.set_footer(text=member.name, icon_url=member.avatar_url)
            mesg = await ticket.send(f'<@{member.id}>', embed=embed)
            await mesg.pin()
            embed = discord.Embed(colour=0xff00, title="Channel Created", description=f"채널 생성 유저 : {member}\n채널 이름 : `📂{member.id}`")
            embed.set_footer(text=member.name, icon_url=member.avatar_url)
            await bot.get_channel(ticketlog).send(embed=embed)
            return None

        if '📮a' == payload.emoji.name+'a':
            msg = await bot.get_channel(chanid).fetch_message(meid)
            await msg.remove_reaction('📮', member)
            ticket = await warp.create_text_channel(f'📂{member.id}', topic=f'{member.id}')
            #await ticket.set_permissions(member, read_messages=True, send_messages=True)
            #role1 = discord.utils.get(guild.roles, id=roleid)
            #await ticket.set_permissions(role1, read_messages=True, send_messages=True)
            #await ticket.set_permissions(guild.default_role, read_messages=False)
            embed = discord.Embed(colour=0xff00, title="Upload Channel Created", description="✅ A new channel has been created.\nAfter uploading data to this channel, please specify the parent and sub directories. Example: ```Parent directory\n:warning:Top directory\nSub directory\n#📂minecraft#📂skateboard#deleted-channel#📂nol``` Enter `<close` to move the channel to the Recycle-Bin.")
            embed.set_footer(text=member.name, icon_url=member.avatar_url)
            mesg = await ticket.send(f'<@{member.id}>', embed=embed)
            await mesg.pin()
            embed = discord.Embed(colour=0xff00, title="Channel Created", description=f"채널 생성 유저 : {member}\n채널 이름 : `📂{member.id}`")
            embed.set_footer(text=member.name, icon_url=member.avatar_url)
            await bot.get_channel(ticketlog).send(embed=embed)
            return None
async def 수정(message,reason):
        if message.author.id not in owner: return
        ㅁㄴㅇㄹq = await bot.get_channel(annlogchan).fetch_message(annlogme)
        cont=ㅁㄴㅇㄹq.content
        reason = cont+"\n"+reason
        ㅁㄴㅇㄹ = await bot.get_channel(warpchan).fetch_message(warpme)
        embed = discord.Embed(colour=0x2F3136, title="[ Materials ]", description=reason)
        await ㅁㄴㅇㄹ.edit(embed=embed,content=None)
        await ㅁㄴㅇㄹq.edit(content=reason)
async def 티켓수정(message):
  embed = discord.Embed(colour=0xff00, title="Ticket Edited", description=f"채널 수정 유저 : {message.author}\n채널 이름 : `{message.channel.name}`")
  embed.set_footer(text=message.author.name, icon_url=message.author.avatar_url)
  await bot.get_channel(ticketlog).send(embed=embed)
@bot.command()
async def 채널수정(ctx,channel:discord.TextChannel,*,rename:str):
      message=ctx.message
      if str(message.author.id) not in channel.topic: return
      elif str(message.author.id) in channel.topic:
        await channel.edit(name="📂"+rename)
        await 티켓수정(message)
        await message.channel.purge(limit=1)
@bot.command()
async def 이채널수정(ctx,*,rename:str):
      message=ctx.message
      channel=ctx.channel
      if str(message.author.id) not in channel.topic: return
      elif str(message.author.id) in channel.topic:
        await channel.edit(name="📂"+rename)
        await 티켓수정(message)
        await message.channel.purge(limit=1)
@bot.command()
async def delete(ctx):
  message=ctx.message
  if message.author.guild_permissions.administrator == True:
            ca = discord.utils.get(message.guild.categories, id=trash)
            if message.channel.category == ca:
                await message.channel.delete()
                embed = discord.Embed(colour=0xff00, title="Ticket Deleted", description=f"채널 삭제 유저 : {message.author}\n채널 이름 : `{message.channel.name}`")
                embed.set_footer(text=message.author.name, icon_url=message.author.avatar_url)
                await bot.get_channel(ticketlog).send(embed=embed)
            else:
                await message.channel.send("Since it is not Recycle-Bin category, it cannot be removed.")
@bot.command()
async def upload(ctx,*,reason):
  message=ctx.message
  await 수정(message,reason)
@bot.command()
async def 목록수정(ctx,*,reason):
        message=ctx.message
        if message.author.id not in owner: return
        ㅁㄴㅇㄹq = await bot.get_channel(annlogchan).fetch_message(annlogme)
        if reason == "None":
          reason=None
        ㅁㄴㅇㄹ = await bot.get_channel(warpchan).fetch_message(warpme)
        embed = discord.Embed(colour=0x2F3136, title="[ Materials ]", description=reason)
        await ㅁㄴㅇㄹ.edit(embed=embed,content=None)
        await ㅁㄴㅇㄹq.edit(content=reason)
@bot.command()
async def close(ctx):
        message=ctx.message
        ca = discord.utils.get(message.guild.categories, id=jiwon)
        ca1 = discord.utils.get(message.guild.categories, id=jiwonpri)
        if message.channel.category == ca or message.channel.category == ca1:
            await message.channel.set_permissions(message.guild.default_role, read_messages=False)
            await message.channel.set_permissions(message.author, read_messages=False)
            await message.channel.edit(category=discord.utils.get(message.guild.categories, name = "recycle-bin"))
            embed = discord.Embed(colour=0xff00, title="Ticket Locked", description=f"채널 잠금 유저 : {message.author}\n채널 이름 : `{message.channel.name}`")
            embed.set_footer(text=message.author.name, icon_url=message.author.avatar_url)
            await bot.get_channel(ticketlog).send(embed=embed)
            embed = discord.Embed(colour=0xff00, title="Upload Channel Locked", description=f"Channel Locked!")
            embed.set_footer(text=message.author.name, icon_url=message.author.avatar_url)
            await message.channel.send(embed=embed)
        else:
            await message.channel.send("Since it is not Upload category, it cannot be moved to the Recycle-Bin.")
@bot.command()
async def uploadmessage(ctx):
        message=ctx.message
        if message.author.id in owner:
            embed = discord.Embedembed = discord.Embed(colour=0xff00, title="Create an Upload Channel", description="You can upload materials!\nIf you create a private channel, a private channel that only managers and you can see will be created.\nOther inquiries/reports are possible, too. Among the emojis below, you can create a private channel with 📩 and a public channel with 📮.")
            embed.set_footer(text=bot.user.name, icon_url=bot.user.avatar_url)
            ticket = await message.channel.send(embed=embed)
            await ticket.add_reaction('📩')
            await ticket.add_reaction('📮')
        else:
          await message.channel.send("금지!")
# @bot.command()
# async def 위치(ctx,up:discord.TextChannel,down
@bot.before_invoke
async def is_registered(ctx):
  if ctx.message.channel.guild.id not in glist:
    await ctx.send("This Bot can ONLY be used at Discord Server 'CLOUD'. Here is the Invite Link. https://discord.gg/qdN7g6w")
    return
  await ctx.channel.trigger_typing()
async def bg_change_playing():
    while True:
      try:
        guild = bot.get_guild(724643561408168007)
        await bot.get_channel(725117974263889972).edit(name=f"👥 {len(list(filter(lambda x: not x.bot, guild.members)))} Users")
        #await bot.get_channel(722836493638303751).edit(name=f"🤖 {len(list(filter(lambda x: x.bot, guild.members)))} Bots")
        await asyncio.sleep(300)
      except Exception as e: print(e)
bot.run(token)
