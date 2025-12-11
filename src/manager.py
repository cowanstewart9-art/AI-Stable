import traceback
import sys
from logger import AILogger

class AIManager:
    def __init__(self, db_path="ai_manager.db"):
        self.logger = AILogger(db_path=db_path)
        self.registered_functions = {}

    def register_ai(self, name, function):
        """Register a new AI function."""
        self.registered_functions[name] = function
        self.logger.log("INFO", "Manager", f"Registered AI: {name}")

    def execute_ai(self, name, *args, **kwargs):
        """Execute a registered AI function with error monitoring."""
        if name not in self.registered_functions:
            self.logger.log("ERROR", "Manager", f"AI '{name}' not found.")
            return None

        self.logger.log("INFO", "Manager", f"Starting AI: {name}", f"Args: {args}")

        try:
            result = self.registered_functions[name](*args, **kwargs)
            self.logger.log("INFO", "Manager", f"AI '{name}' completed successfully.")
            return result
        except Exception as e:
            # Capture the full traceback
            tb = traceback.format_exc()
            self.logger.log("ERROR", "Manager", f"AI '{name}' crashed (Bad Exit)", f"Error: {e}\nTraceback: {tb}")
            return None

    def get_history(self):
        return self.logger.get_logs()
