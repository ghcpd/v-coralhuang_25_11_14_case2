import os
import unittest
from unittest.mock import patch

from app import create_app, db, mail
from config import TestConfig
from app.models import EmailLog


class EmailTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()

        # ensure a clean db
        db.create_all()

        # capture sent messages
        self.sent = []

        def fake_send(msg):
            self.sent.append(msg)

        # monkeypatch mail.send
        self._orig_send = mail.send
        mail.send = fake_send

    def tearDown(self):
        # restore mail.send
        mail.send = self._orig_send

        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_send_email_sync(self):
        from app.email import send_email

        # By default TestConfig sets EMAIL_SEND_ASYNC False
        send_email("Test Sync", "noreply@example.com", ["user@example.com"], "body")

        # because TestConfig uses sync sends, EmailLog should be created
        log = EmailLog.query.first()
        self.assertIsNotNone(log)
        self.assertEqual(log.message, "Test Sync")

        # and the email should have been sent via the fake send
        self.assertEqual(len(self.sent), 1)
        self.assertEqual(self.sent[0].subject, "Test Sync")

    def test_send_email_async_and_join(self):
        from app import email as email_mod
        from app.email import send_email

        # Configure app to send emails async for this test
        self.app.config['EMAIL_SEND_ASYNC'] = True

        threads = []

        class TestThread:
            def __init__(self, target, args=(), kwargs=None, daemon=None):
                self._target = target
                self._args = args
                self._kwargs = kwargs or {}
                self.daemon = daemon

            def start(self):
                # start a real thread but keep reference
                import threading
                t = threading.Thread(target=self._target, args=self._args, kwargs=self._kwargs, daemon=self.daemon)
                threads.append(t)
                t.start()

        # monkeypatch Thread in the email module
        with patch.object(email_mod, 'Thread', TestThread):
            send_email("Test Async", "noreply@example.com", ["user@example.com"], "body")

            # join created threads to wait for processing
            for t in threads:
                t.join(timeout=2)

        # assert the email log was created
        log = EmailLog.query.filter_by(message="Test Async").first()
        self.assertIsNotNone(log)
        self.assertEqual(len(self.sent), 1)
        self.assertEqual(self.sent[0].subject, "Test Async")


if __name__ == '__main__':
    unittest.main()
