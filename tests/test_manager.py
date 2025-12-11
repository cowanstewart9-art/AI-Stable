import unittest
import os
import shutil
import sys

# Add src to path so we can import modules directly as they will be in the APK root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from manager import AIManager
from logger import AILogger

class TestAIManager(unittest.TestCase):
    def setUp(self):
        # Use a test database
        self.test_db = "test_ai_manager.db"
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

        # Instantiate Manager with the test db path.
        self.manager = AIManager(db_path=self.test_db)

    def tearDown(self):
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
        if os.path.exists("ai_manager_debug.log"):
            # Optional: clean up the file log too
            os.remove("ai_manager_debug.log")

    def test_register_and_execute_success(self):
        def add(a, b):
            return a + b

        self.manager.register_ai("Adder", add)
        result = self.manager.execute_ai("Adder", 5, 3)
        self.assertEqual(result, 8)

        logs = self.manager.get_history()
        # Should have registration, start, and success logs
        self.assertTrue(any("Registered AI: Adder" in log[4] for log in logs))
        self.assertTrue(any("AI 'Adder' completed successfully" in log[4] for log in logs))

    def test_execute_failure_handling(self):
        def crasher():
            raise ValueError("Boom")

        self.manager.register_ai("Crasher", crasher)
        result = self.manager.execute_ai("Crasher")
        self.assertIsNone(result)

        logs = self.manager.get_history()
        # Find the error log
        error_logs = [log for log in logs if log[2] == "ERROR"]
        self.assertTrue(len(error_logs) > 0)
        self.assertIn("AI 'Crasher' crashed (Bad Exit)", error_logs[0][4])
        self.assertIn("ValueError: Boom", error_logs[0][5])

if __name__ == '__main__':
    unittest.main()
