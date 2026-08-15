import random


class RandomEvent:
    EVENTS = [
        {
            "name": "Heavy Traffic",
            "description": "You got stuck in heavy traffic.",
            "fuel_cost": 5,
            "damage": 0,
            "money": 0
        },
        {
            "name": "Pothole",
            "description": "You hit a large pothole.",
            "fuel_cost": 0,
            "damage": 5,
            "money": 0
        },
        {
            "name": "Police Checkpoint",
            "description": "You were stopped at a police checkpoint.",
            "fuel_cost": 0,
            "damage": 0,
            "money": -200
        },
        {
            "name": "Heavy Rain",
            "description": "Heavy rain slowed down the trip.",
            "fuel_cost": 3,
            "damage": 2,
            "money": 0
        },
        {
            "name": "Lucky Passenger",
            "description": "A passenger gave you a small tip.",
            "fuel_cost": 0,
            "damage": 0,
            "money": 100
        },
        {
            "name": "Smooth Trip",
            "description": "The trip went smoothly.",
            "fuel_cost": 0,
            "damage": 0,
            "money": 50
        }
    ]

    @classmethod
    def generate_event(cls):
        return random.choice(cls.EVENTS)

    @classmethod
    def display_event(cls, event):
        print("\nRANDOM EVENT")
        print("-" * 40)
        print(f"Event: {event['name']}")
        print(f"{event['description']}")