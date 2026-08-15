from models.event import RandomEvent
from models.driving import DrivingStyle


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
        self.driving_style = None

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

        difficulty_multiplier = (
            self.get_difficulty_multiplier()
        )

        earnings = (
            base_earnings
            * difficulty_multiplier
        )

        if self.driving_style:
            earnings *= (
                self.driving_style[
                    "earnings_multiplier"
                ]
            )

        self.earnings = round(
            earnings
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

        base_fuel = max(
            1,
            round(
                self.route.distance * fuel_rate
            )
        )

        if self.driving_style:
            multiplier = (
                self.driving_style[
                    "fuel_multiplier"
                ]
            )

            self.fuel_used = max(
                1,
                round(
                    base_fuel * multiplier
                )
            )

        else:
            self.fuel_used = base_fuel

        return self.fuel_used

    def calculate_damage(self):
        if self.driving_style:
            return self.driving_style["damage"]

        difficulty = self.route.difficulty.lower()

        if difficulty == "easy":
            return 1

        elif difficulty == "medium":
            return 2

        elif difficulty == "hard":
            return 4

        return 2

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

    def calculate_driving_reputation(self):
        if not self.driving_style:
            return 0

        return self.driving_style["reputation"]

    def choose_driving_style(self):
        self.driving_style = (
            DrivingStyle.choose_style()
        )

        print(
            f"\nSelected: "
            f"{self.driving_style['name']}"
        )

    def apply_event(self):
        if not self.event:
            return

        RandomEvent.display_event(
            self.event
        )

        self.fuel_used += (
            self.event["fuel_cost"]
        )

        self.matatu.damage(
            self.event["damage"]
        )

        self.player.earn_money(
            self.event["money"]
        )

    def handle_passenger_patience(self):
        if not self.event:
            return

        delay = self.event.get(
            "patience_loss",
            0
        )

        if delay <= 0:
            return

        remaining_passengers = []

        for passenger in self.passengers:
            still_riding = (
                passenger.handle_trip_delay(
                    delay
                )
            )

            if still_riding:
                remaining_passengers.append(
                    passenger
                )

            else:
                print(
                    f"\n{passenger.name} "
                    f"left the matatu because "
                    f"of the delay."
                )

        self.passengers = (
            remaining_passengers
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

        self.choose_driving_style()

        self.calculate_fuel_used()

        self.event = (
            RandomEvent.generate_event()
        )

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
                f"Fuel required: "
                f"{total_fuel}L"
            )

            print(
                f"Fuel available: "
                f"{self.matatu.fuel}L"
            )

            return False

        self.apply_event()

        self.handle_passenger_patience()

        self.calculate_earnings()

        self.matatu.use_fuel(
            self.fuel_used
        )

        trip_damage = (
            self.calculate_damage()
        )

        self.matatu.damage(
            trip_damage
        )

        self.player.earn_money(
            self.earnings
        )

        self.calculate_rewards()

        driving_reputation = (
            self.calculate_driving_reputation()
        )

        self.reputation_earned += (
            driving_reputation
        )

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

        print(
            f"Route: {self.route.name}"
        )

        print(
            f"Difficulty: "
            f"{self.route.difficulty}"
        )

        if self.driving_style:
            print(
                f"Driving Style: "
                f"{self.driving_style['name']}"
            )

        print(
            f"Passengers remaining: "
            f"{len(self.passengers)}"
        )

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