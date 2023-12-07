"""
In this file you must implement all your database models.
If you need to use the methods from your database.py call them
statically. For instance:
       # opens a new connection to your database
       connection = Database.connect()
       # closes the previous connection to avoid memory leaks
       connection.close()
"""

from database import Database
from database import Query


class TestModel:
  """
    This is an object model example. Note that
    this model doesn't implement a DB connection.
    """

  def __init__(self, ctx):
    self.ctx = ctx
    self.author = ctx.message.author.name

  def response(self):
    return f'Hi, {self.author}. I am alive'


# this is a model to check if this member_id exists in db
class MemberModel:

  def __init__(self):
    self.db = Database()
    self.table = 'membership'
    self.id = None
    self.name = None

  def get_member(self, member_id):
    query = "SELECT COUNT(*) FROM membership WHERE member_id = %s"
    result = self.db.select(query, (member_id, ))
    print("what is result to check if member exsits", result)
    member_exists = result[0]['COUNT(*)'] > 0 if result else False
    return member_exists


class ClassModel:

  def __init__(self):
    self.db = Database()
    self.table = 'workout_class'
    self.class_id = None

  def get_class(self, class_id):
    query = "SELECT COUNT(*) FROM workout_class WHERE class_id = %s"
    result = self.db.select(query, (class_id, ))
    print("Check if class exists", result)
    class_exists = result[0]['COUNT(*)'] > 0 if result else False
    return class_exists


# business requirement 1 model
class TopClassesModel:

  def __init__(self, number_of_classes):
    self.number_of_classes = number_of_classes
    self.db = Database()

  def get_top_classes(self, number_of_classes):
    return self.db.select(Query.TOP_CLASSES, (self.number_of_classes, ))


# business requirement 2 model
class MembersAttendanceModel:

  def __init__(self, month, year):
    self.db = Database()

    self.month = month
    self.year = year

  def get_attendance(self):
    result = self.db.select(Query.ATTENDANCE, (
        self.month,
        self.year,
    ))
    print("att", result)
    return result


# business requirement 3 model
class InstructorScheduleModel:

  def __init__(self, min_classes, date):
    self.min_classes = min_classes
    self.date = date
    self.db = Database()

  def get_instructor_schedule(self):
    return self.db.select(Query.GET_INSTRUCTOR_SCHEDULE,
                          (self.date, self.min_classes))


# business requirement 4 model
class InactiveMemberModel:

  def __init__(self, month):
    self.month = month
    self.db = Database()

  def get_inactive_members(self, month):
    return self.db.select(Query.INACTIVE_MEMBERS, (self.month, ))


# business requirement 5 model
class CreateNewBookingModel:

  def __init__(self, member_id, class_id, booking_date):
    self.member_id = member_id
    self.class_id = class_id
    self.booking_date = booking_date
    self.db = Database()

#

  def has_existing_booking(self):
    result = self.db.select(Query.HAS_EXISTING_BOOKING, (
        self.member_id,
        self.class_id,
        self.booking_date,
    ))
    if result:
      booking_count = result[0]['booking_count']
      return booking_count > 0
    else:
      # Handle the case where result is None or empty
      return False

  def creat_new_booking(self):
    return self.db.insert(Query.CREATE_NEW_BOOKING, (
        self.member_id,
        self.class_id,
        self.booking_date,
    ))


# business requirement 6 model
class AddAccountModel:

  def __init__(self):
    self.db = Database()

  def has_email_exist(self, email):
    result = self.db.select(Query.HAS_EMAIL_EXIST, (email, ))
    if result and result[0]['email_count'] > 0:
      return True  # existing email found
    return False  # No existing email found

  def add_account(self, email, password, role, date_registered):
    if self.has_email_exist(email):
      return False  # Email already exists
    return self.db.insert(Query.ADD_NEW_ACCOUNT,
                          (email, password, role, date_registered))


# business 7 model
class BookingModel:

  def __init__(self):
    self.db = Database()

  def update_booked_status_to_attended(self, member_id):
    return self.db.update(Query.UPDATE_BOOKED_STATUS, (member_id, ))

  def fetch_attended_bookings(self, member_id):
    return self.db.select(Query.FETCH_ATTENDED_BOOKINGS, (member_id, ))


# business requirement 8 model
class MembershipModel:

  def __init__(self):
    self.db = Database()

  def reactivate_memberships_based_on_recent_activity(self):
    memberships = self.db.select(Query.REACTIVATE_MEMBERSHIP, ())

    print("memberships", memberships)

    # If no account IDs to reactivate, return an empty list
    if not memberships:
      return []

    # Update the is_active status for these account IDs
    for member_id in memberships:

      self.db.update(Query.UPDATE_MEMBERSHIP_TO_ACTIVATE, (member_id, ))

    return memberships


# business requirement 9 model
class WorkoutClassModel:

  def __init__(self):
    self.db = Database()

    self.table = 'workout_classes'

  def delete_unassigned_past_classes(self):
    # select the classes need to be deleted

    classes_to_delete = self.db.select(Query.ASSINGED_PASS_CLASSES, ())

    class_ids_to_delete = [
        str(class_info['class_id']) for class_info in classes_to_delete
    ]

    if class_ids_to_delete:
      delete_query = """
          DELETE FROM workout_class
          WHERE class_id IN ({});
      """.format(','.join(class_ids_to_delete))
      self.db.delete(delete_query)

    # Return to main of  the deleted classes
    return classes_to_delete


# business requirement 10 model
class BookingHistoryModel:

  def __init__(self):
    self.db = Database()
    self.table = 'booking_history'

  def get_cancelled_bookings(self):
    # select the classes need to be deleted
    return self.db.select(Query.FIND_CANCELLED_BOOKINGS, ())

  def delete_cancelled_bookings(self):
    return self.db.delete(Query.DELETE_CANCELLED_BOOKINGS, ())


# business requirement 141 model


class AttendanceModel:

  def __init__(self):
    self.db = Database()

  def get_attendance_count(self, member_id):
    result = self.db.select(Query.ATTENDANCE_COUNT, (member_id, ))

    if result:
      return result[0]['total_attended']
    else:
      return 0


# business requirement 15 FUNCTION
class RevenuesModel:

  def __init__(self):
    self.db = Database()

  def get_monthly_revenue(self, year, month):
    result = self.db.select(Query.MONTH_REVENUE, (year, month))
    print("print it from model to see result month", result)

    # If the select method returns a tuple with one element (which is the sum of the prices)
    return result
