```python
class Route:
    # ==========================================
    # ROUTE REWARDS
    # ==========================================

    REWARDS = {
        "Easy": {
            "experience": 20,
            "reputation": 1
        },

        "Medium": {
            "experience": 40,
            "reputation": 2
        },

        "Hard": {
            "experience": 70,
            "reputation": 3
        }
    }

    # ==========================================
    # ROUTE SETTINGS
    # ==========================================

    DIFFICULTIES = {
        "Easy",
        "Medium",
        "Hard"
    }

    def __init__(
        self,
        name,
        start_location,
        destination,
        distance,
        fare,
        difficulty="Easy",
        required_level=1
    ):
        self.name = name
        self.start_location = start_location
        self.destination = destination
        self.distance = distance
        self.fare = fare
        self.difficulty = difficulty
        self.required_level = required_level

        self.validate()

    # ==========================================
    # VALIDATION
    # ==========================================

    def validate(self):
        """Validate route information."""

        if self.distance <= 0:
            raise ValueError(
                "Route distance must be greater than 0."
            )

        if self.fare <= 0:
            raise ValueError(
                "Route fare must be greater than 0."
            )

        if self.required_level < 1:
            raise ValueError(
                "Required level must be at least 1."
            )

        if self.difficulty not in self.DIFFICULTIES:
            raise ValueError(
                f"Invalid difficulty: "
                f"{self.difficulty}"
            )

    # ==========================================
    # UNLOCK SYSTEM
    # ==========================================

    def is_unlocked(self, player_level):
        """Check whether the player can access the route."""

        return player_level >= self.required_level

    def get_unlock_message(self, player_level):
        """Return a message explaining route access."""

        if self.is_unlocked(player_level):
            return "UNLOCKED"

        levels_needed = (
            self.required_level - player_level
        )

        return (
            f"LOCKED - "
            f"{levels_needed} more level"
            f"{'s' if levels_needed != 1 else ''} needed"
        )

    # ==========================================
    # REWARDS
    # ==========================================

    def get_rewards(self):
        """Return all rewards for this route."""

        return self.REWARDS.get(
            self.difficulty,
            self.REWARDS["Easy"]
        )

    def get_experience_reward(self):
        return self.get_rewards()["experience"]

    def get_reputation_reward(self):
        return self.get_rewards()["reputation"]

    # ==========================================
    # ROUTE INFORMATION
    # ==========================================

    def get_estimated_earnings(
        self,
        passenger_count
    ):
        """
        Estimate earnings based on the number
        of passengers.
        """

        if passenger_count <= 0:
            return 0

        return passenger_count * self.fare

    def get_difficulty_multiplier(self):
        """Return the earnings multiplier."""

        multipliers = {
            "Easy": 1.0,
            "Medium": 1.2,
            "Hard": 1.5
        }

        return multipliers.get(
            self.difficulty,
            1.0
        )

    def display_info(self):
        print(f"\n{self.name}")
        print("=" * 40)

        print(
            f"From: "
            f"{self.start_location}"
        )

        print(
            f"To: "
            f"{self.destination}"
        )

        print(
            f"Distance: "
            f"{self.distance} km"
        )

        print(
            f"Fare per passenger: "
            f"KSh {self.fare}"
        )

        print(
            f"Difficulty: "
            f"{self.difficulty}"
        )

        print(
            f"Required Level: "
            f"{self.required_level}"
        )

        print(
            f"XP Reward: "
            f"{self.get_experience_reward()}"
        )

        print(
            f"Reputation: +"
            f"{self.get_reputation_reward()}"
        )

        print(
            f"Earnings Multiplier: "
            f"x{self.get_difficulty_multiplier()}"
        )

    def __str__(self):
        return (
            f"{self.name} | "
            f"{self.distance} km | "
            f"{self.difficulty} | "
            f"KSh {self.fare}"
        )
```
