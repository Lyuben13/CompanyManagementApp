import sqlite3
from app_config.db_config import DATABASE_PATH

class Department:
    def __init__(self, department_name):
        self.department_name = department_name

    def save(self):
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO Departments (DepartmentName) VALUES (?)', (self.department_name,))
            conn.commit()
        print(f"Department '{self.department_name}' added.")

    @classmethod
    def get_all(cls):
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Departments')
            return cursor.fetchall()
