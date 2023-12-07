


# Discord API has a limited number of requests (bot requests) per day.
# If developers meet that quota, then Discord will put a temporal ban to your bot (24 hours)
# In order to avoid that, and only for testing, create unit test methods to test your functions
# without using the functionality provided by your bot. Once all your tests passed, then you can
# integrate these functions with your bot logic in main.py

import unittest
from unittest.mock import patch
from models import TopClassesModel
from models import MembersAttendanceModel


class TestTopClassesModel(unittest.TestCase):

  @patch('models.Database.select')
  def test_get_top_classes(self, mock_select):
    # Mocking the database response
    mock_select.return_value = [{
        'class_title': 'Cardio Blast',
        'booking_count': 3
    }, {
        'class_title': 'Pilates Powerhouse',
        'booking_count': 2
    }]

    model = TopClassesModel(2)  # create an instance for this model
    result = model.get_top_classes()  # instance call the class
    print("checking result from unit test:", result)

    self.assertEqual(len(result), 2)
    self.assertEqual(result[0]['class_title'], 'Cardio Blast')
    self.assertEqual(result[1]['class_title'], 'Pilates Powerhouse')


class TestMembersAttendanceModel(unittest.TestCase):

  def test_get_attendance(self):
    year = 2023
    month = 10

    expected_result = [
        {
            'member_id': 888803,
            'attendance_count': 2
        },
    ]
    model = MembersAttendanceModel(year, month)
    result = model.get_attendance(year, month)
    print('Expected:', expected_result)
    print('Actual:', result)

    self.assertEqual(result, expected_result)


if __name__ == '__main__':
  unittest.main()
