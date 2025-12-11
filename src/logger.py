import logging
import sqlite3
from datetime import datetime
import os

class AILogger:
    def __init__(self, db_path="ai_manager.db"):
        self.db_path = db_path
        self._init_db()
        self._setup_file_logging()

    def _init_db(self):
        """Initialize the SQLite database for structured logging."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                level TEXT,
                source TEXT,
                message TEXT,
                details TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def _setup_file_logging(self):
        """Setup standard python logging to file as a backup."""
        logging.basicConfig(
            filename='ai_manager_debug.log',
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    def log(self, level, source, message, details=""):
        """Log an event to the database and file."""
        # Log to file
        if level == "INFO":
            logging.info(f"[{source}] {message} - {details}")
        elif level == "ERROR":
            logging.error(f"[{source}] {message} - {details}")
        elif level == "WARNING":
            logging.warning(f"[{source}] {message} - {details}")

        # Log to DB
        timestamp = datetime.now().isoformat()
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO logs (timestamp, level, source, message, details)
                VALUES (?, ?, ?, ?, ?)
            ''', (timestamp, level, source, message, str(details)))
            conn.commit()
            conn.close()
        except Exception as e:
            logging.error(f"Failed to log to DB: {e}")

    def get_logs(self, limit=50):
        """Retrieve recent logs."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM logs ORDER BY id DESC LIMIT ?', (limit,))
            rows = cursor.fetchall()
            conn.close()
            return rows
        except Exception as e:
            logging.error(f"Failed to retrieve logs: {e}")
            return []
