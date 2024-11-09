import sqlite3
from app_config.db_config import DATABASE_PATH


class Employee:
    def __init__(self, first_name="", last_name="", position_name="", department_name="",
                 hire_date="", manager_name="", gender=""):
        self.first_name = first_name
        self.last_name = last_name
        self.position_name = position_name
        self.department_name = department_name
        self.hire_date = hire_date
        self.manager_name = manager_name
        self.gender = gender

    def save(self):
        """Save the employee to the database."""
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO Employees (FirstName, LastName, PositionName, DepartmentName, HireDate, ManagerName, Gender)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (self.first_name, self.last_name, self.position_name, self.department_name, self.hire_date,
                  self.manager_name, self.gender))
            conn.commit()
        print(f"Employee '{self.first_name} {self.last_name}' added.")

    @classmethod
    def get_all(cls):
        """Retrieve all employees from the database."""
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Employees')
            return cursor.fetchall()

    @classmethod
    def get_team_leaders(cls):
        """Retrieve all employees who are team leaders."""
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT Employees.FirstName, Employees.LastName, Employees.PositionName
                FROM Employees
                JOIN Positions ON Employees.PositionName = Positions.PositionName
                WHERE Positions.IsTeamLeader = 1
            ''')
            return cursor.fetchall()

    @classmethod
    def promote_employee(cls, employee_name, new_position):
        """Promote an employee to a new position."""
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE Employees
                SET PositionName = ?
                WHERE FirstName || ' ' || LastName = ?
            ''', (new_position, employee_name))
            conn.commit()
            print(f"Employee '{employee_name}' promoted to '{new_position}'.")
