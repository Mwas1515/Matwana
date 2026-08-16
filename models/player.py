class Player:
    """Represent the player and manage progression."""

    BASE_XP_PER_LEVEL = 100
    XP_INCREASE_PER_LEVEL = 50
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
        """Add money to the player's balance."""

        if amount <= 0:
            return False

        self.money += amount

        return True

    def spend_money(self, amount):
        """Spend money if the player can afford it."""

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

        XP requirement increases by 50 for every
        level reached.
        """

        return (
            self.BASE_XP_PER_LEVEL
            + (
                (self.level - 1)
                * self.XP_INCREASE_PER_LEVEL
            )
        )

    def add_experience(self, amount):
        """
        Add XP and automatically process level-ups.

        Returns a list of levels reached.
        """

        if amount <= 0:
            return []

        self.experience += amount

        levels_gained = []

        while self.experience >= self.get_xp_required():
            xp_required = self.get_xp_required()

            self.experience -= xp_required

            self.level += 1

            levels_gained.append(
                self.level
            )

            # Level-up reward.
            self.earn_money(
                self.LEVEL_UP_REWARD
            )

            print("\n" + "=" * 45)
            print("LEVEL UP!")
            print("=" * 45)

            print(
                f"Congratulations, "
                f"{self.name}!"
            )

            print(
                f"You reached "
                f"Level {self.level}!"
            )

            print(
                f"Reward: "
                f"KSh {self.LEVEL_UP_REWARD}"
            )

            print(
                f"Next level requires "
                f"{self.get_xp_required()} XP."
            )

        return levels_gained

    # ==========================================
    # REPUTATION
    # ==========================================

    def add_reputation(self, amount):
        """
        Add or remove reputation.

        Reputation cannot fall below zero.
        """

        self.reputation += amount

        if self.reputation < 0:
            self.reputation = 0

        return self.reputation

    # ==========================================
    # PLAYER PROGRESS
    # ==========================================

    def get_xp_progress(self):
        """
        Return current XP and XP required
        for the next level.
        """

        return (
            self.experience,
            self.get_xp_required()
        )

    def get_xp_percentage(self):
        """Return XP progress as a percentage."""

        required = self.get_xp_required()

        if required <= 0:
            return 0

        percentage = (
            self.experience
            / required
        ) * 100

        return min(
            percentage,
            100
        )

    # ==========================================
    # DISPLAY
    # ==========================================

    def display_stats(self):
        """Display the player's current statistics."""

        current_xp, required_xp = (
            self.get_xp_progress()
        )

        percentage = (
            self.get_xp_percentage()
        )

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
            f"{current_xp}/"
            f"{required_xp}"
        )

        print(
            f"XP Progress: "
            f"{percentage:.1f}%"
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