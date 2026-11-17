import unittest
from app.segments import load_segments

class SegmentTests(unittest.TestCase):
    def test_segment_count_and_order(self):
        segments = load_segments()
        self.assertEqual(len(segments), 13)
        self.assertIn("Bugliano", segments[0]["name"])
        self.assertIn("Rondò Coop", segments[-1]["name"])

if __name__ == "__main__":
    unittest.main()
