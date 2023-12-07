# In this file you must implement your main query methods
# so they can be used by your database models to interact with your bot.

import os

import pymysql.cursors

# note that your remote host where your database is hosted
# must support user permissions to run stored triggers, procedures and functions.
db_host = os.environ["DB_HOST"]
db_username = os.environ["DB_USER"]
db_password = os.environ["DB_PASSWORD"]
db_name = os.environ["DB_NAME"]


class Database:

  def connect(self):
    """
        This method creates a connection with your database
        IMPORTANT: all the environment variables must be set correctly
                   before attempting to run this method. Otherwise, it
                   will throw an error message stating that the attempt
                   to connect to your database failed.
        """
    try:
      conn = pymysql.connect(host=db_host,
                             port=3306,
                             user=db_username,
                             password=db_password,
                             db=db_name,
                             charset="utf8mb4",
                             cursorclass=pymysql.cursors.DictCursor)
      print("Bot connected to database {}".format(db_name))
      return conn
    except ConnectionError as err:

      print(f"An error has occurred: {err.args[1]}")
      print("\n")

  #TODO: needs to implement the internal logic of all the main query operations
  def get_response(self,
                   query,
                   values=None,
                   fetchResult=False,
                   many_entities=False):
    """
        query: the SQL query with wildcards (if applicable) to avoid injection attacks
        values: the values passed in the query
        fetch: If set to True, then the method fetches data from the database (i.e with SELECT)
        many_entities: If set to True, the method can insert multiple entities at a time.
        """
    connection = self.connect()
    # your code here
    cursor = connection.cursor()
    if values:
      if many_entities:
        cursor.executemany(query, values)
      else:
        cursor.execute(query, values)
    else:
      cursor.execute(query)

    connection.commit()
    connection.close()  # close the connection , no memory leask
    if fetchResult:
      return cursor.fetchall()
    return None

  @staticmethod
  def select(query, values=None, fetchResult=True):
    database = Database()  # object
    return database.get_response(query, values=values, fetchResult=True)

  @staticmethod
  def insert(query, values=None, many_entities=False):
    database = Database()
    try:
      database.get_response(query, values=values, many_entities=many_entities)
      return True  # Indicate success if no exceptions were thrown
    except Exception as e:
      print(f"An error occurred during database insertion: {e}")
      return False  # Indicate failure on exception

  @staticmethod
  def update(query, values=None):
    database = Database()
    return database.get_response(query, values=values)

  @staticmethod
  def delete(query, values=None):
    database = Database()
    return database.get_response(query, values=values)


class Query:
  TOP_CLASSES = """
        SELECT wc.class_title, COUNT(*) as booking_count
        FROM booking_history bh
        JOIN workout_class wc ON bh.class_id = wc.class_id
        WHERE bh.status = 'Booked'
        GROUP BY bh.class_id
        ORDER BY booking_count DESC
        LIMIT %s
  """

  ATTENDANCE = """
        SELECT member_id , COUNT(*) as attendance_count
        FROM booking_history bh
        JOIN workout_class wc ON bh.class_id = wc.class_id
        WHERE MONTH(booking_date) = %s AND YEAR(booking_date) = %s 
        GROUP BY member_id

    
  """

  GET_INSTRUCTOR_SCHEDULE = """
        SELECT i.instructor_id, i.name, COUNT(*) AS class_count
        FROM instructor i
        JOIN workout_class wc ON i.instructor_id = wc.instructor_id
        JOIN schedule s ON wc.schedule_id = s.schedule_id
        WHERE DATE(s.start_time) = %s
        GROUP BY i.instructor_id, i.name
        HAVING COUNT(*) >= %s

  """

  INACTIVE_MEMBERS = """
        SELECT 
           m.member_id,
           m.start_date,
           m.end_date
        FROM 
           membership m
        LEFT JOIN 
           (SELECT DISTINCT 
                member_id 
            FROM 
                booking_history 
            WHERE 
                booking_date >= NOW() - INTERVAL %s MONTH
           ) bh ON m.member_id = bh.member_id
        WHERE 
           m.end_date > CURDATE() AND
           m.start_date <= CURDATE() AND
           bh.member_id IS NULL;
  """

  HAS_EXISTING_BOOKING = """
          SELECT COUNT(*) AS booking_count
          FROM booking_history
          WHERE member_id = %s AND class_id = %s AND DATE(booking_date) = %s

  """

  CREATE_NEW_BOOKING = """
          INSERT INTO booking_history (member_id, class_id, booking_date, status)
          VALUES (%s, %s, %s, 'Booked');
  """

  HAS_EMAIL_EXIST = """
      SELECT COUNT(*) AS email_count FROM account  WHERE email = %s

  """

  ADD_NEW_ACCOUNT = """
      INSERT INTO account (email, password, role, date_registered) VALUES (%s, %s, %s, %s)
  
  """

  UPDATE_BOOKED_STATUS = """
      UPDATE booking_history b
      JOIN membership m ON b.member_id = m.member_id
      SET b.status = 'Attended'
      WHERE b.member_id = %s
        AND b.cancellation_date IS NULL
        AND b.status = 'Booked'

  """

  FETCH_ATTENDED_BOOKINGS = """
        SELECT class_id, booking_date, status FROM booking_history
        WHERE member_id = %s AND status = 'Attended'

  """

  REACTIVATE_MEMBERSHIP = """
        SELECT DISTINCT m.member_id
        FROM membership m
        JOIN booking_history bh ON m.member_id = bh.member_id
        WHERE m.is_active = 0
            AND bh.status = 'Attended'
            AND bh.booking_date >= DATE_SUB(NOW(), INTERVAL 2 MONTH)
 """

  UPDATE_MEMBERSHIP_TO_ACTIVATE = """
        UPDATE membership
        SET is_active = 1
        WHERE member_id = %s


"""

  ASSINGED_PASS_CLASSES = """
  
       SELECT wc.class_id, wc.class_title, s.start_time
       FROM workout_class AS wc
       JOIN schedule AS s ON wc.schedule_id = s.schedule_id
       WHERE wc.instructor_id IS NULL
       AND s.start_time < NOW();
  
  """

  FIND_CANCELLED_BOOKINGS = """
        SELECT bh.member_id, wc.class_id, wc.class_title
        FROM booking_history AS bh
        JOIN workout_class AS wc ON bh.class_id = wc.class_id
        WHERE bh.status = 'Cancelled';
    """

  DELETE_CANCELLED_BOOKINGS = """
        DELETE FROM booking_history
        WHERE status = 'Cancelled';
  
  """

  MONTH_REVENUE = """
        SELECT SUM(price) AS total_revenue
        FROM purchase
        WHERE YEAR(date) = %s AND MONTH(date) = %s;

  
  """

  ATTENDANCE_COUNT = """
        SELECT COUNT(*) AS total_attended
        FROM booking_history
        WHERE member_id = %s AND status = 'Attended';
  
  
  """
