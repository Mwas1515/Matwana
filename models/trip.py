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
        self.completed = False

    def calculate_earnings(self):
        self.earnings = sum(
            passenger.fare for passenger in self.passengers
        )

        return self.earnings

    def calculate_fuel_used(self):
        # Basic fuel calculation for now.
        # We can make this more advanced later.
        self.fuel_used = max(5, self.route.distance // 2)

        return self.fuel_used

    def complete_trip(self):
        if self.completed:
            return False

        # Check passenger capacity
        if not self.matatu.can_carry(len(self.passengers)):
            print("Too many passengers for this matatu.")
            return False

        # Calculate fuel
        self.calculate_fuel_used()

        # Check if there is enough fuel
        if self.matatu.fuel < self.fuel_used:
            print("Not enough fuel to complete this trip.")
            return False

        # Calculate earnings
        self.calculate_earnings()

        # Use fuel
        self.matatu.use_fuel(self.fuel_used)

        # Damage vehicle slightly
        self.matatu.damage(2)

        # Give player money
        self.player.earn_money(self.earnings)

        # Give XP
        self.experience_earned = 50
        self.player.add_experience(self.experience_earned)

        # Give reputation
        self.reputation_earned = 5
        self.player.add_reputation(self.reputation_earned)

        self.completed = True

        return True

    def display_summary(self):
        print("\n" + "=" * 40)
        print("TRIP COMPLETED")
        print("=" * 40)

        print(f" Route: {self.route.name}")
        print(f" Passengers: {len(self.passengers)}")
        print(f" Earnings: KSh {self.earnings}")
        print(f" Fuel used: {self.fuel_used}%")
        print(f" XP earned: {self.experience_earned}")
        print(f" Reputation: +{self.reputation_earned}")