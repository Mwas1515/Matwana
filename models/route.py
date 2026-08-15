class Route:
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

    def is_unlocked(self, player_level):
        return player_level >= self.required_level

    def get_experience_reward(self):
        reward = self.REWARDS.get(
            self.difficulty,
            self.REWARDS["Easy"]
        )

        return reward["experience"]

    def get_reputation_reward(self):
        reward = self.REWARDS.get(
            self.difficulty,
            self.REWARDS["Easy"]
        )

        return reward["reputation"]

    def display_info(self):
        print(f"\n{self.name}")
        print(f"From: {self.start_location}")
        print(f"To: {self.destination}")
        print(f"Distance: {self.distance} km")
        print(f"Fare: KSh {self.fare}")
        print(f"Difficulty: {self.difficulty}")
        print(
            f"XP Reward: "
            f"{self.get_experience_reward()}"
        )
        print(
            f"Reputation: +"
            f"{self.get_reputation_reward()}"
        )