import sqlite3
from app_config.db_config import DATABASE_PATH

class Position:
    def __init__(self, position_name, is_team_leader=0):
        self.position_name = position_name
        self.is_team_leader = is_team_leader

    def save(self):
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO Positions (PositionName, IsTeamLeader) VALUES (?, ?)',
                           (self.position_name, self.is_team_leader))
            conn.commit()
        print(f"Position '{self.position_name}' added.")

    @classmethod
    def get_all(cls):
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Positions')
            return cursor.fetchall()
