
import random


class Passenger:
    NAMES = [
        "Kevin",
        "Brian",
        "Mary",
        "Ann",
        "John",
        "Faith",
        "David",
        "Mercy",
        "Peter",
        "Lucy"
    ]

    def __init__(self, name, destination, fare):
        self.name = name
        self.destination = destination
        self.fare = fare

    def display_info(self):
        print(f"Passenger: {self.name}")
        print(f"Destination: {self.destination}")
        print(f"Fare: KSh {self.fare}")

    @classmethod
    def generate_passengers(cls, route, capacity):
        passenger_count = random.randint(
            1,
            min(capacity, len(cls.NAMES))
        )

        selected_names = random.sample(
            cls.NAMES,
            passenger_count
        )

        passengers = []

        for name in selected_names:
            passenger = cls(
                name=name,
                destination=route.destination,
                fare=route.fare
            )

            passengers.append(passenger)

        return passengers