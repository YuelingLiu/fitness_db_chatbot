"""
The code below is just representative of the implementation of a Bot. 
However, this code was not meant to be compiled as it. It is the responsability 
of all the students to modifify this code such that it can fit the 
requirements for this assignments.
"""

import discord
from discord.ext import commands

from database import Database
from models import *
import os

TOKEN = my_secret = os.environ['DISCORD_TOKEN']

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())


@bot.event
async def on_ready():

  print(f"{bot.user.name} joined the room")

  database = Database()
  if database.connect():
    print(f"{bot.user.name} is connected to the remote database")
  else:
    print(f"{bot.user.name} was unable to connect to the remote database")


@bot.command(
    name="test",
    description="write your database business requirement for this command here"
)
async def _test(ctx, arg1):
  testModel = TestModel(ctx, arg1)
  response = testModel.response()
  await ctx.send(response)


# TODO: complete the following tasks:
#       (1) Replace the commands' names with your own commands
#       (2) Write the description of your business requirement in the description parameter
#       (3) Implement your commands' methods.


@bot.command(name="TopClasses",
             description="database business requirement #1 here")
async def _command1(ctx, *args):
  await ctx.send("This method is not implemented yet")


@bot.command(name="getMemberAttendance",
             description="database business requirement #2 here")
async def _command2(ctx, *args):
  await ctx.send("This method is not implemented yet")


@bot.command(name="getInstructorSchedule",
             description="database business requirement #3 here")
async def _command3(ctx, *args):
  await ctx.send("This method is not implemented yet")


@bot.command(name="findInactiveMembers",
             description="database business requirement #4 here")
async def _command4(ctx, *args):
  await ctx.send("This method is not implemented yet")


@bot.command(name="createNewBooking",
             description="database business requirement #5 here")
async def _command5(ctx, *args):
  await ctx.send("This method is not implemented yet")


@bot.command(name="addNewInstructor",
             description="database business requirement #6 here")
async def _command6(ctx, *args):
  await ctx.send("This method is not implemented yet")


@bot.command(name="updateToAttended",
             description="database business requirement #7 here")
async def _command7(ctx, *args):
  await ctx.send("This method is not implemented yet")


@bot.command(name="updateSubStatus",
             description="database business requirement #8 here")
async def _command8(ctx, *args):
  await ctx.send("This method is not implemented yet")


@bot.command(name="cleanOrphanedBookings",
             description="database business requirement #9 here")
async def _command9(ctx, *args):
  await ctx.send("This method is not implemented yet")


@bot.command(name="cleanCancelledBookings",
             description="database business requirement #10 here")
async def _command10(ctx, *args):
  await ctx.send("This method is not implemented yet")


@bot.command(name="trigger_UpdateMemberStatus",
             description="database business requirement #11 here")
async def _command11(ctx, *args):
  await ctx.send("This method is not implemented yet")


@bot.command(name="trigger_AutoCancelOnDeletion",
             description="database business requirement #12 here")
async def _command12(ctx, *args):
  await ctx.send("This method is not implemented yet")


@bot.command(name="checkClassSpots <class_id>",
             description="database business requirement #13 here")
async def _command13(ctx, *args):
  await ctx.send("This method is not implemented yet")


@bot.command(name="getTotalClassAttended",
             description="database business requirement #14 here")
async def _command14(ctx, *args):
  await ctx.send("This method is not implemented yet")


@bot.command(name="monthRevenue",
             description="database business requirement #15 here")
async def _command15(ctx, *args):
  await ctx.send("This method is not implemented yet")


bot.run(TOKEN)
