import sqlite3

DATABASE_PATH = 'company.db'

def initialize_database():
    """Initializes the database with tables and sample data."""
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()

        # Create Positions Table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Positions (
            PositionID INTEGER PRIMARY KEY AUTOINCREMENT,
            PositionName TEXT NOT NULL,
            IsTeamLeader INTEGER NOT NULL DEFAULT 0
        )''')

        # Create Employees Table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Employees (
            EmployeeID INTEGER PRIMARY KEY AUTOINCREMENT,
            FirstName TEXT NOT NULL,
            LastName TEXT NOT NULL,
            PositionName TEXT NOT NULL,
            DepartmentName TEXT NOT NULL,
            HireDate TEXT NOT NULL,
            ManagerName TEXT,
            Gender TEXT NOT NULL,
            FOREIGN KEY (PositionName) REFERENCES Positions (PositionName)
        )''')

        # Insert Sample Data
        insert_sample_data(cursor)

        conn.commit()

def insert_sample_data(cursor):
    """Inserts some sample data into Positions and Employees tables."""
    # Insert sample positions
    cursor.execute('''INSERT OR IGNORE INTO Positions (PositionName, IsTeamLeader) VALUES 
                      ('Manager', 1),
                      ('Developer', 0),
                      ('HR', 0),
                      ('Team Lead', 1)''')

    # Insert sample employees
    cursor.execute('''INSERT OR IGNORE INTO Employees (FirstName, LastName, PositionName, DepartmentName, HireDate, ManagerName, Gender) VALUES  
                      ('Checho', 'Chechev', 'Manager', 'Sales', '2021-01-15', NULL, 'Male'),
                      ('Penka', 'Penkova', 'Developer', 'Engineering', '2022-05-10', 'Checho Chechev', 'Female'), 
                      ('Ani', 'Ankova', 'Team Lead', 'Engineering', '2021-02-25', 'Checho Chechev', 'Female'), 
                      ('Bozhidar', 'Bobov', 'Developer', 'Engineering', '2022-08-20', 'Checho Chechev', 'Male'), 
                      ('Stefka', 'Bankova', 'HR', 'Human Resources', '2020-03-11', 'Checho Chechev', 'Female')''') # noqa

    print("Sample data inserted.")

if __name__ == "__main__":
    initialize_database()
    print("Database initialized successfully.")
