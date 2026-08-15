class Garage:
    MAX_LEVEL = 5

    BASE_COSTS = {
        "engine": 5000,
        "suspension": 3000,
        "seats": 4000,
        "fuel_tank": 3500,
        "comfort": 2500
    }

    @classmethod
    def get_upgrade_level(cls, matatu, upgrade):
        level_attributes = {
            "engine": "engine_level",
            "suspension": "suspension_level",
            "seats": "seat_level",
            "fuel_tank": "fuel_tank_level",
            "comfort": "comfort_level"
        }

        attribute = level_attributes.get(upgrade)

        if attribute is None:
            return None

        return getattr(matatu, attribute)

    @classmethod
    def get_upgrade_cost(cls, matatu, upgrade):
        if upgrade not in cls.BASE_COSTS:
            return None

        current_level = cls.get_upgrade_level(
            matatu,
            upgrade
        )

        if current_level is None:
            return None

        if current_level >= cls.MAX_LEVEL:
            return None

        base_cost = cls.BASE_COSTS[upgrade]

        cost_multiplier = 1.5 ** (
            current_level - 1
        )

        return round(
            base_cost * cost_multiplier
        )

    @classmethod
    def can_upgrade(cls, matatu, upgrade):
        level = cls.get_upgrade_level(
            matatu,
            upgrade
        )

        if level is None:
            return False

        return level < cls.MAX_LEVEL

    @classmethod
    def upgrade_matatu(
        cls,
        player,
        matatu,
        upgrade
    ):
        if upgrade not in cls.BASE_COSTS:
            print("Invalid upgrade.")
            return False

        current_level = cls.get_upgrade_level(
            matatu,
            upgrade
        )

        if current_level >= cls.MAX_LEVEL:
            print(
                f"{upgrade.replace('_', ' ').title()} "
                f"is already at maximum level."
            )

            return False

        cost = cls.get_upgrade_cost(
            matatu,
            upgrade
        )

        if cost is None:
            print("Unable to calculate upgrade cost.")
            return False

        if player.money < cost:
            print(
                f"You don't have enough money."
            )

            print(
                f"Required: KSh {cost}"
            )

            print(
                f"Available: KSh {player.money}"
            )

            return False

        if upgrade == "engine":
            matatu.upgrade_engine()

        elif upgrade == "suspension":
            matatu.upgrade_suspension()

        elif upgrade == "seats":
            matatu.upgrade_seats()

        elif upgrade == "fuel_tank":
            matatu.upgrade_fuel_tank()

        elif upgrade == "comfort":
            matatu.upgrade_comfort()

        player.spend_money(cost)

        new_level = cls.get_upgrade_level(
            matatu,
            upgrade
        )

        print(
            f"\n{upgrade.replace('_', ' ').title()} "
            f"upgraded successfully!"
        )

        print(
            f"Level: "
            f"{current_level} -> {new_level}"
        )

        print(
            f"Cost: KSh {cost}"
        )

        return True

    @classmethod
    def display_upgrades(cls, matatu):
        print("\nGARAGE UPGRADES")
        print("=" * 50)

        upgrades = [
            ("engine", "Engine"),
            ("suspension", "Suspension"),
            ("seats", "Seats"),
            ("fuel_tank", "Fuel Tank"),
            ("comfort", "Comfort")
        ]

        for upgrade, display_name in upgrades:
            level = cls.get_upgrade_level(
                matatu,
                upgrade
            )

            cost = cls.get_upgrade_cost(
                matatu,
                upgrade
            )

            print(
                f"\n{display_name}"
            )

            print(
                f"Level: "
                f"{level}/{cls.MAX_LEVEL}"
            )

            if cost is None:
                print("Status: MAX LEVEL")

            else:
                print(
                    f"Upgrade cost: "
                    f"KSh {cost}"
                )