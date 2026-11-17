import unittest
from datetime import datetime
from app.profiles import is_commuting

class ProfileTests(unittest.TestCase):
    def setUp(self):
        self.profile = {"weekly_schedule": {
            "monday": {"departure": "17:30", "work_from_home": False},
            "tuesday": {"departure": "17:30", "work_from_home": True}
        }}
    def test_smart_working(self):
        self.assertFalse(is_commuting(self.profile, datetime(2026, 11, 17, 17, 0)))
    def test_departure_window(self):
        self.assertTrue(is_commuting(self.profile, datetime(2026, 11, 16, 17, 0)))
    def test_outside_window(self):
        self.assertFalse(is_commuting(self.profile, datetime(2026, 11, 16, 14, 0)))

if __name__ == "__main__":
    unittest.main()
