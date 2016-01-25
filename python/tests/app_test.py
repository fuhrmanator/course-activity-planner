import requests
import unittest
import course_activity_planner


class AppTest(unittest.TestCase):

    def setUp(self):
        self.app = course_activity_planner.app.test_client()

    def tearDown(self):
        pass

    def test_app_is_created(self):
        self.assertTrue(self.app)

    def test_generate_uuid(self):
        self.assertEqual(
            36, len(course_activity_planner._generate_transaction_uuid()))

    def test_get_cookie(self):
        res = self.app.post('/api/planning')
        self.assertEqual(200, res._status_code)

if __name__ == '__main__':
    unittest.main()
