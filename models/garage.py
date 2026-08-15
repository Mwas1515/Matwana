class Garage:
    UPGRADE_COSTS = {
        "engine": 5000,
        "suspension": 3000,
        "seats": 4000,
        "fuel_tank": 3500,
        "comfort": 2500
    }

    @classmethod
    def upgrade_matatu(cls, player, matatu, upgrade):
        if upgrade not in cls.UPGRADE_COSTS:
            return False

        cost = cls.UPGRADE_COSTS[upgrade]

        if player.money < cost:
            print("You don't have enough money.")
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

        print(
            f"{upgrade.replace('_', ' ').title()} "
            f"upgrade purchased for KSh {cost}."
        )

        return True