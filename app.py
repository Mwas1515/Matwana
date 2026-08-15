from models.player import Player
from models.matatu import Matatu
from models.route import Route
from models.passenger import Passenger


def main():
    # Create player
    player = Player("Goon")

    # Create matatu
    matatu = Matatu(
        name="Beast",
        model="Toyota Hiace"
    )

    # Create routes
    routes = [
        Route(
            name="CBD → Rongai",
            start_location="Nairobi CBD",
            destination="Rongai",
            distance=18,
            fare=100,
            difficulty="Medium"
        ),
        Route(
            name="CBD → Eastleigh",
            start_location="Nairobi CBD",
            destination="Eastleigh",
            distance=8,
            fare=80,
            difficulty="Easy"
        ),
        Route(
            name="CBD → Kasarani",
            start_location="Nairobi CBD",
            destination="Kasarani",
            distance=12,
            fare=70,
            difficulty="Easy"
        ),
        Route(
            name="CBD → Githurai",
            start_location="Nairobi CBD",
            destination="Githurai",
            distance=18,
            fare=100,
            difficulty="Hard"
        )
    ]

    # Create passengers
    passengers = [
        Passenger("Kevin", "Rongai", 100),
        Passenger("Brian", "Rongai", 100),
        Passenger("Mary", "Rongai", 100),
        Passenger("Ann", "Rongai", 100)
    ]

    # Welcome screen
    print("=" * 40)
    print("WELCOME TO MATWANA")
    print("=" * 40)

    print(f"Driver: {player.name}")
    print(f"Money: KSh {player.money}")
    print(f"Level: {player.level}")
    print(f"Reputation: {player.reputation}")

    # Matatu information
    matatu.display_info()

    # Available routes
    print("\n AVAILABLE ROUTES")

    for route in routes:
        route.display_info()

    # Passenger information
    print("\n PASSENGERS")

    for passenger in passengers:
        passenger.display_info()

    # Check capacity
    if matatu.can_carry(len(passengers)):
        print(f"\n {len(passengers)} passengers boarded.")
    else:
        print("\n Too many passengers!")

    # Calculate expected earnings
    total_fare = sum(passenger.fare for passenger in passengers)

    print(f"\n Expected earnings: KSh {total_fare}")


if __name__ == "__main__":
    main()