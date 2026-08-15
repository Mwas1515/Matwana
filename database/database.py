import os
import sqlite3
from datetime import datetime


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

        # ======================================
        # PLAYERS
        # ======================================

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

        # ======================================
        # MATATUS
        # ======================================

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

        # ======================================
        # TRIPS
        # ======================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS trips (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                player_id INTEGER NOT NULL,

                route_name TEXT NOT NULL,
                difficulty TEXT NOT NULL DEFAULT 'Easy',

                passengers INTEGER NOT NULL,

                base_earnings INTEGER NOT NULL DEFAULT 0,
                earnings INTEGER NOT NULL DEFAULT 0,

                fuel_used REAL NOT NULL DEFAULT 0,
                fuel_cost INTEGER NOT NULL DEFAULT 0,

                event_name TEXT,
                event_money INTEGER NOT NULL DEFAULT 0,

                driving_style TEXT,

                net_profit INTEGER NOT NULL DEFAULT 0,

                experience_earned INTEGER NOT NULL DEFAULT 0,
                reputation_earned INTEGER NOT NULL DEFAULT 0,

                distance REAL NOT NULL DEFAULT 0,

                completed_at TEXT,

                FOREIGN KEY (player_id)
                    REFERENCES players(id)
                    ON DELETE CASCADE
            )
        """)

        # ======================================
        # ACHIEVEMENTS
        # ======================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS achievements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                player_id INTEGER NOT NULL,

                achievement_key TEXT NOT NULL,
                achievement_name TEXT NOT NULL,
                description TEXT NOT NULL,

                unlocked_at TEXT NOT NULL,

                UNIQUE (
                    player_id,
                    achievement_key
                ),

                FOREIGN KEY (player_id)
                    REFERENCES players(id)
                    ON DELETE CASCADE
            )
        """)

        connection.commit()
        connection.close()

        # Update older databases.
        self.migrate_database()

    # ==========================================
    # DATABASE MIGRATION
    # ==========================================

    def migrate_database(self):
        connection = self.connect()
        cursor = connection.cursor()

        # ======================================
        # MATATU COLUMNS
        # ======================================

        cursor.execute("""
            PRAGMA table_info(matatus)
        """)

        columns = cursor.fetchall()

        column_names = [
            column[1]
            for column in columns
        ]

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

        # ======================================
        # TRIP COLUMNS
        # ======================================

        cursor.execute("""
            PRAGMA table_info(trips)
        """)

        trip_columns = cursor.fetchall()

        trip_column_names = [
            column[1]
            for column in trip_columns
        ]

        trip_upgrade_columns = {
            "difficulty": (
                "TEXT NOT NULL DEFAULT 'Easy'"
            ),
            "base_earnings": (
                "INTEGER NOT NULL DEFAULT 0"
            ),
            "fuel_cost": (
                "INTEGER NOT NULL DEFAULT 0"
            ),
            "event_money": (
                "INTEGER NOT NULL DEFAULT 0"
            ),
            "driving_style": (
                "TEXT"
            ),
            "net_profit": (
                "INTEGER NOT NULL DEFAULT 0"
            ),
            "distance": (
                "REAL NOT NULL DEFAULT 0"
            ),
            "completed_at": (
                "TEXT"
            )
        }

        for column_name, column_definition in (
            trip_upgrade_columns.items()
        ):
            if column_name not in trip_column_names:
                cursor.execute(
                    f"""
                    ALTER TABLE trips
                    ADD COLUMN {column_name}
                    {column_definition}
                    """
                )

                print(
                    f"Database migration: "
                    f"added trips."
                    f"'{column_name}' column."
                )

        # ======================================
        # FIX OLD TRIP DATA
        # ======================================

        # Old databases may have earnings but no
        # base earnings or net profit information.
        cursor.execute("""
            UPDATE trips
            SET base_earnings = earnings
            WHERE base_earnings = 0
            AND earnings > 0
        """)

        cursor.execute("""
            UPDATE trips
            SET net_profit = earnings
            WHERE net_profit = 0
            AND earnings > 0
        """)

        # ======================================
        # FIX ACTIVE MATATUS
        # ======================================

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

        # ======================================
        # UNIQUE ACTIVE MATATU
        # ======================================

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

        driving_style = None

        if trip.driving_style:
            driving_style = trip.driving_style["name"]

        completed_at = datetime.now().isoformat(
            timespec="seconds"
        )

        cursor.execute("""
            INSERT INTO trips (
                player_id,
                route_name,
                difficulty,
                passengers,
                base_earnings,
                earnings,
                fuel_used,
                fuel_cost,
                event_name,
                event_money,
                driving_style,
                net_profit,
                experience_earned,
                reputation_earned,
                distance,
                completed_at
            )
            VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?, ?, ?
            )
        """, (
            player_id,
            trip.route.name,
            trip.route.difficulty,
            len(trip.passengers),
            trip.base_earnings,
            trip.earnings,
            trip.fuel_used,
            trip.fuel_cost,
            event_name,
            trip.event_money,
            driving_style,
            trip.net_profit,
            trip.experience_earned,
            trip.reputation_earned,
            trip.route.distance,
            completed_at
        ))

        connection.commit()

        trip_id = cursor.lastrowid

        connection.close()

        return trip_id

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
    # STATISTICS
    # ==========================================

    def get_player_statistics(
        self,
        player_id
    ):
        """
        Return overall statistics for a player.
        """

        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                COUNT(*),
                COALESCE(SUM(passengers), 0),
                COALESCE(SUM(earnings), 0),
                COALESCE(SUM(fuel_used), 0),
                COALESCE(SUM(fuel_cost), 0),
                COALESCE(SUM(net_profit), 0),
                COALESCE(SUM(experience_earned), 0),
                COALESCE(SUM(reputation_earned), 0),
                COALESCE(SUM(distance), 0)
            FROM trips
            WHERE player_id = ?
        """, (player_id,))

        statistics = cursor.fetchone()

        connection.close()

        return {
            "total_trips": statistics[0],
            "total_passengers": statistics[1],
            "total_earnings": statistics[2],
            "total_fuel_used": statistics[3],
            "total_fuel_cost": statistics[4],
            "total_net_profit": statistics[5],
            "total_experience": statistics[6],
            "total_reputation": statistics[7],
            "total_distance": statistics[8]
        }

    def get_best_trip(
        self,
        player_id
    ):
        """
        Return the player's most profitable trip.
        """

        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                route_name,
                net_profit,
                earnings,
                passengers,
                difficulty,
                completed_at
            FROM trips
            WHERE player_id = ?
            ORDER BY net_profit DESC
            LIMIT 1
        """, (player_id,))

        trip = cursor.fetchone()

        connection.close()

        return trip

    def get_route_statistics(
        self,
        player_id
    ):
        """
        Return statistics grouped by route.
        """

        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                route_name,
                COUNT(*) AS trips,
                COALESCE(SUM(passengers), 0),
                COALESCE(SUM(earnings), 0),
                COALESCE(SUM(net_profit), 0),
                COALESCE(SUM(distance), 0)
            FROM trips
            WHERE player_id = ?
            GROUP BY route_name
            ORDER BY net_profit DESC
        """, (player_id,))

        statistics = cursor.fetchall()

        connection.close()

        return statistics

    def get_driving_style_statistics(
        self,
        player_id
    ):
        """
        Return statistics grouped by driving style.
        """

        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                driving_style,
                COUNT(*) AS trips,
                COALESCE(SUM(earnings), 0),
                COALESCE(SUM(net_profit), 0),
                COALESCE(SUM(fuel_used), 0)
            FROM trips
            WHERE player_id = ?
            AND driving_style IS NOT NULL
            GROUP BY driving_style
            ORDER BY trips DESC
        """, (player_id,))

        statistics = cursor.fetchall()

        connection.close()

        return statistics

    # ==========================================
    # ACHIEVEMENTS
    # ==========================================

    def achievement_unlocked(
        self,
        player_id,
        achievement_key
    ):
        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT 1
            FROM achievements
            WHERE player_id = ?
            AND achievement_key = ?
        """, (
            player_id,
            achievement_key
        ))

        unlocked = cursor.fetchone() is not None

        connection.close()

        return unlocked

    def unlock_achievement(
        self,
        player_id,
        achievement_key,
        achievement_name,
        description
    ):
        """
        Unlock an achievement.

        Returns True if the achievement was newly
        unlocked and False if it already existed.
        """

        if self.achievement_unlocked(
            player_id,
            achievement_key
        ):
            return False

        connection = self.connect()
        cursor = connection.cursor()

        unlocked_at = datetime.now().isoformat(
            timespec="seconds"
        )

        cursor.execute("""
            INSERT INTO achievements (
                player_id,
                achievement_key,
                achievement_name,
                description,
                unlocked_at
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            player_id,
            achievement_key,
            achievement_name,
            description,
            unlocked_at
        ))

        connection.commit()
        connection.close()

        return True

    def get_achievements(
        self,
        player_id
    ):
        """
        Return all unlocked achievements.
        """

        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                id,
                achievement_key,
                achievement_name,
                description,
                unlocked_at
            FROM achievements
            WHERE player_id = ?
            ORDER BY id ASC
        """, (player_id,))

        achievements = cursor.fetchall()

        connection.close()

        return achievements

    # ==========================================
    # DATABASE RESET
    # ==========================================

    def delete_player_data(
        self,
        player_id
    ):
        """
        Delete all data belonging to a player.

        Foreign-key cascading removes matatus,
        trips and achievements.
        """

        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("""
            DELETE FROM players
            WHERE id = ?
        """, (player_id,))

        connection.commit()

        deleted = cursor.rowcount > 0

        connection.close()

        return deleted


# ==========================================
# TEST DATABASE
# ==========================================

if __name__ == "__main__":
    database = Database()

    database.create_tables()

    print(
        "Database initialized successfully."
    )