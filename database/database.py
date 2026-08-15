import os
import sqlite3


class Database:
    def __init__(self, database_name="data/matwana.db"):
        self.database_name = database_name

        database_directory = os.path.dirname(
            self.database_name
        )

        if database_directory:
            os.makedirs(
                database_directory,
                exist_ok=True
            )

    # ==========================================
    # CONNECTION
    # ==========================================

    def connect(self):
        connection = sqlite3.connect(
            self.database_name
        )

        connection.execute(
            "PRAGMA foreign_keys = ON"
        )

        return connection

    # ==========================================
    # DATABASE SETUP
    # ==========================================

    def create_tables(self):
        connection = self.connect()
        cursor = connection.cursor()

        # -------------------------
        # PLAYERS
        # -------------------------

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

        # -------------------------
        # MATATUS
        # -------------------------

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
                engine_level INTEGER NOT NULL DEFAULT 1,
                suspension_level INTEGER NOT NULL DEFAULT 1,
                seat_level INTEGER NOT NULL DEFAULT 1,
                fuel_tank_level INTEGER NOT NULL DEFAULT 1,
                comfort_level INTEGER NOT NULL DEFAULT 1,
                active INTEGER NOT NULL DEFAULT 0,

                FOREIGN KEY (player_id)
                    REFERENCES players(id)
                    ON DELETE CASCADE
            )
        """)

        # -------------------------
        # TRIPS
        # -------------------------

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
                    ON DELETE CASCADE
            )
        """)

        connection.commit()
        connection.close()

        self.migrate_database()

    # ==========================================
    # DATABASE MIGRATION
    # ==========================================

    def migrate_database(self):
        connection = self.connect()
        cursor = connection.cursor()

        # -------------------------
        # MATATU COLUMNS
        # -------------------------

        cursor.execute("""
            PRAGMA table_info(matatus)
        """)

        columns = cursor.fetchall()

        column_names = [
            column[1]
            for column in columns
        ]

        # Add upgrade columns to older databases.
        upgrade_columns = {
            "engine_level": (
                "INTEGER NOT NULL DEFAULT 1"
            ),
            "suspension_level": (
                "INTEGER NOT NULL DEFAULT 1"
            ),
            "seat_level": (
                "INTEGER NOT NULL DEFAULT 1"
            ),
            "fuel_tank_level": (
                "INTEGER NOT NULL DEFAULT 1"
            ),
            "comfort_level": (
                "INTEGER NOT NULL DEFAULT 1"
            ),
            "active": (
                "INTEGER NOT NULL DEFAULT 0"
            )
        }

        for column_name, column_definition in (
            upgrade_columns.items()
        ):
            if column_name not in column_names:
                cursor.execute(
                    f"""
                    ALTER TABLE matatus
                    ADD COLUMN {column_name}
                    {column_definition}
                    """
                )

                print(
                    f"Database migration: "
                    f"added '{column_name}' column."
                )

        # -------------------------
        # FIX ACTIVE MATATUS
        # -------------------------

        cursor.execute("""
            SELECT DISTINCT player_id
            FROM matatus
        """)

        player_ids = cursor.fetchall()

        for row in player_ids:
            player_id = row[0]

            cursor.execute("""
                SELECT id
                FROM matatus
                WHERE player_id = ?
                AND active = 1
                ORDER BY id ASC
            """, (player_id,))

            active_matatus = cursor.fetchall()

            # No active matatu.
            if not active_matatus:
                cursor.execute("""
                    SELECT id
                    FROM matatus
                    WHERE player_id = ?
                    ORDER BY id ASC
                    LIMIT 1
                """, (player_id,))

                first_matatu = cursor.fetchone()

                if first_matatu:
                    cursor.execute("""
                        UPDATE matatus
                        SET active = 1
                        WHERE id = ?
                    """, (first_matatu[0],))

            # Multiple active matatus.
            elif len(active_matatus) > 1:
                keep_active = active_matatus[0][0]

                cursor.execute("""
                    UPDATE matatus
                    SET active = 0
                    WHERE player_id = ?
                """, (player_id,))

                cursor.execute("""
                    UPDATE matatus
                    SET active = 1
                    WHERE id = ?
                """, (keep_active,))

        # -------------------------
        # UNIQUE ACTIVE MATATU
        # -------------------------

        cursor.execute("""
            CREATE UNIQUE INDEX IF NOT EXISTS
            one_active_matatu_per_player
            ON matatus(player_id)
            WHERE active = 1
        """)

        connection.commit()
        connection.close()

    # ==========================================
    # PLAYER METHODS
    # ==========================================

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

    # ==========================================
    # MATATU METHODS
    # ==========================================

    def create_matatu(
        self,
        player_id,
        matatu,
        active=True
    ):
        connection = self.connect()
        cursor = connection.cursor()

        if active:
            cursor.execute("""
                UPDATE matatus
                SET active = 0
                WHERE player_id = ?
            """, (player_id,))

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
                comfort_level,
                active
            )
            VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?
            )
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
            matatu.comfort_level,
            1 if active else 0
        ))

        connection.commit()

        matatu_id = cursor.lastrowid

        connection.close()

        return matatu_id

    def get_matatu(self, player_id):
        """
        Return the player's active matatu.
        """

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
                comfort_level,
                active
            FROM matatus
            WHERE player_id = ?
            AND active = 1
            LIMIT 1
        """, (player_id,))

        matatu_data = cursor.fetchone()

        connection.close()

        return matatu_data

    def get_matatu_by_id(
        self,
        player_id,
        matatu_id
    ):
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
                comfort_level,
                active
            FROM matatus
            WHERE player_id = ?
            AND id = ?
        """, (
            player_id,
            matatu_id
        ))

        matatu_data = cursor.fetchone()

        connection.close()

        return matatu_data

    def get_all_matatus(self, player_id):
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
                comfort_level,
                active
            FROM matatus
            WHERE player_id = ?
            ORDER BY id ASC
        """, (player_id,))

        matatus = cursor.fetchall()

        connection.close()

        return matatus

    def matatu_exists(
        self,
        player_id,
        matatu_id
    ):
        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT 1
            FROM matatus
            WHERE player_id = ?
            AND id = ?
        """, (
            player_id,
            matatu_id
        ))

        exists = cursor.fetchone() is not None

        connection.close()

        return exists

    def set_active_matatu(
        self,
        player_id,
        matatu_id
    ):
        connection = self.connect()
        cursor = connection.cursor()

        # Verify ownership.
        cursor.execute("""
            SELECT id
            FROM matatus
            WHERE id = ?
            AND player_id = ?
        """, (
            matatu_id,
            player_id
        ))

        matatu = cursor.fetchone()

        if matatu is None:
            connection.close()
            return False

        # Deactivate all vehicles.
        cursor.execute("""
            UPDATE matatus
            SET active = 0
            WHERE player_id = ?
        """, (player_id,))

        # Activate selected vehicle.
        cursor.execute("""
            UPDATE matatus
            SET active = 1
            WHERE id = ?
            AND player_id = ?
        """, (
            matatu_id,
            player_id
        ))

        connection.commit()
        connection.close()

        return True

    def save_matatu(
        self,
        matatu_id,
        matatu
    ):
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

        updated = cursor.rowcount > 0

        connection.close()

        return updated

    # ==========================================
    # TRIP METHODS
    # ==========================================

    def save_trip(
        self,
        player_id,
        trip
    ):
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

    def get_trip_history(
        self,
        player_id
    ):
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


# ==========================================
# TEST DATABASE
# ==========================================

if __name__ == "__main__":
    database = Database()

    database.create_tables()

    print(
        "Database initialized successfully."
    )