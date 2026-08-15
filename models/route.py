class Route:
    def __init__(self, name, start_location, destination, distance, fare, difficulty="Easy"):
        self.name = name
        self.start_location = start_location
        self.destination = destination
        self.distance = distance
        self.fare = fare
        self.difficulty = difficulty

    def display_info(self):
        print(f"\n {self.name}")
        print(f"From: {self.start_location}")
        print(f"To: {self.destination}")
        print(f"Distance: {self.distance} km")
        print(f"Fare: KSh {self.fare}")
        print(f"Difficulty: {self.difficulty}")