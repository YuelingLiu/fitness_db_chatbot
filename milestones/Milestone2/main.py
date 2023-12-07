"""
The code below is just representative of the implementation of a Bot. 
However, this code was not meant to be compiled as it. It is the responsability 
of all the students to modifify this code such that it can fit the 
requirements for this assignments.
"""

import discord
from discord.ext import commands
from datetime import datetime

from database import Database
from models import *
import os
from models import AddAccountModel
from models import CreateNewBookingModel

TOKEN = my_secret = os.environ['DISCORD_TOKEN']

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())


@bot.event
async def on_ready():

  print(f"{bot.user.name} joined the room")
  # creat tge database object
  database = Database()
  if database.connect():  # call
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


# Business requirement 1: this function is to get the top x classes which have the highest attendance
# command example: !TopClasses 2
@bot.command(
    name="TopClasses",
    description=
    "Find the top  X  classes with the highest attendance. Order by descending order."
)
async def TopClasses(ctx, number_of_classes: int):
  try:

    if number_of_classes <= 0:
      # to handle invalid input
      await ctx.send("Please enter a positive number")
      return

    top_classes_model = TopClassesModel(number_of_classes)
    result = top_classes_model.get_top_classes(number_of_classes)
    print("any result from the database", result)

    if result is not None:
      # Handle the result
      response = "\n".join([
          f"Class Title: {item['class_title']}, Bookings: {item['booking_count']}"
          for item in result
      ])
      await ctx.send(response)
    else:
      # Handle the case where result is None
      await ctx.send("No data found")

  except Exception as e:
    await ctx.send(f"Error from the 1st business requirement: {str(e)}")


# business requirement 2
# command eg: !getMembersAttendance 2023 01
@bot.command(
    name="getMembersAttendance",
    description=
    " Retrieve the attendance of members who has attended workout class in a given month and year"
)
async def getMembersAttendance(ctx, month: int, year: int):
  if month <= 0 or year <= 0:
    # to handle invalid input
    await ctx.send("Please enter a positive number")
    return

  try:
    attendance = MembersAttendanceModel(month, year)

    result = attendance.get_attendance()
    print("checking what is result in the second requirement", result)

    if result:

      response = "\n".join([
          f"Member id: {item['member_id']}, Attendance count: {item['attendance_count']}"
          for item in result
      ])
      await ctx.send(response)
    else:
      await ctx.send("Data not found!")

  except Exception as e:
    await ctx.send(f"An error occurred: {str(e)}")


# business requirement 3
# command example: !getInstructorsSchedule 2 2023-11-05
@bot.command(
    name="getInstructorsSchedule",
    description=
    "Retrieve all instructors who are teaching more than X classes on a given date"
)
async def getInstructorsSchedule(ctx, min_classes: int, date: str):
  try:
    schedule_model = InstructorScheduleModel(min_classes, date)
    result = schedule_model.get_instructor_schedule()
    print('testing 3rd business requirement', result)

    if result:
      response = '\n'.join([
          f"instructor_id: {item['instructor_id']}, Name: {item['name']}, Class Count: {item['class_count']}"
          for item in result
      ])
      await ctx.send(response)
    else:
      await ctx.send("No data found !")

  except Exception as e:
    await ctx.send(f"An error occurred: {str(e)}")


# business requirement 4
@bot.command(
    name="findInactiveMembers",
    description=
    "Find all members who have not booked any classes in the last X months but have an active subscription"
)
async def findInactiveMembers(ctx, month: int):
  try:
    if month <= 0:
      # to handle invalid input
      await ctx.send("Please enter a positive number")
      return
    print("Does this function get called?")

    inactive_members_model = InactiveMemberModel(month)
    result = inactive_members_model.get_inactive_members(month)
    if result is not None:
      response = "\n\n".join([
          f"Member ID: {item['member_id']}, Start Date: {item['start_date'].strftime('%Y-%m-%d')}, End Date: {item['end_date'].strftime('%Y-%m-%d')}"
          for item in result
      ])
      await ctx.send(response)
      # print("result from 4th", result)
    else:
      await ctx.send("Error from the fourth business requirement ")

  except Exception as e:
    await ctx.send(f"An error occurred: {str(e)}")


