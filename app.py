from models.player import Player
from models.matatu import Matatu
from models.route import Route
from models.passenger import Passenger
from models.trip import Trip


def choose_route(routes):
    print("\nAVAILABLE ROUTES")
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

        print(
            "Invalid choice. "
            "Please select a valid route."
        )


def main():
    player = Player("Goon")

    matatu = Matatu(
        name="Beast",
        model="Toyota Hiace"
    )

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

    print("=" * 40)
    print("WELCOME TO MATWANA")
    print("=" * 40)

    print(f"Driver: {player.name}")
    print(f"Money: KSh {player.money}")
    print(f"Level: {player.level}")
    print(f"Experience: {player.experience}")
    print(f"Reputation: {player.reputation}")

    matatu.display_info()

    selected_route = choose_route(routes)

    print("\nSELECTED ROUTE")
    selected_route.display_info()

    passengers = Passenger.generate_passengers(
        selected_route,
        matatu.capacity
    )

    print("\nPASSENGERS")

    for passenger in passengers:
        passenger.display_info()

    if not matatu.can_carry(len(passengers)):
        print("\nToo many passengers!")
        return

    print(
        f"\n{len(passengers)} passengers boarded."
    )

    trip = Trip(
        player=player,
        matatu=matatu,
        route=selected_route,
        passengers=passengers
    )

    print("\nStarting trip...")

    if trip.complete_trip():
        trip.display_summary()
    else:
        print("\nTrip could not be completed.")

    print("\nUPDATED PLAYER STATUS")
    print("=" * 40)

    print(f"Money: KSh {player.money}")
    print(f"Level: {player.level}")
    print(f"Experience: {player.experience}")
    print(f"Reputation: {player.reputation}")

    print("\nUPDATED MATATU STATUS")

    matatu.display_info()


if __name__ == "__main__":
    main()