class Player:
    BASE_XP_PER_LEVEL = 100
    LEVEL_UP_REWARD = 500

    def __init__(self, name):
        self.name = name
        self.money = 5000
        self.level = 1
        self.experience = 0
        self.reputation = 0

    # ==========================================
    # MONEY
    # ==========================================

    def earn_money(self, amount):
        if amount <= 0:
            return

        self.money += amount

    def spend_money(self, amount):
        if amount <= 0:
            return False

        if amount > self.money:
            return False

        self.money -= amount

        return True

    # ==========================================
    # EXPERIENCE / LEVEL
    # ==========================================

    def get_xp_required(self):
        """
        Return the XP required to reach the next level.

        XP requirement increases as the player levels up.
        """

        return self.BASE_XP_PER_LEVEL + (
            (self.level - 1) * 50
        )

    def add_experience(self, amount):
        """
        Add XP and automatically handle level-ups.

        Returns True if the player leveled up.
        """

        if amount <= 0:
            return False

        self.experience += amount

        leveled_up = False

        while self.experience >= self.get_xp_required():
            xp_required = self.get_xp_required()

            self.experience -= xp_required
            self.level += 1

            leveled_up = True

            # Level-up reward
            self.earn_money(
                self.LEVEL_UP_REWARD
            )

            print("\n" + "=" * 45)
            print("LEVEL UP!")
            print("=" * 45)

            print(
                f"Congratulations, {self.name}!"
            )

            print(
                f"You reached Level {self.level}!"
            )

            print(
                f"Reward: "
                f"KSh {self.LEVEL_UP_REWARD}"
            )

            print(
                f"Next level requires "
                f"{self.get_xp_required()} XP."
            )

        return leveled_up

    # ==========================================
    # REPUTATION
    # ==========================================

    def add_reputation(self, amount):
        if amount == 0:
            return

        self.reputation += amount

    # ==========================================
    # PLAYER PROGRESS
    # ==========================================

    def get_xp_progress(self):
        """
        Return current XP and required XP.
        """

        return (
            self.experience,
            self.get_xp_required()
        )

    def display_stats(self):
        print("\nPLAYER STATS")
        print("=" * 45)

        print(
            f"Driver: {self.name}"
        )

        print(
            f"Level: {self.level}"
        )

        print(
            f"Experience: "
            f"{self.experience}/"
            f"{self.get_xp_required()}"
        )

        print(
            f"Reputation: "
            f"{self.reputation}"
        )

        print(
            f"Money: "
            f"KSh {self.money}"
        )

        print(
            f"Level-up reward: "
            f"KSh {self.LEVEL_UP_REWARD}"
        )
