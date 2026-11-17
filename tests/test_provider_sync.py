# Creato il: 2026-11-17 12:36
import unittest
from app.provider import POINTS
from app.segments import load_segments


class ProviderSyncTests(unittest.TestCase):
    """Verifica che segments.json e POINTS in provider.py descrivano lo stesso percorso."""

    def test_segment_ids_are_sequential(self):
        ids = [s["id"] for s in load_segments()]
        self.assertEqual(ids, list(range(1, len(POINTS))))

    def test_segment_count_matches_provider(self):
        self.assertEqual(len(load_segments()), len(POINTS) - 1)

    def test_coordinates_match_provider(self):
        for index, segment in enumerate(load_segments()):
            _, lat_a, lon_a = POINTS[index]
            _, lat_b, lon_b = POINTS[index + 1]
            with self.subTest(segment_id=segment["id"]):
                self.assertEqual((segment["from"]["lat"], segment["from"]["lon"]), (lat_a, lon_a))
                self.assertEqual((segment["to"]["lat"], segment["to"]["lon"]), (lat_b, lon_b))


if __name__ == "__main__":
    unittest.main()
