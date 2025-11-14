# tests.py (fixed)
import os
import unittest

from app import create_app, db, mail
from config import TestConfig
from app.models import EmailLog


class EmailTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        # close DB engine connections to allow file deletion
        db.engine.dispose()
        self.app_context.pop()
        # cleanup file-based sqlite created during tests
        try:
            os.remove('test.db')
        except FileNotFoundError:
            pass

    def test_send_email(self):
        from app.email import send_email

        # capture outgoing messages using Flask-Mail helper
        with mail.record_messages() as outbox:
            send_email("Test", "noreply@example.com", ["user@example.com"], "body", app=self.app)

        # message was recorded
        self.assertEqual(len(outbox), 1)
        self.assertEqual(outbox[0].subject, 'Test')

        # verify EmailLog entry exists
        logs = EmailLog.query.all()
        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0].message, 'Test')


    def test_send_email_async(self):
        # use an on-disk file DB to allow threads to operate safely
        class AsyncConfig(TestConfig):
            TESTING = False
            MAIL_USE_THREADING = True
            SQLALCHEMY_DATABASE_URI = 'sqlite:///test_async.db'

        app = create_app(AsyncConfig)
        ctx = app.app_context()
        ctx.push()
        db.create_all()

        from app.email import send_email
        thread = send_email("Async Test", "from@example.com", ["user@example.com"], "body", app=app)
        self.assertIsNotNone(thread)
        # wait for the thread to finish
        thread.join(timeout=2)

        self.assertFalse(thread.is_alive())
        logs = db.session.execute(db.select(EmailLog)).scalars().all()
        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0].message, 'Async Test')

        # cleanup
        db.session.remove()
        db.drop_all()
        db.engine.dispose()
        ctx.pop()
        try:
            os.remove('test_async.db')
        except FileNotFoundError:
            pass


if __name__ == '__main__':
    unittest.main()