# business requirement 5
# command example: !createNewBooking 888802  9905 2023-12-15
@bot.command(
    name="createNewBooking",
    description=
    "Create a record in the member's booking history for a class that has been scheduled on a specified date."
)
async def createNewBooking(ctx, member_id: int, class_id, booking_date: str):
  # helper function to validate member_id
  def is_valid_member(member_id):
    try:
      member_model = MemberModel()
      result = member_model.get_member(member_id)
      if result:
        print("member exist", result)
        return True
    except Exception as e:
      print(e)
      return False

  # helper function to validate class_id
  def is_valid_class(class_id):
    try:
      class_model = ClassModel()
      result = class_model.get_class(class_id)
      if result:
        print("class exist", result)
        return True
    except Exception as e:
      print(e)
      return False

  # helper function to validate booking_date
  def is_valid_date(booking_date):
    try:
      datetime.strptime(booking_date, "%Y-%m-%d")
      return True
    except ValueError:
      return False

  # validate member_id
  if not is_valid_member(member_id):
    await ctx.send("Invalid member ID.")
    return

  # validate class_id
  if not is_valid_class(class_id):
    await ctx.send("Invalid class ID.")
    return
  
  if not is_valid_date(booking_date):
    await ctx.send("Invalid booking date. Please use the format YYYY-MM-DD.")
    return

  # also need to check if this member has already booked the same class at the same date
  creat_new_booking_model = CreateNewBookingModel(member_id, class_id,
                                                  booking_date)
  if creat_new_booking_model.has_existing_booking():
    await ctx.send(
        "This member havs already booked this class on the selected date.")
    return

  try:
    result = creat_new_booking_model.creat_new_booking()
    print("checking result from 5th", result)
    if result:
      await ctx.send(
          f"Booking created for member {member_id} for class {class_id} on {booking_date}."
      )
      print("result from 5th", result)
    else:
      await ctx.send("Error from the fifth business requirement ")

  except Exception as e:
    # Handle any errors during insertion
    await ctx.send(f"An error occurred while creating the booking: {str(e)}")


# helper function to validate registered date
def is_valid_registered_date(date: str):
  try:
    # Parse the date string
    valid_date = datetime.strptime(date, '%Y-%m-%d').date()
    return valid_date <= datetime.now().date(
    )  # Return True if date is today or in the past
  except ValueError:
    return False  # Return False if date format is invalid


# business requirement 6
@bot.command(
    name="addNewInstructorAccount",
    description=
    "Add a new  account to account table and assign its role as instructor")
async def addNewInstructorAccount(ctx, email: str, password: str, role: str,
                                  date_registered: str):

  account_model = AddAccountModel()
  # validate if this email has already registered account
  if account_model.has_email_exist(email):
    await ctx.send("An account with this email already exists.")
    return

  # validate if registered date is in the past or today, cannot registered an account for the furture date
  if not is_valid_registered_date(date_registered):
    await ctx.send(
        "Invalid date format or date is in the future. Please use YYYY-MM-DD and ensure the date is today or in the past."
    )
    return

  try:
    result = account_model.add_account(email, password, role, date_registered)
    if result:
      await ctx.send(
          f"Account created successfully for email {email} with role {role}.")
    else:
      await ctx.send("An error occurred while creating the account.")
  except Exception as e:
    await ctx.send(f"An error occurred while creating the account: {str(e)}")


# business requirement 7
# command example: !updateBookedToAttended 888803
@bot.command(
    name="updateBookedToAttended",
    description=
    "Update the status of all bookings to 'Attended' for a member who has a record of attendance in the gym on the day of their booking"
)
async def updateBookedToAttended(ctx, member_id: int):

  # validate memver id
  member_model = MemberModel()
  if not member_model.get_member(member_id):
    await ctx.send("Invalid member ID.")
    return

  booking_model = BookingModel()

  try:
    # first update the status from "Booked" to "Attended"
    booking_model.update_booked_status_to_attended(member_id)

    # fetch the list of "Attdenced" bookings for the this member
    attended_classes = booking_model.fetch_attended_bookings(member_id)

    if attended_classes:
      # Format and send the list of attended classes
      response = "\n".join([
          f"Class ID: {cls['class_id']}, Booking Date: {cls['booking_date']}, Status: {cls['status']}"
          for cls in attended_classes
      ])
      await ctx.send(
          f"Member {member_id} has attended the following classes:\n{response}"
      )
    else:
      await ctx.send("No attended classes found for this member.")
  except Exception as e:
    await ctx.send(f"An error occurred: {str(e)}")


