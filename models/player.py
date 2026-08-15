class Player:
    def __init__(self, name):
        self.name = name
        self.money = 5000

        self.level = 1
        self.experience = 0
        self.reputation = 0

    def earn_money(self, amount):
        self.money += amount

    def spend_money(self, amount):
        if amount > self.money:
            return False

        self.money -= amount
        return True

    def add_experience(self, amount):
        if amount <= 0:
            return []

        self.experience += amount

        level_ups = []

        while self.experience >= self.experience_required():
            required_xp = self.experience_required()

            self.experience -= required_xp
            self.level += 1

            level_ups.append(self.level)

        for level in level_ups:
            print("\n" + "=" * 40)
            print("LEVEL UP!")
            print("=" * 40)
            print(
                f"You reached Level {level}."
            )

        return level_ups

    def experience_required(self):
        return self.level * 100

    def add_reputation(self, amount):
        self.reputation += amount

        if self.reputation < 0:
            self.reputation = 0

    def display_stats(self):
        print("\nPLAYER STATS")
        print("=" * 40)

        print(f"Driver: {self.name}")
        print(f"Level: {self.level}")

        print(
            f"Experience: "
            f"{self.experience}/"
            f"{self.experience_required()}"
        )

        print(
            f"Reputation: "
            f"{self.reputation}"
        )

        print(
            f"Money: "
            f"KSh {self.money}"
        )