import random


class RandomEvent:
    # ==========================================
    # RANDOM EVENTS
    # ==========================================

    EVENTS = [
        {
            "name": "Heavy Traffic",
            "description": (
                "You got stuck in heavy traffic."
            ),
            "fuel_cost": 5,
            "damage": 0,
            "money": 0,
            "patience_loss": 20,
            "type": "negative"
        },

        {
            "name": "Pothole",
            "description": (
                "You hit a large pothole."
            ),
            "fuel_cost": 0,
            "damage": 5,
            "money": 0,
            "patience_loss": 10,
            "type": "negative"
        },

        {
            "name": "Police Checkpoint",
            "description": (
                "You were stopped at a "
                "police checkpoint."
            ),
            "fuel_cost": 0,
            "damage": 0,
            "money": -200,
            "patience_loss": 15,
            "type": "negative"
        },

        {
            "name": "Heavy Rain",
            "description": (
                "Heavy rain slowed down the trip."
            ),
            "fuel_cost": 3,
            "damage": 2,
            "money": 0,
            "patience_loss": 15,
            "type": "negative"
        },

        {
            "name": "Lucky Passenger",
            "description": (
                "A passenger gave you a small tip."
            ),
            "fuel_cost": 0,
            "damage": 0,
            "money": 100,
            "patience_loss": 0,
            "type": "positive"
        },

        {
            "name": "Smooth Trip",
            "description": (
                "The trip went smoothly."
            ),
            "fuel_cost": 0,
            "damage": 0,
            "money": 50,
            "patience_loss": 0,
            "type": "positive"
        }
    ]

    # ==========================================
    # EVENT GENERATION
    # ==========================================

    @classmethod
    def generate_event(cls):
        """Return a random event."""

        return random.choice(cls.EVENTS)

    # ==========================================
    # EVENT INFORMATION
    # ==========================================

    @classmethod
    def get_event_type(cls, event):
        """Return the event type."""

        return event.get(
            "type",
            "neutral"
        )

    @classmethod
    def is_positive(cls, event):
        """Check whether an event is positive."""

        return cls.get_event_type(event) == "positive"

    @classmethod
    def is_negative(cls, event):
        """Check whether an event is negative."""

        return cls.get_event_type(event) == "negative"

    # ==========================================
    # EVENT DISPLAY
    # ==========================================

    @classmethod
    def display_event(cls, event):
        print("\nRANDOM EVENT")
        print("=" * 40)

        print(
            f"Event: "
            f"{event['name']}"
        )

        print(
            f"{event['description']}"
        )

        event_type = cls.get_event_type(
            event
        )

        print(
            f"Type: "
            f"{event_type.title()}"
        )

        # -------------------------
        # FUEL
        # -------------------------

        if event["fuel_cost"] > 0:
            print(
                f"Extra fuel required: "
                f"{event['fuel_cost']}L"
            )

        # -------------------------
        # DAMAGE
        # -------------------------

        if event["damage"] > 0:
            print(
                f"Matatu damage: "
                f"{event['damage']}%"
            )

        # -------------------------
        # MONEY
        # -------------------------

        if event["money"] > 0:
            print(
                f"Money gained: "
                f"KSh {event['money']}"
            )

        elif event["money"] < 0:
            print(
                f"Money lost: "
                f"KSh {abs(event['money'])}"
            )

        # -------------------------
        # PATIENCE
        # -------------------------

        if event["patience_loss"] > 0:
            print(
                f"Passenger patience lost: "
                f"{event['patience_loss']}%"
            )

