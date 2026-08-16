from models.achievement import Achievement


class AchievementManager:
    """Manage player achievements."""

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

        # Get completed trips.
        trips = database.get_trip_history(
            player_id
        )

        total_trips = len(trips)

        # Calculate total earnings.
        total_earnings = sum(
            trip[3]
            for trip in trips
        )

        # Calculate total passengers.
        total_passengers = sum(
            trip[2]
            for trip in trips
        )

        # Calculate total distance.
        #
        # The current trip database stores the
        # route name rather than distance, so
        # distance achievements will be handled
        # separately once route statistics are
        # added to the database.
        total_distance = 0

        # Count owned matatus.
        matatus = database.get_all_matatus(
            player_id
        )

        total_matatus = len(matatus)

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

    @classmethod
    def check_achievements(
        cls,
        player,
        database,
        player_id
    ):
        """
        Check all achievements and unlock
        any newly completed ones.

        Returns a list of newly unlocked
        achievement IDs.
        """

        statistics = cls.build_statistics(
            player,
            database,
            player_id
        )

        newly_unlocked = []

        for achievement_id in (
            Achievement.get_all_achievements()
        ):
            # Skip achievements that have
            # already been unlocked.
            if database.has_achievement(
                player_id,
                achievement_id
            ):
                continue

            # Check whether the requirement
            # has been completed.
            completed = (
                Achievement.check_requirement(
                    achievement_id,
                    statistics
                )
            )

            if not completed:
                continue

            # Save achievement to database.
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

    @classmethod
    def display_new_achievements(
        cls,
        achievement_ids,
        player
    ):
        """
        Display achievements that were
        newly unlocked.
        """

        if not achievement_ids:
            return

        print("\n" + "=" * 50)
        print(" ACHIEVEMENTS UNLOCKED!")
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

            # Give the player the achievement reward.
            player.earn_money(reward)

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
        """

        newly_unlocked = (
            cls.check_achievements(
                player,
                database,
                player_id
            )
        )

        if newly_unlocked:
            cls.display_new_achievements(
                newly_unlocked,
                player
            )

        return newly_unlocked