# business requirement 8
# command example:  !reactivateMemberships
# returns a list of of memmber_ids that have attended a workout class in the past month and these member_id is_active is 1 now
@bot.command(
    name="reactivateMemberships",
    description="Reactivate memberships based on recent class attendance")
async def reactivateMemberships(ctx):
  print("Command called to reactivate memberships.")

  membership_model = MembershipModel()
  try:
    reactivated_memberships = membership_model.reactivate_memberships_based_on_recent_activity(
    )
    print("Memberships processed for reactivation:", reactivated_memberships)

    if reactivated_memberships:
      reactivated_memberships_str = ', '.join(map(str,
                                                  reactivated_memberships))
      await ctx.send(
          f"The following memberships have been reactivated: {reactivated_memberships_str}"
      )
    else:
      await ctx.send(
          "No memberships were reactivated based on recent activity.")
  except Exception as e:
    await ctx.send(f"An error occurred: {str(e)}")


# business requirement 9
# command example: !removeUnassignedPastClasses
@bot.command(
    name="removeUnassignedPastClasses",
    description=
    "Remove all class records from the workout_class table that have not been assigned an instructor and are not scheduled in the future, indicating these classes will not take place"
)
async def removeUnassignedPastClasses(ctx):

  workout_class_model = WorkoutClassModel()

  try:
    # Call the method to delete unassigned past classes
    classes_to_delete = workout_class_model.delete_unassigned_past_classes()

    if classes_to_delete:
      details = "\n".join(
          f"Class ID: {c['class_id']}, Title: {c['class_title']}, Scheduled Time: {c['start_time']}"
          for c in classes_to_delete)
      await ctx.send(
          f"The following classes were removed because they had no instructor assigned and were scheduled in the past:\n{details}"
      )
    else:
      await ctx.send("There were no classes to remove.")

  except Exception as e:
    await ctx.send(f"An error occurred: {str(e)}")


# business requirement 10
@bot.command(name="cleanupCancelledBookings",
             description=
             "Clean up cancelled bookings for classes without future schedules"
             )
async def cleanupCancelledBookings(ctx):

  booking_history_model = BookingHistoryModel()

  try:
    # First, get the cancelled bookings that need to be deleted
    to_be_deleted_bookings = booking_history_model.get_cancelled_bookings()

    if to_be_deleted_bookings:
      # Delete the cancelled bookings
      booking_history_model.delete_cancelled_bookings()

      # Format the message with the details of the deleted bookings
      booking_details = "\n".join(
          f"Member ID: {booking['member_id']}, Class ID: {booking['class_id']}, Title: {booking['class_title']}"
          for booking in to_be_deleted_bookings)

      await ctx.send(
          f"The following cancelled bookings have been removed:\n{booking_details}"
      )
    else:
      await ctx.send("No cancelled bookings were found to be removed.")

  except Exception as e:
    await ctx.send(f"An error occurred: {str(e)}")


# business requirement 11
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


# business requirement 14
@bot.command(
    name="getAttendanceCount",
    description="Get the total number of classes a member has attended")
async def getAttendanceCount(ctx, member_id: int):
  attendance_model = AttendanceModel()

  try:
    count = attendance_model.get_attendance_count(member_id)
    await ctx.send(f"Member {member_id} has attended {count} classes.")
  except Exception as e:
    await ctx.send(f"An error occurred: {str(e)}")


# business requirement 15
@bot.command(
    name="monthRevenue",
    description=
    "Retrieves a  total membership revenue from membership registrations  for a  specific month and year"
)
async def monthRevenue(ctx, year: int, month: int):
  purchase_model = RevenuesModel()

  try:
    result = purchase_model.get_monthly_revenue(year, month)
    print("checkng the result of montly reveue", result)
    if result is not None:
      revenue = result[0]
      await ctx.send(
          f"Total purchase revenue for {month}/{year} is: ${revenue}")
    else:
      await ctx.send("No revenue data found for the specified month and year.")
  except Exception as e:
    await ctx.send(f"An error occurred: {str(e)}")


bot.run(TOKEN)
