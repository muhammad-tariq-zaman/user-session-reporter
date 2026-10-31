import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unittest
from datetime import datetime
from main import parse_rows, summarise

NOW = datetime(2026, 10, 30, 12, 0, 0)
ROWS = [{"user": "alice", "host": "pc1", "login": "2026-10-30T09:00:00", "logout": "2026-10-30T11:00:00"},
        {"user": "bob", "host": "pc2", "login": "2026-10-30T10:00:00", "logout": ""}]


class TestSessionReporter(unittest.TestCase):
    def test_active_detection(self):
        sessions = parse_rows(ROWS, NOW)
        self.assertEqual([s["active"] for s in sessions], [False, True])

    def test_durations(self):
        sessions = parse_rows(ROWS, NOW)
        self.assertAlmostEqual(sessions[0]["minutes"], 120.0)
        self.assertAlmostEqual(sessions[1]["minutes"], 120.0)

    def test_summary(self):
        summary = summarise(parse_rows(ROWS, NOW))
        self.assertEqual(summary["active"], 1)
        self.assertEqual(summary["per_user"]["alice"], 120.0)
