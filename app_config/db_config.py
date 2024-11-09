import sqlite3
import os

DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'company.db')

def get_connection():
    try:
        connection = sqlite3.connect(DATABASE_PATH)
        return connection
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def initialize_database():
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Employees (
                EmployeeID INTEGER PRIMARY KEY AUTOINCREMENT,
                FirstName TEXT,
                LastName TEXT,
                PositionName TEXT,
                DepartmentName TEXT,
                HireDate TEXT,
                ManagerName TEXT,
                Gender TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Positions (
                PositionID INTEGER PRIMARY KEY AUTOINCREMENT,
                PositionName TEXT,
                IsTeamLeader INTEGER
            )
        ''')

        conn.commit()
        conn.close()
        print("Database initialized successfully.")

    except Exception as e:
        print(f"Error initializing database: {e}")


def insert_position(position_name, is_team_leader=0):
    try:
        with sqlite3.connect(DATABASE_PATH) as connection:
            cursor = connection.cursor()
            cursor.execute(''' 
                INSERT INTO Positions (PositionName, IsTeamLeader)
                VALUES (?, ?)
            ''', (position_name, is_team_leader))
            connection.commit()
            print(f"Position '{position_name}' inserted successfully.")
    except sqlite3.Error as e:
        print(f"Error inserting position: {e}")


def insert_department(department_name):
    try:
        with sqlite3.connect(DATABASE_PATH) as connection:
            cursor = connection.cursor()
            cursor.execute(''' 
                INSERT INTO Departments (DepartmentName)
                VALUES (?)
            ''', (department_name,))
            connection.commit()
            print(f"Department '{department_name}' inserted successfully.")
    except sqlite3.Error as e:
        print(f"Error inserting department: {e}")


def insert_employee(first_name, last_name, position_name, department_name, hire_date, manager_name, gender):
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO Employees (FirstName, LastName, PositionName, DepartmentName, HireDate, ManagerName, Gender)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (first_name, last_name, position_name, department_name, hire_date, manager_name, gender))

        conn.commit()
        print(f"Employee {first_name} {last_name} added to the database.")
        conn.close()
    except Exception as e:
        print(f"Error inserting employee: {e}")


def get_all_employees():
    try:
        with sqlite3.connect(DATABASE_PATH) as connection:
            cursor = connection.cursor()
            cursor.execute(''' 
                SELECT FirstName, LastName, PositionName, DepartmentName, HireDate, ManagerName 
                FROM Employees
            ''')
            employee_list = cursor.fetchall()  # Fetching all employees
            return employee_list  # Return the list of employees
    except sqlite3.Error as e:
        print(f"Error retrieving employees: {e}")
        return []


def delete_employee_by_name(employee_name):
    try:
        with sqlite3.connect(DATABASE_PATH) as connection:
            cursor = connection.cursor()
            cursor.execute(''' 
                DELETE FROM Employees WHERE FirstName || ' ' || LastName = ?
            ''', (employee_name,))
            connection.commit()
            print(f"Employee '{employee_name}' deleted successfully.")
    except sqlite3.Error as e:
        print(f"Error deleting employee: {e}")
