# tests.py (buggy)
import unittest
from app import create_app, db
from config import TestConfig

class EmailTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        # ❌ Bug: thread may still be running → pop happens too early
        self.app_context.pop()

    def test_send_email(self):
        from app.email import send_email
        send_email("Test", "noreply@example.com", ["user@example.com"], "body")
        # test ends before async thread finishes
        self.assertTrue(True)
