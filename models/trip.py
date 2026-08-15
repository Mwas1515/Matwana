from models.event import RandomEvent


class Trip:
    def __init__(self, player, matatu, route, passengers):
        self.player = player
        self.matatu = matatu
        self.route = route
        self.passengers = passengers

        self.earnings = 0
        self.fuel_used = 0
        self.experience_earned = 0
        self.reputation_earned = 0

        self.event = None

        self.completed = False

    def calculate_earnings(self):
        self.earnings = sum(
            passenger.fare
            for passenger in self.passengers
        )

        return self.earnings

    def calculate_fuel_used(self):
        self.fuel_used = max(
            1,
            round(self.route.distance * 0.25)
        )

        return self.fuel_used

    def apply_event(self):
        if not self.event:
            return

        RandomEvent.display_event(self.event)

        self.fuel_used += self.event["fuel_cost"]

        self.matatu.damage(
            self.event["damage"]
        )

        self.player.earn_money(
            self.event["money"]
        )

    def complete_trip(self):
        if self.completed:
            return False

        if not self.matatu.can_carry(
            len(self.passengers)
        ):
            print("\nToo many passengers for this matatu.")
            return False

        self.calculate_fuel_used()

        self.event = RandomEvent.generate_event()

        total_fuel = (
            self.fuel_used
            + self.event["fuel_cost"]
        )

        if self.matatu.fuel < total_fuel:
            print(
                "\nNot enough fuel "
                "to complete this trip."
            )
            return False

        self.apply_event()

        self.calculate_earnings()

        self.matatu.use_fuel(
            self.fuel_used
        )

        self.matatu.damage(2)

        self.player.earn_money(
            self.earnings
        )

        self.experience_earned = 50

        self.player.add_experience(
            self.experience_earned
        )

        self.reputation_earned = 5

        self.player.add_reputation(
            self.reputation_earned
        )

        self.completed = True

        return True

    def display_summary(self):
        print("\n" + "=" * 40)
        print("TRIP COMPLETED")
        print("=" * 40)

        print(f"Route: {self.route.name}")
        print(f"Passengers: {len(self.passengers)}")
        print(f"Passenger earnings: KSh {self.earnings}")
        print(f"Fuel used: {self.fuel_used}L")
        print(f"XP earned: {self.experience_earned}")
        print(f"Reputation: +{self.reputation_earned}")

        if self.event:
            print(f"Event: {self.event['name']}")