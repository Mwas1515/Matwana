class DrivingStyle:
    STYLES = {
        "1": {
            "name": "Safe Driving",
            "fuel_multiplier": 0.85,
            "damage": 1,
            "earnings_multiplier": 0.95,
            "reputation": 2
        },
        "2": {
            "name": "Normal Driving",
            "fuel_multiplier": 1.0,
            "damage": 2,
            "earnings_multiplier": 1.0,
            "reputation": 1
        },
        "3": {
            "name": "Aggressive Driving",
            "fuel_multiplier": 1.2,
            "damage": 4,
            "earnings_multiplier": 1.15,
            "reputation": -2
        }
    }

    @classmethod
    def display_styles(cls):
        print("\nDRIVING STYLE")
        print("=" * 40)

        print("\n1. Safe Driving")
        print("   Lower fuel usage")
        print("   Less matatu damage")
        print("   Slightly lower earnings")
        print("   Reputation: +2")

        print("\n2. Normal Driving")
        print("   Balanced fuel usage")
        print("   Balanced damage")
        print("   Normal earnings")
        print("   Reputation: +1")

        print("\n3. Aggressive Driving")
        print("   Higher fuel usage")
        print("   More matatu damage")
        print("   Higher earnings")
        print("   Reputation: -2")

    @classmethod
    def choose_style(cls):
        cls.display_styles()

        while True:
            choice = input(
                "\nChoose driving style: "
            )

            if choice in cls.STYLES:
                return cls.STYLES[choice]

            print(
                "Invalid choice. "
                "Please choose 1, 2, or 3."
            )