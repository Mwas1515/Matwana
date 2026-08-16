class Achievement:
    ACHIEVEMENTS = {
        "first_trip": {
            "name": "First Trip",
            "description": "Complete your first trip.",
            "type": "trips",
            "requirement": 1,
            "reward": 50
        },

        "road_warrior": {
            "name": "Road Warrior",
            "description": "Complete 10 trips.",
            "type": "trips",
            "requirement": 10,
            "reward": 200
        },

        "veteran_driver": {
            "name": "Veteran Driver",
            "description": "Complete 50 trips.",
            "type": "trips",
            "requirement": 50,
            "reward": 1000
        },

        "first_earnings": {
            "name": "First Earnings",
            "description": "Earn KSh 1,000 from trips.",
            "type": "earnings",
            "requirement": 1000,
            "reward": 100
        },

        "big_earner": {
            "name": "Big Earner",
            "description": "Earn KSh 10,000 from trips.",
            "type": "earnings",
            "requirement": 10000,
            "reward": 500
        },

        "profit_master": {
            "name": "Profit Master",
            "description": "Make KSh 5,000 in net profit.",
            "type": "profit",
            "requirement": 5000,
            "reward": 500
        },

        "people_person": {
            "name": "People Person",
            "description": "Carry 50 passengers.",
            "type": "passengers",
            "requirement": 50,
            "reward": 300
        },

        "road_explorer": {
            "name": "Road Explorer",
            "description": "Travel 100 km.",
            "type": "distance",
            "requirement": 100,
            "reward": 300
        },

        "rising_star": {
            "name": "Rising Star",
            "description": "Reach Level 5.",
            "type": "level",
            "requirement": 5,
            "reward": 500
        },

        "reputation_builder": {
            "name": "Reputation Builder",
            "description": "Reach 50 reputation.",
            "type": "reputation",
            "requirement": 50,
            "reward": 500
        },

        "fleet_owner": {
            "name": "Fleet Owner",
            "description": "Own 3 matatus.",
            "type": "matatus",
            "requirement": 3,
            "reward": 1000
        }
    }

    @classmethod
    def get_achievement(cls, achievement_id):
        """Return an achievement by its ID."""

        return cls.ACHIEVEMENTS.get(
            achievement_id
        )

    @classmethod
    def get_all_achievements(cls):
        """Return all available achievements."""

        return cls.ACHIEVEMENTS

    @classmethod
    def display_achievement(
        cls,
        achievement_id
    ):
        """Display information about an achievement."""

        achievement = cls.get_achievement(
            achievement_id
        )

        if achievement is None:
            return

        print("\n" + "=" * 40)
        print("ACHIEVEMENT")
        print("=" * 40)

        print(
            f"Name: "
            f"{achievement['name']}"
        )

        print(
            f"Description: "
            f"{achievement['description']}"
        )

        print(
            f"Reward: "
            f"KSh {achievement['reward']}"
        )

        print("=" * 40)

    @classmethod
    def check_requirement(
        cls,
        achievement_id,
        statistics
    ):
        """
        Check whether an achievement
        requirement has been completed.
        """

        achievement = cls.get_achievement(
            achievement_id
        )

        if achievement is None:
            return False

        achievement_type = achievement["type"]
        requirement = achievement["requirement"]

        current_value = statistics.get(
            achievement_type,
            0
        )

        return current_value >= requirement