from models.player import Player
from models.matatu import Matatu
from models.route import Route
from models.passenger import Passenger
from models.trip import Trip


def choose_route(routes):
    print("\n AVAILABLE ROUTES")
    print("=" * 40)

    for index, route in enumerate(routes, start=1):
        print(
            f"{index}. {route.name} "
            f"- KSh {route.fare} "
            f"- {route.distance} km"
        )

    while True:
        choice = input("\nChoose a route: ")

        if choice.isdigit():
            choice = int(choice)

            if 1 <= choice <= len(routes):
                return routes[choice - 1]

        print(" Invalid choice. Please select a valid route.")


def create_passengers(route, count=4):
    passengers = []

    for i in range(1, count + 1):
        passengers.append(
            Passenger(
                name=f"Passenger {i}",
                destination=route.destination,
                fare=route.fare
            )
        )

    return passengers


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

    # Choose route
    selected_route = choose_route(routes)

    print("\n SELECTED ROUTE")
    selected_route.display_info()

    # Create passengers based on selected route
    passengers = create_passengers(selected_route)

    print("\n PASSENGERS")

    for passenger in passengers:
        passenger.display_info()

    # Check capacity
    if not matatu.can_carry(len(passengers)):
        print("\n Too many passengers!")
        return

    print(f"\n {len(passengers)} passengers boarded.")

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

    # Updated player information
    print("\n UPDATED PLAYER STATUS")
    print(f"Money: KSh {player.money}")
    print(f"Level: {player.level}")
    print(f"Experience: {player.experience}")
    print(f" Reputation: {player.reputation}")

    # Updated matatu information
    matatu.display_info()


if __name__ == "__main__":
    main()