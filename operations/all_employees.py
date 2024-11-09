import sqlite3

from app_config.db_config import DATABASE_PATH


def get_all_employees():
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Employees')
        return cursor.fetchall()

if __name__ == "__main__":
    employees = get_all_employees()
    for employee in employees:
        print(employee)
