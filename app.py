from models.player import Player
from models.matatu import Matatu
from models.route import Route
from models.passenger import Passenger
from models.trip import Trip


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

    # Select route
    selected_route = routes[0]

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

    # Selected route
    print("\n SELECTED ROUTE")
    selected_route.display_info()

    # Passenger information
    print("\n PASSENGERS")

    for passenger in passengers:
        passenger.display_info()

    # Create trip
    trip = Trip(
        player=player,
        matatu=matatu,
        route=selected_route,
        passengers=passengers
    )

    # Start trip
    print("\n Starting trip...")

    if trip.complete_trip():
        trip.display_summary()
    else:
        print("\n Trip could not be completed.")

    # Show updated player information
    print("\n UPDATED PLAYER STATUS")
    print(f" Money: KSh {player.money}")
    print(f" Level: {player.level}")
    print(f" Experience: {player.experience}")
    print(f" Reputation: {player.reputation}")

    # Show updated matatu
    matatu.display_info()


if __name__ == "__main__":
    main()