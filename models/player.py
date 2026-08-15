class Player:
    XP_PER_LEVEL = 100

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
            return False

        self.experience += amount

        leveled_up = False

        while self.experience >= self.XP_PER_LEVEL:
            self.experience -= self.XP_PER_LEVEL
            self.level += 1
            leveled_up = True

            print("\n" + "=" * 40)
            print("LEVEL UP!")
            print("=" * 40)
            print(
                f"Congratulations, {self.name}!"
            )
            print(
                f"You reached Level {self.level}."
            )

        return leveled_up

    def add_reputation(self, amount):
        self.reputation += amount

    def get_xp_required(self):
        return self.XP_PER_LEVEL

    def display_stats(self):
        print("\nPLAYER STATS")
        print("=" * 40)

        print(f"Driver: {self.name}")
        print(f"Level: {self.level}")
        print(
            f"Experience: "
            f"{self.experience}/"
            f"{self.XP_PER_LEVEL}"
        )
        print(f"Reputation: {self.reputation}")
        print(f"Money: KSh {self.money}")