from models.employee import Employee  # noqa
from datetime import datetime
import sqlite3
from app_config.db_config import DATABASE_PATH
from loguru import logger

# Setup logger
logger.add("logs/app_log.log", rotation="1 week", retention="10 days", compression="zip")


def add_employee(first_name, last_name, position_name, department_name, hire_date, manager_name, gender):
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute(''' 
            INSERT INTO Employees (FirstName, LastName, PositionName, DepartmentName, HireDate, ManagerName, Gender)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (first_name, last_name, position_name, department_name, hire_date, manager_name, gender))
        conn.commit()
        conn.close()
        logger.info(f"Added new employee: {first_name} {last_name} - Position: {position_name}")
    except Exception as e:
        logger.error(f"Error adding employee {first_name} {last_name}: {e}")


def delete_employee(employee_name):
    try:
        first_name, last_name = employee_name.split(" ", 1)

        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()

            logger.info(f"Attempting to delete employee: {employee_name}")
            cursor.execute('''DELETE FROM Employees WHERE FirstName = ? AND LastName = ?''', (first_name, last_name))
            conn.commit()

            cursor.execute('''SELECT * FROM Employees WHERE FirstName = ? AND LastName = ?''', (first_name, last_name))
            result = cursor.fetchall()

            if not result:
                logger.info(f"Employee {employee_name} has been successfully deleted.")
            else:
                logger.error(f"Error: Employee {employee_name} was not found.")
    except Exception as e:
        logger.error(f"Error deleting employee {employee_name}: {e}")


def promote_employee(employee_name, new_position):
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute('''UPDATE Employees
                          SET PositionName = ?
                          WHERE FirstName || ' ' || LastName = ?''', (new_position, employee_name))
        conn.commit()
        logger.info(f"Employee {employee_name} promoted to {new_position}.")
    except sqlite3.Error as e:
        logger.error(f"Error promoting employee {employee_name}: {e}")
    finally:
        conn.close() # noqa


def list_all_employees():
    """Get all employees from the database."""
    try:
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Employees')
            employees = cursor.fetchall()
            return employees
    except Exception as e:
        logger.error(f"Error fetching employees: {e}")
        return []


def get_team_leaders():
    """Retrieve all employees who are team leaders."""
    try:
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(''' 
                SELECT DISTINCT Employees.FirstName, Employees.LastName, Employees.PositionName
                FROM Employees
                JOIN Positions ON Employees.PositionName = Positions.PositionName
                WHERE Positions.IsTeamLeader = 1
            ''')
            leaders = cursor.fetchall()
            return leaders
    except Exception as e:
        logger.error(f"Error fetching team leaders: {e}")
        return []


def get_experienced_women():
    """Retrieve female employees with 10 or more years of experience."""
    try:
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT FirstName, LastName, HireDate, Gender
                              FROM Employees
                              WHERE Gender = 'Female' ''')
            today = datetime.today()
            experienced_women = []  # noqa

            for row in cursor.fetchall():
                first_name, last_name, hire_date, gender = row
                try:
                    hire_date_obj = datetime.strptime(hire_date, '%Y-%m-%d')
                    years_of_experience = (today - hire_date_obj).days // 365

                    if years_of_experience >= 10:
                        experienced_women.append((first_name, last_name, years_of_experience))
                except ValueError:
                    logger.error(f"Error: Invalid date format for {first_name} {last_name}: {hire_date}")
                    continue

            return experienced_women
    except Exception as e:
        logger.error(f"Error retrieving experienced women: {e}")
        return []


def save_report(report_text):
    try:
        with open('reports/operation_reports.txt', 'a') as f:
            f.write(report_text + '\n')
        logger.info("Report saved successfully.")
    except Exception as e:
        logger.error(f"Error saving report: {e}")


#
# new_employee = Employee(
#     first_name="John",
#     last_name="Doe",
#     position_name="Software Engineer",
#     department_name="IT",
#     hire_date="2023-01-15",
#     manager_name="Jane Smith",
#     gender="Male"
# )
# new_employee.save()
#
# all_employees = Employee.get_all()
# for emp in all_employees:
#     print(emp)
#
# Employee.promote_employee("John Doe", "Team Leader")

if __name__ == "__main__":
    experienced_women = get_experienced_women()
    for woman in experienced_women:
        logger.info(f"Experienced woman: {woman}")
