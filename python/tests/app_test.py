import unittest
import course_activity_planner


class AppTest(unittest.TestCase):

    def setUp(self):
        self.app = course_activity_planner.app

    def tearDown(self):
        pass

    def test_app_is_created(self):
        self.assertTrue(self.app)

if __name__ == '__main__':
    unittest.main()
