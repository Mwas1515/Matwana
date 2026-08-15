class Passenger:
    def __init__(self, name, destination, fare):
        self.name = name
        self.destination = destination
        self.fare = fare

    def display_info(self):
        print(f" {self.name}")
        print(f"Destination: {self.destination}")
        print(f"Fare: KSh {self.fare}")