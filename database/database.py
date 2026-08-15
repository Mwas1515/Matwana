import sqlite3


class Database:
    def __init__(self, database_name="data/matwana.db"):
        self.database_name = database_name

    def connect(self):
        return sqlite3.connect(
            self.database_name
        )

    def create_tables(self):
        connection = self.connect()

        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                money INTEGER NOT NULL,
                level INTEGER NOT NULL,
                experience INTEGER NOT NULL,
                reputation INTEGER NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS matatus (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                model TEXT NOT NULL,
                capacity INTEGER NOT NULL,
                fuel REAL NOT NULL,
                fuel_capacity REAL NOT NULL,
                condition REAL NOT NULL,
                speed INTEGER NOT NULL,
                comfort INTEGER NOT NULL,
                engine_level INTEGER NOT NULL,
                suspension_level INTEGER NOT NULL,
                seat_level INTEGER NOT NULL,
                fuel_tank_level INTEGER NOT NULL,
                comfort_level INTEGER NOT NULL,
                FOREIGN KEY (player_id)
                    REFERENCES players(id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS trips (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id INTEGER NOT NULL,
                route_name TEXT NOT NULL,
                passengers INTEGER NOT NULL,
                earnings INTEGER NOT NULL,
                fuel_used REAL NOT NULL,
                event_name TEXT,
                experience_earned INTEGER NOT NULL,
                reputation_earned INTEGER NOT NULL,
                FOREIGN KEY (player_id)
                    REFERENCES players(id)
            )
        """)

        connection.commit()
        connection.close()

    def create_player(
        self,
        player
    ):
        connection = self.connect()

        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO players (
                name,
                money,
                level,
                experience,
                reputation
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            player.name,
            player.money,
            player.level,
            player.experience,
            player.reputation
        ))

        connection.commit()

        player_id = cursor.lastrowid

        connection.close()

        return player_id

    def get_player(self, name):
        connection = self.connect()

        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                id,
                name,
                money,
                level,
                experience,
                reputation
            FROM players
            WHERE name = ?
        """, (name,))

        player_data = cursor.fetchone()

        connection.close()

        return player_data

    def save_player(self, player_id, player):
        connection = self.connect()

        cursor = connection.cursor()

        cursor.execute("""
            UPDATE players
            SET
                money = ?,
                level = ?,
                experience = ?,
                reputation = ?
            WHERE id = ?
        """, (
            player.money,
            player.level,
            player.experience,
            player.reputation,
            player_id
        ))

        connection.commit()
        connection.close()
if __name__ == "__main__":
    database = Database()

    database.create_tables()

    print("Database initialized successfully.")