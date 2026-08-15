class DrivingStyle:
    # ==========================================
    # DRIVING STYLES
    # ==========================================

    STYLES = {
        "1": {
            "name": "Safe Driving",
            "fuel_multiplier": 0.85,
            "damage": 1,
            "earnings_multiplier": 0.95,
            "reputation": 2,
            "description": (
                "Lower fuel usage, less damage, "
                "but slightly lower earnings."
            )
        },

        "2": {
            "name": "Normal Driving",
            "fuel_multiplier": 1.0,
            "damage": 2,
            "earnings_multiplier": 1.0,
            "reputation": 1,
            "description": (
                "Balanced fuel usage, damage, "
                "and earnings."
            )
        },

        "3": {
            "name": "Aggressive Driving",
            "fuel_multiplier": 1.2,
            "damage": 4,
            "earnings_multiplier": 1.15,
            "reputation": -2,
            "description": (
                "Higher earnings, but uses more "
                "fuel and causes more damage."
            )
        }
    }

    # ==========================================
    # DISPLAY
    # ==========================================

    @classmethod
    def display_styles(cls):
        print("\nDRIVING STYLE")
        print("=" * 40)

        for key, style in cls.STYLES.items():
            print(
                f"\n{key}. "
                f"{style['name']}"
            )

            print(
                f"   {style['description']}"
            )

            print(
                f"   Fuel multiplier: "
                f"x{style['fuel_multiplier']}"
            )

            print(
                f"   Damage: "
                f"{style['damage']}"
            )

            print(
                f"   Earnings multiplier: "
                f"x{style['earnings_multiplier']}"
            )

            reputation = style["reputation"]

            if reputation >= 0:
                print(
                    f"   Reputation: "
                    f"+{reputation}"
                )

            else:
                print(
                    f"   Reputation: "
                    f"{reputation}"
                )

    # ==========================================
    # CHOOSE STYLE
    # ==========================================

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

    # ==========================================
    # GET STYLE
    # ==========================================

    @classmethod
    def get_style(cls, choice):
        """Return a driving style by its option number."""

        return cls.STYLES.get(choice)