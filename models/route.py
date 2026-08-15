class Route:
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

    def display_info(self):
        print(f"\n{self.name}")
        print(f"From: {self.start_location}")
        print(f"To: {self.destination}")
        print(f"Distance: {self.distance} km")
        print(f"Fare: KSh {self.fare}")
        print(f"Difficulty: {self.difficulty}")
        print(
            f"Required Level: "
            f"{self.required_level}"
        )