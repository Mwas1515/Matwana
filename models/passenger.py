import random


class Passenger:
    # ==========================================
    # PASSENGER NAMES
    # ==========================================

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

    # ==========================================
    # PASSENGER TYPES
    # ==========================================

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

    # ==========================================
    # INITIALIZATION
    # ==========================================

    def __init__(
        self,
        name,
        destination,
        fare,
        passenger_type="Regular",
        patience=75
    ):
        if passenger_type not in self.PASSENGER_TYPES:
            raise ValueError(
                f"Invalid passenger type: "
                f"{passenger_type}"
            )

        if fare < 0:
            raise ValueError(
                "Passenger fare cannot be negative."
            )

        if patience < 0:
            raise ValueError(
                "Passenger patience cannot be negative."
            )

        self.name = name
        self.destination = destination
        self.fare = fare
        self.passenger_type = passenger_type
        self.patience = min(patience, 100)

    # ==========================================
    # PASSENGER INFORMATION
    # ==========================================

    def display_info(self):
        print(
            f"Passenger: "
            f"{self.name}"
        )

        print(
            f"Type: "
            f"{self.passenger_type}"
        )

        print(
            f"Destination: "
            f"{self.destination}"
        )

        print(
            f"Fare: "
            f"KSh {self.fare}"
        )

        print(
            f"Patience: "
            f"{self.patience}%"
        )

    # ==========================================
    # FARE
    # ==========================================

    def calculate_fare(self, base_fare):
        """
        Calculate the passenger's fare
        using their passenger type.
        """

        passenger_data = (
            self.PASSENGER_TYPES[
                self.passenger_type
            ]
        )

        multiplier = (
            passenger_data["fare_multiplier"]
        )

        return round(
            base_fare * multiplier
        )

    def get_fare(self):
        """Return the passenger's current fare."""

        return self.fare

    # ==========================================
    # PATIENCE
    # ==========================================

    def lose_patience(self, amount):
        """Reduce passenger patience."""

        if amount <= 0:
            return

        self.patience = max(
            0,
            self.patience - amount
        )

    def is_patient(self):
        """Check whether the passenger is still willing to ride."""

        return self.patience > 0

    def handle_trip_delay(self, delay):
        """
        Apply a delay to the passenger.

        Returns False if the passenger leaves.
        """

        self.lose_patience(delay)

        return self.is_patient()

    # ==========================================
    # PASSENGER GENERATION
    # ==========================================

    @classmethod
    def generate_passengers(
        cls,
        route,
        capacity
    ):
        """
        Generate random passengers for a route.
        """

        if capacity <= 0:
            return []

        max_passengers = min(
            capacity,
            len(cls.NAMES)
        )

        passenger_count = random.randint(
            1,
            max_passengers
        )

        selected_names = random.sample(
            cls.NAMES,
            passenger_count
        )

        passengers = []

        for name in selected_names:

            # Choose a random passenger type.
            passenger_type = random.choice(
                list(cls.PASSENGER_TYPES.keys())
            )

            passenger_data = (
                cls.PASSENGER_TYPES[
                    passenger_type
                ]
            )

            # Create passenger first.
            passenger = cls(
                name=name,
                destination=route.destination,
                fare=0,
                passenger_type=passenger_type,
                patience=passenger_data["patience"]
            )

            # Calculate fare using the
            # passenger's own fare logic.
            passenger.fare = (
                passenger.calculate_fare(
                    route.fare
                )
            )

            passengers.append(
                passenger
            )

        return passengers

    # ==========================================
    # STRING REPRESENTATION
    # ==========================================

    def __str__(self):
        return (
            f"{self.name} | "
            f"{self.passenger_type} | "
            f"{self.destination} | "
            f"KSh {self.fare} | "
            f"Patience: {self.patience}%"
        )