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

    PASSENGER_TYPES = {
        "Student": {
            "fare_multiplier": 0.8,
            "patience": 90
        },
        "Worker": {
            "fare_multiplier": 1.0,
            "patience": 80
        },
        "Businessperson": {
            "fare_multiplier": 1.3,
            "patience": 60
        },
        "Regular": {
            "fare_multiplier": 1.0,
            "patience": 75
        }
    }

    def __init__(
        self,
        name,
        destination,
        fare,
        passenger_type="Regular",
        patience=75
    ):
        self.name = name
        self.destination = destination
        self.fare = fare
        self.passenger_type = passenger_type
        self.patience = patience

    def display_info(self):
        print(f"Passenger: {self.name}")
        print(f"Type: {self.passenger_type}")
        print(f"Destination: {self.destination}")
        print(f"Fare: KSh {self.fare}")
        print(f"Patience: {self.patience}%")

    def calculate_fare(self, base_fare):
        passenger_data = self.PASSENGER_TYPES[
            self.passenger_type
        ]

        multiplier = passenger_data[
            "fare_multiplier"
        ]

        return round(
            base_fare * multiplier
        )

    def lose_patience(self, amount):
        self.patience = max(
            0,
            self.patience - amount
        )

    def is_patient(self):
        return self.patience > 0

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
            passenger_type = random.choice(
                list(cls.PASSENGER_TYPES.keys())
            )

            passenger_data = cls.PASSENGER_TYPES[
                passenger_type
            ]

            passenger = cls(
                name=name,
                destination=route.destination,
                fare=round(
                    route.fare
                    * passenger_data["fare_multiplier"]
                ),
                passenger_type=passenger_type,
                patience=passenger_data["patience"]
            )

            passengers.append(passenger)

        return passengers