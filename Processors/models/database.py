import sqlite3

class DatabaseManager:
    _instance = None
    def __new__(cls, db_name="data/processors.db"):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance.db_name = db_name
        return cls._instance

    def connect(self):
        return sqlite3.connect(self.db_name)
