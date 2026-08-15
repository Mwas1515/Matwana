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

    def get_experience_required(self):
        return self.level * 100

    def add_experience(self, amount):
        self.experience += amount

        while (
            self.experience
            >= self.get_experience_required()
        ):
            self.level_up()

    def level_up(self):
        required_xp = self.get_experience_required()

        self.experience -= required_xp

        self.level += 1

        level_reward = self.level * 500

        reputation_reward = 5

        self.earn_money(level_reward)

        self.add_reputation(
            reputation_reward
        )

        print("\n" + "=" * 40)
        print("LEVEL UP!")
        print("=" * 40)

        print(
            f"Congratulations, {self.name}!"
        )

        print(
            f"You reached Level {self.level}."
        )

        print(
            f"Money reward: "
            f"KSh {level_reward}"
        )

        print(
            f"Reputation reward: "
            f"+{reputation_reward}"
        )

    def add_reputation(self, amount):
        self.reputation += amount

        if self.reputation < 0:
            self.reputation = 0

    def get_level_progress(self):
        required_xp = self.get_experience_required()

        return (
            self.experience,
            required_xp
        )

    def display_stats(self):
        current_xp, required_xp = (
            self.get_level_progress()
        )

        print("\nPLAYER STATS")
        print("=" * 40)

        print(f"Driver: {self.name}")
        print(f"Level: {self.level}")
        print(
            f"Experience: "
            f"{current_xp}/{required_xp}"
        )
        print(f"Money: KSh {self.money}")
        print(
            f"Reputation: "
            f"{self.reputation}"
        )