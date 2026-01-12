import unittest
import time
import os
from app import create_app, db
from app.models import EmailLog  # Import models before using db.create_all
from config import TestConfig


class EmailTestCase(unittest.TestCase):
    """Test suite for email functionality."""
    
    @classmethod
    def setUpClass(cls):
        """Set up class-level fixtures."""
        # Ensure test database is clean before running all tests
        if os.path.exists('instance'):
            import shutil
            try:
                shutil.rmtree('instance')
            except:
                pass
    
    @classmethod
    def tearDownClass(cls):
        """Clean up class-level fixtures."""
        # Clean up test database after all tests
        if os.path.exists('instance'):
            import shutil
            try:
                shutil.rmtree('instance')
            except:
                pass
    
    def setUp(self):
        """Set up test fixtures before each test."""
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Create all tables and ensure they're committed
        db.create_all()
        db.session.commit()
        
        # Track background threads
        self.threads = []

    def tearDown(self):
        """Clean up after each test."""
        # Wait for background email threads to complete
        for thread in self.threads:
            if thread.is_alive():
                thread.join(timeout=2.0)
                if thread.is_alive():
                    self.app.logger.warning(f"Thread {thread.name} did not complete within timeout")
        
        # Now clean up database and context
        db.session.remove()
        db.drop_all()
        db.session.commit()
        self.app_context.pop()

    def test_send_email_creates_log(self):
        """Test that send_email creates an email log entry in the database."""
        from app.email import send_email
        
        # Send an email
        thread = send_email(
            "Test Subject",
            "noreply@example.com",
            ["user@example.com"],
            "Test body"
        )
        
        # Track the thread so tearDown can wait for it
        self.threads.append(thread)
        
        # Wait for the background thread to complete
        thread.join(timeout=2.0)
        self.assertFalse(thread.is_alive(), "Email thread did not complete in time")
        
        # Verify email log was created
        logs = EmailLog.query.all()
        self.assertEqual(len(logs), 1, f"Expected 1 log, got {len(logs)}")
        
        log = logs[0]
        self.assertEqual(log.subject, "Test Subject")
        self.assertEqual(log.sender, "noreply@example.com")
        self.assertEqual(log.recipients, "user@example.com")
        self.assertEqual(log.body, "Test body")

    def test_send_email_multiple_recipients(self):
        """Test send_email with multiple recipients."""
        from app.email import send_email
        
        recipients = ["user1@example.com", "user2@example.com", "user3@example.com"]
        thread = send_email(
            "Multi-recipient Test",
            "sender@example.com",
            recipients,
            "Testing multiple recipients"
        )
        
        self.threads.append(thread)
        thread.join(timeout=2.0)
        self.assertFalse(thread.is_alive(), "Email thread did not complete in time")
        
        logs = EmailLog.query.all()
        self.assertEqual(len(logs), 1, f"Expected 1 log, got {len(logs)}")
        
        log = logs[0]
        self.assertEqual(log.recipients, "user1@example.com,user2@example.com,user3@example.com")

    def test_send_email_no_context_errors(self):
        """Test that send_email works within app context without errors."""
        from app.email import send_email
        
        # This should not raise an error
        try:
            thread = send_email(
                "No Context Test",
                "test@example.com",
                ["recipient@example.com"],
                "Body"
            )
            self.threads.append(thread)
            thread.join(timeout=2.0)
            self.assertFalse(thread.is_alive(), "Email thread did not complete in time")
        except Exception as e:
            self.fail(f"send_email raised {type(e).__name__}: {e}")

    def test_database_not_corrupted_after_async_send(self):
        """Test that database remains valid after async email send."""
        from app.email import send_email
        
        # Send first email
        thread1 = send_email("First", "sender@example.com", ["r1@example.com"], "Body 1")
        self.threads.append(thread1)
        thread1.join(timeout=2.0)
        self.assertFalse(thread1.is_alive(), "Email thread 1 did not complete in time")
        
        # Send second email
        thread2 = send_email("Second", "sender@example.com", ["r2@example.com"], "Body 2")
        self.threads.append(thread2)
        thread2.join(timeout=2.0)
        self.assertFalse(thread2.is_alive(), "Email thread 2 did not complete in time")
        
        # Verify both logs exist and are correct
        logs = EmailLog.query.order_by(EmailLog.id).all()
        self.assertEqual(len(logs), 2, f"Expected 2 logs, got {len(logs)}")
        self.assertEqual(logs[0].subject, "First")
        self.assertEqual(logs[1].subject, "Second")


if __name__ == '__main__':
    unittest.main()
