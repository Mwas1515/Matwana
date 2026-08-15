import random

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

    def get_difficulty_multiplier(self):
        difficulty = self.route.difficulty.lower()

        if difficulty == "easy":
            return 1.0

        if difficulty == "medium":
            return 1.2

        if difficulty == "hard":
            return 1.5

        return 1.0

    def calculate_earnings(self):
        base_earnings = sum(
            passenger.fare
            for passenger in self.passengers
        )

        multiplier = self.get_difficulty_multiplier()

        self.earnings = round(
            base_earnings * multiplier
        )

        return self.earnings

    def calculate_fuel_used(self):
        difficulty = self.route.difficulty.lower()

        if difficulty == "easy":
            fuel_rate = 0.20

        elif difficulty == "medium":
            fuel_rate = 0.25

        elif difficulty == "hard":
            fuel_rate = 0.30

        else:
            fuel_rate = 0.25

        self.fuel_used = max(
            1,
            round(self.route.distance * fuel_rate)
        )

        return self.fuel_used

    def calculate_damage(self):
        difficulty = self.route.difficulty.lower()

        if difficulty == "easy":
            damage = 1

        elif difficulty == "medium":
            damage = 2

        elif difficulty == "hard":
            damage = 4

        else:
            damage = 2

        return damage

    def calculate_rewards(self):
        difficulty = self.route.difficulty.lower()

        if difficulty == "easy":
            self.experience_earned = 30
            self.reputation_earned = 2

        elif difficulty == "medium":
            self.experience_earned = 50
            self.reputation_earned = 5

        elif difficulty == "hard":
            self.experience_earned = 80
            self.reputation_earned = 8

        else:
            self.experience_earned = 30
            self.reputation_earned = 2

    def apply_event(self):
        if not self.event:
            return

        RandomEvent.display_event(
            self.event
        )

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
            print(
                "\nToo many passengers "
                "for this matatu."
            )

            return False

        if self.matatu.condition <= 0:
            print(
                "\nYour matatu is too damaged "
                "to start this trip."
            )

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

            print(
                f"Fuel required: {total_fuel}L"
            )

            print(
                f"Fuel available: "
                f"{self.matatu.fuel}L"
            )

            return False

        self.apply_event()

        self.calculate_earnings()

        self.matatu.use_fuel(
            self.fuel_used
        )

        trip_damage = self.calculate_damage()

        self.matatu.damage(
            trip_damage
        )

        self.player.earn_money(
            self.earnings
        )

        self.calculate_rewards()

        self.player.add_experience(
            self.experience_earned
        )

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
        print(f"Difficulty: {self.route.difficulty}")
        print(f"Passengers: {len(self.passengers)}")

        print(
            f"Passenger earnings: "
            f"KSh {self.earnings}"
        )

        print(
            f"Fuel used: "
            f"{self.fuel_used}L"
        )

        print(
            f"XP earned: "
            f"{self.experience_earned}"
        )

        print(
            f"Reputation: "
            f"+{self.reputation_earned}"
        )

        print(
            f"Matatu condition: "
            f"{self.matatu.condition}%"
        )

        print(
            f"Remaining fuel: "
            f"{self.matatu.fuel}L"
        )

        if self.event:
            print(
                f"Event: "
                f"{self.event['name']}"
            )