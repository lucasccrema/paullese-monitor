import unittest
from app.alerts import evaluate

class AlertTests(unittest.TestCase):
    def test_normal(self):
        self.assertEqual(evaluate(110, 100).status, "normal")
    def test_watch(self):
        self.assertEqual(evaluate(125, 100).status, "watch")
    def test_alert(self):
        self.assertEqual(evaluate(150, 100).status, "alert")
    def test_invalid(self):
        self.assertEqual(evaluate(0, 100).status, "invalid")

if __name__ == "__main__":
    unittest.main()
