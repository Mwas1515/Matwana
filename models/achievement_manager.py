from models.achievement import Achievement


class AchievementManager:
    """Manage player achievements."""

    # ==========================================
    # BUILD STATISTICS
    # ==========================================

    @staticmethod
    def build_statistics(
        player,
        database,
        player_id
    ):
        """
        Build the statistics used to check
        achievement requirements.
        """

        # -------------------------
        # TRIP STATISTICS
        # -------------------------

        trips = database.get_trip_history(
            player_id
        )

        total_trips = len(trips)

        # Total earnings from completed trips.
        total_earnings = sum(
            trip[3]
            for trip in trips
        )

        # Total passengers transported.
        total_passengers = sum(
            trip[2]
            for trip in trips
        )

        # Total distance.
        #
        # The current trips table stores the
        # route name but does not store distance.
        #
        # This will remain 0 until route distance
        # is added to the trip database.
        total_distance = 0

        # -------------------------
        # MATATU STATISTICS
        # -------------------------

        matatus = database.get_all_matatus(
            player_id
        )

        total_matatus = len(matatus)

        # -------------------------
        # PLAYER STATISTICS
        # -------------------------

        return {
            "trips": total_trips,
            "earnings": total_earnings,
            "profit": total_earnings,
            "passengers": total_passengers,
            "distance": total_distance,
            "level": player.level,
            "reputation": player.reputation,
            "matatus": total_matatus
        }

    # ==========================================
    # CHECK ACHIEVEMENTS
    # ==========================================

    @classmethod
    def check_achievements(
        cls,
        player,
        database,
        player_id
    ):
        """
        Check every achievement and unlock any
        achievement whose requirement has been met.

        Returns:
            list: Newly unlocked achievement IDs.
        """

        statistics = cls.build_statistics(
            player,
            database,
            player_id
        )

        newly_unlocked = []

        # Get all available achievements.
        achievements = (
            Achievement.get_all_achievements()
        )

        for achievement_id in achievements:

            # -------------------------
            # ALREADY UNLOCKED?
            # -------------------------

            if database.has_achievement(
                player_id,
                achievement_id
            ):
                continue

            # -------------------------
            # CHECK REQUIREMENT
            # -------------------------

            completed = (
                Achievement.check_requirement(
                    achievement_id,
                    statistics
                )
            )

            if not completed:
                continue

            # -------------------------
            # SAVE ACHIEVEMENT
            # -------------------------

            unlocked = (
                database.unlock_achievement(
                    player_id,
                    achievement_id
                )
            )

            if unlocked:
                newly_unlocked.append(
                    achievement_id
                )

        return newly_unlocked

    # ==========================================
    # DISPLAY ACHIEVEMENTS
    # ==========================================

    @classmethod
    def display_new_achievements(
        cls,
        achievement_ids,
        player
    ):
        """
        Display newly unlocked achievements
        and give their rewards.
        """

        if not achievement_ids:
            return

        print("\n" + "=" * 50)
        print("ACHIEVEMENTS UNLOCKED!")
        print("=" * 50)

        for achievement_id in achievement_ids:

            achievement = (
                Achievement.get_achievement(
                    achievement_id
                )
            )

            if achievement is None:
                continue

            reward = achievement["reward"]

            # -------------------------
            # GIVE REWARD
            # -------------------------

            player.earn_money(
                reward
            )

            # -------------------------
            # DISPLAY ACHIEVEMENT
            # -------------------------

            print(
                f"\n {achievement['name']}"
            )

            print(
                f"   {achievement['description']}"
            )

            print(
                f"   Reward: "
                f"KSh {reward}"
            )

        print("\n" + "=" * 50)

    # ==========================================
    # PROCESS ACHIEVEMENTS
    # ==========================================

    @classmethod
    def process_achievements(
        cls,
        player,
        database,
        player_id
    ):
        """
        Check, unlock, reward and display
        newly completed achievements.

        Returns:
            list: Newly unlocked achievement IDs.
        """

        # -------------------------
        # CHECK ACHIEVEMENTS
        # -------------------------

        newly_unlocked = (
            cls.check_achievements(
                player,
                database,
                player_id
            )
        )

        # -------------------------
        # REWARD & DISPLAY
        # -------------------------

        if newly_unlocked:
            cls.display_new_achievements(
                newly_unlocked,
                player
            )

        return newly_unlocked

    # ==========================================
    # DISPLAY ALL UNLOCKED ACHIEVEMENTS
    # ==========================================

    @classmethod
    def display_achievements(
        cls,
        database,
        player_id
    ):
        """
        Display all achievements currently
        unlocked by the player.
        """

        achievements = (
            database.get_achievements(
                player_id
            )
        )

        print("\n" + "=" * 50)
        print(" MY ACHIEVEMENTS")
        print("=" * 50)

        if not achievements:
            print(
                "\nNo achievements unlocked yet."
            )

            return

        for achievement_id, unlocked_at in achievements:

            achievement = (
                Achievement.get_achievement(
                    achievement_id
                )
            )

            if achievement is None:
                continue

            print(
                f"\n {achievement['name']}"
            )

            print(
                f"   {achievement['description']}"
            )

            print(
                f"   Reward: "
                f"KSh {achievement['reward']}"
            )

            print(
                f"   Unlocked: "
                f"{unlocked_at}"
            )

        print("\n" + "=" * 50)

    # ==========================================
    # GET ACHIEVEMENT PROGRESS
    # ==========================================

    @classmethod
    def get_progress(
        cls,
        player,
        database,
        player_id
    ):
        """
        Return achievement statistics for the
        current player.

        Useful for displaying achievement
        progress in the future.
        """

        return cls.build_statistics(
            player,
            database,
            player_id
        )