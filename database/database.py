import sqlite3


class Database:
    def __init__(self, database_name="data/matwana.db"):
        self.database_name = database_name

    def connect(self):
        return sqlite3.connect(self.database_name)

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

    # -------------------------
    # PLAYER METHODS
    # -------------------------

    def create_player(self, player):
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

    # -------------------------
    # MATATU METHODS
    # -------------------------

    def create_matatu(self, player_id, matatu):
        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO matatus (
                player_id,
                name,
                model,
                capacity,
                fuel,
                fuel_capacity,
                condition,
                speed,
                comfort,
                engine_level,
                suspension_level,
                seat_level,
                fuel_tank_level,
                comfort_level
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            player_id,
            matatu.name,
            matatu.model,
            matatu.capacity,
            matatu.fuel,
            matatu.fuel_capacity,
            matatu.condition,
            matatu.speed,
            matatu.comfort,
            matatu.engine_level,
            matatu.suspension_level,
            matatu.seat_level,
            matatu.fuel_tank_level,
            matatu.comfort_level
        ))

        connection.commit()

        matatu_id = cursor.lastrowid

        connection.close()

        return matatu_id

    def get_matatu(self, player_id):
        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                id,
                name,
                model,
                capacity,
                fuel,
                fuel_capacity,
                condition,
                speed,
                comfort,
                engine_level,
                suspension_level,
                seat_level,
                fuel_tank_level,
                comfort_level
            FROM matatus
            WHERE player_id = ?
            LIMIT 1
        """, (player_id,))

        matatu_data = cursor.fetchone()

        connection.close()

        return matatu_data

    def save_matatu(self, matatu_id, matatu):
        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE matatus
            SET
                name = ?,
                model = ?,
                capacity = ?,
                fuel = ?,
                fuel_capacity = ?,
                condition = ?,
                speed = ?,
                comfort = ?,
                engine_level = ?,
                suspension_level = ?,
                seat_level = ?,
                fuel_tank_level = ?,
                comfort_level = ?
            WHERE id = ?
        """, (
            matatu.name,
            matatu.model,
            matatu.capacity,
            matatu.fuel,
            matatu.fuel_capacity,
            matatu.condition,
            matatu.speed,
            matatu.comfort,
            matatu.engine_level,
            matatu.suspension_level,
            matatu.seat_level,
            matatu.fuel_tank_level,
            matatu.comfort_level,
            matatu_id
        ))

        connection.commit()
        connection.close()

    # -------------------------
    # TRIP METHODS
    # -------------------------

    def save_trip(self, player_id, trip):
        connection = self.connect()
        cursor = connection.cursor()

        event_name = None

        if trip.event:
            event_name = trip.event["name"]

        cursor.execute("""
            INSERT INTO trips (
                player_id,
                route_name,
                passengers,
                earnings,
                fuel_used,
                event_name,
                experience_earned,
                reputation_earned
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            player_id,
            trip.route.name,
            len(trip.passengers),
            trip.earnings,
            trip.fuel_used,
            event_name,
            trip.experience_earned,
            trip.reputation_earned
        ))

        connection.commit()
        connection.close()

    def get_trip_history(self, player_id):
        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                id,
                route_name,
                passengers,
                earnings,
                fuel_used,
                event_name,
                experience_earned,
                reputation_earned
            FROM trips
            WHERE player_id = ?
            ORDER BY id DESC
        """, (player_id,))

        trips = cursor.fetchall()

        connection.close()

        return trips


if __name__ == "__main__":
    database = Database()

    database.create_tables()

    print("Database initialized successfully.")