from models.event import RandomEvent
from models.driving import DrivingStyle


class Trip:
    def __init__(self, player, matatu, route, passengers):
        self.player = player
        self.matatu = matatu
        self.route = route
        self.passengers = passengers

        # -------------------------
        # FINANCIAL DATA
        # -------------------------

        self.earnings = 0
        self.base_earnings = 0
        self.difficulty_bonus = 0
        self.driving_bonus = 0
        self.event_money = 0
        self.fuel_cost = 0
        self.net_profit = 0

        # -------------------------
        # TRIP DATA
        # -------------------------

        self.fuel_used = 0
        self.experience_earned = 0
        self.reputation_earned = 0

        self.event = None
        self.driving_style = None

        self.completed = False

    # ==========================================
    # DIFFICULTY
    # ==========================================

    def get_difficulty_multiplier(self):
        difficulty = self.route.difficulty.lower()

        if difficulty == "easy":
            return 1.0

        if difficulty == "medium":
            return 1.2

        if difficulty == "hard":
            return 1.5

        return 1.0

    # ==========================================
    # EARNINGS
    # ==========================================

    def calculate_earnings(self):
        # Base earnings from passengers.
        self.base_earnings = sum(
            passenger.fare
            for passenger in self.passengers
        )

        # Apply route difficulty multiplier.
        difficulty_multiplier = (
            self.get_difficulty_multiplier()
        )

        difficulty_earnings = (
            self.base_earnings
            * difficulty_multiplier
        )

        self.difficulty_bonus = round(
            difficulty_earnings
            - self.base_earnings
        )

        earnings = difficulty_earnings

        # Apply driving style multiplier.
        if self.driving_style:
            driving_multiplier = (
                self.driving_style[
                    "earnings_multiplier"
                ]
            )

            before_driving = earnings

            earnings *= driving_multiplier

            self.driving_bonus = round(
                earnings - before_driving
            )

        self.earnings = round(
            earnings
        )

        return self.earnings

    # ==========================================
    # FUEL
    # ==========================================

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

        # Apply driving style fuel multiplier.
        if self.driving_style:
            driving_multiplier = (
                self.driving_style[
                    "fuel_multiplier"
                ]
            )

            base_fuel = round(
                base_fuel
                * driving_multiplier
            )

        # Apply matatu engine efficiency.
        engine_efficiency = (
            self.matatu.get_fuel_efficiency()
        )

        self.fuel_used = max(
            1,
            round(
                base_fuel
                * engine_efficiency
            )
        )

        return self.fuel_used

    # ==========================================
    # DAMAGE
    # ==========================================

    def calculate_damage(self):
        if self.driving_style:
            base_damage = (
                self.driving_style["damage"]
            )

        else:
            difficulty = (
                self.route.difficulty.lower()
            )

            if difficulty == "easy":
                base_damage = 1

            elif difficulty == "medium":
                base_damage = 2

            elif difficulty == "hard":
                base_damage = 4

            else:
                base_damage = 2

        damage_reduction = (
            self.matatu.get_damage_reduction()
        )

        final_damage = round(
            base_damage
            * (1 - damage_reduction)
        )

        return max(
            0,
            final_damage
        )

    # ==========================================
    # REWARDS
    # ==========================================

    def calculate_rewards(self):
        difficulty = (
            self.route.difficulty.lower()
        )

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

    # ==========================================
    # DRIVING REPUTATION
    # ==========================================

    def calculate_driving_reputation(self):
        if not self.driving_style:
            return 0

        return self.driving_style["reputation"]

    # ==========================================
    # DRIVING STYLE
    # ==========================================

    def choose_driving_style(self):
        self.driving_style = (
            DrivingStyle.choose_style()
        )

        print(
            f"\nSelected: "
            f"{self.driving_style['name']}"
        )

    # ==========================================
    # RANDOM EVENT
    # ==========================================

    def apply_event(self):
        if not self.event:
            return

        RandomEvent.display_event(
            self.event
        )

        # -------------------------
        # EVENT FUEL
        # -------------------------

        event_fuel = (
            self.event["fuel_cost"]
        )

        engine_efficiency = (
            self.matatu.get_fuel_efficiency()
        )

        reduced_event_fuel = round(
            event_fuel
            * engine_efficiency
        )

        self.fuel_used += (
            reduced_event_fuel
        )

        # -------------------------
        # EVENT DAMAGE
        # -------------------------

        event_damage = (
            self.event["damage"]
        )

        damage_reduction = (
            self.matatu.get_damage_reduction()
        )

        reduced_event_damage = round(
            event_damage
            * (1 - damage_reduction)
        )

        self.matatu.damage(
            reduced_event_damage
        )

        # -------------------------
        # EVENT MONEY
        # -------------------------

        self.event_money = (
            self.event["money"]
        )

        self.player.earn_money(
            self.event_money
        )

    # ==========================================
    # PASSENGER PATIENCE
    # ==========================================

    def handle_passenger_patience(self):
        if not self.event:
            return

        delay = self.event.get(
            "patience_loss",
            0
        )

        if delay <= 0:
            return

        comfort_reduction = (
            self.matatu.get_patience_reduction()
        )

        reduced_delay = round(
            delay
            * (1 - comfort_reduction)
        )

        if reduced_delay <= 0:
            return

        remaining_passengers = []

        for passenger in self.passengers:
            still_riding = (
                passenger.handle_trip_delay(
                    reduced_delay
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

    # ==========================================
    # COMPLETE TRIP
    # ==========================================

    def complete_trip(self):
        if self.completed:
            return False

        # Check passenger capacity.
        if not self.matatu.can_carry(
            len(self.passengers)
        ):
            print(
                "\nToo many passengers "
                "for this matatu."
            )

            return False

        # Check matatu condition.
        if self.matatu.condition <= 0:
            print(
                "\nYour matatu is too damaged "
                "to start this trip."
            )

            return False

        # -------------------------
        # DRIVING STYLE
        # -------------------------

        self.choose_driving_style()

        # -------------------------
        # BASE FUEL
        # -------------------------

        self.calculate_fuel_used()

        # -------------------------
        # RANDOM EVENT
        # -------------------------

        self.event = (
            RandomEvent.generate_event()
        )

        event_fuel = (
            self.event["fuel_cost"]
        )

        engine_efficiency = (
            self.matatu.get_fuel_efficiency()
        )

        reduced_event_fuel = round(
            event_fuel
            * engine_efficiency
        )

        total_fuel = (
            self.fuel_used
            + reduced_event_fuel
        )

        # -------------------------
        # FUEL CHECK
        # -------------------------

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

        # -------------------------
        # APPLY EVENT
        # -------------------------

        self.apply_event()

        # -------------------------
        # PASSENGER PATIENCE
        # -------------------------

        self.handle_passenger_patience()

        # -------------------------
        # EARNINGS
        # -------------------------

        self.calculate_earnings()

        # -------------------------
        # FUEL CONSUMPTION
        # -------------------------

        self.matatu.use_fuel(
            self.fuel_used
        )

        event_fuel_used = (
            reduced_event_fuel
        )

        self.matatu.use_fuel(
            event_fuel_used
        )

        # -------------------------
        # FUEL COST
        # -------------------------

        self.fuel_cost = (
            self.matatu.calculate_fuel_cost(
                self.fuel_used
                + event_fuel_used
            )
        )

        # -------------------------
        # DAMAGE
        # -------------------------

        trip_damage = (
            self.calculate_damage()
        )

        self.matatu.damage(
            trip_damage
        )

        # -------------------------
        # PLAYER MONEY
        # -------------------------

        self.player.earn_money(
            self.earnings
        )

        # -------------------------
        # XP & REPUTATION
        # -------------------------

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

        # -------------------------
        # NET PROFIT
        # -------------------------

        total_income = (
            self.earnings
            + self.event_money
        )

        self.net_profit = (
            total_income
            - self.fuel_cost
        )

        # -------------------------
        # COMPLETE
        # -------------------------

        self.completed = True

        return True

    # ==========================================
    # TRIP SUMMARY
    # ==========================================

    def display_summary(self):
        print("\n" + "=" * 40)
        print("TRIP COMPLETED")
        print("=" * 40)

        print(
            f"Route: "
            f"{self.route.name}"
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

        # -------------------------
        # FINANCIAL SUMMARY
        # -------------------------

        print("\n" + "-" * 40)
        print("TRIP FINANCIAL SUMMARY")
        print("-" * 40)

        print(
            f"Base passenger fares: "
            f"KSh {self.base_earnings}"
        )

        print(
            f"Difficulty bonus: "
            f"+KSh {self.difficulty_bonus}"
        )

        print(
            f"Driving style bonus: "
            f"+KSh {self.driving_bonus}"
        )

        if self.event_money > 0:
            print(
                f"Random event bonus: "
                f"+KSh {self.event_money}"
            )

        elif self.event_money < 0:
            print(
                f"Random event penalty: "
                f"-KSh {abs(self.event_money)}"
            )

        print("-" * 40)

        print(
            f"Trip earnings: "
            f"KSh {self.earnings}"
        )

        print(
            f"Fuel cost: "
            f"KSh {self.fuel_cost}"
        )

        print(
            f"Net profit: "
            f"KSh {self.net_profit}"
        )

        # -------------------------
        # PROGRESSION
        # -------------------------

        print("\n" + "-" * 40)
        print("PROGRESSION")
        print("-" * 40)

        print(
            f"XP earned: "
            f"{self.experience_earned}"
        )

        print(
            f"Reputation: "
            f"+{self.reputation_earned}"
        )

        # -------------------------
        # MATATU STATUS
        # -------------------------

        print("\n" + "-" * 40)
        print("MATATU STATUS")
        print("-" * 40)

        print(
            f"Matatu condition: "
            f"{self.matatu.condition}%"
        )

        print(
            f"Remaining fuel: "
            f"{self.matatu.fuel}L"
        )

        # -------------------------
        # EVENT
        # -------------------------

        if self.event:
            print("\n" + "-" * 40)

            print(
                f"Event: "
                f"{self.event['name']}"
            )

        print("\n" + "=" * 40)