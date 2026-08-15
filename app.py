from models.player import Player
from models.matatu import Matatu
from models.route import Route
from models.passenger import Passenger
from models.trip import Trip
from models.garage import Garage
from database.database import Database


def choose_route(routes, player):
    print("\nAVAILABLE ROUTES")
    print("=" * 40)

    for index, route in enumerate(routes, start=1):
        print(f"\n{index}. {route.name}")
        print(f"   Difficulty: {route.difficulty}")
        print(f"   Distance: {route.distance} km")
        print(f"   Fare: KSh {route.fare}")

        if route.is_unlocked(player.level):
            print("   Status: UNLOCKED")
        else:
            print(
                f"   Status: LOCKED "
                f"(Requires Level {route.required_level})"
            )

    while True:
        choice = input(
            "\nChoose a route or 0 to cancel: "
        )

        if choice == "0":
            return None

        if choice.isdigit():
            choice = int(choice)

            if 1 <= choice <= len(routes):
                selected_route = routes[choice - 1]

                if not selected_route.is_unlocked(
                    player.level
                ):
                    print("\nRoute locked.")
                    print(
                        f"You need Level "
                        f"{selected_route.required_level} "
                        f"to unlock this route."
                    )
                    continue

                return selected_route

        print(
            "Invalid choice. "
            "Please select an available route."
        )


def maintenance_menu(player, matatu):
    while True:
        print("\nMAINTENANCE")
        print("=" * 40)

        print(f"Money: KSh {player.money}")
        print(
            f"Fuel: {matatu.fuel}L / "
            f"{matatu.fuel_capacity}L"
        )
        print(f"Condition: {matatu.condition}%")

        print("\n1. Refuel")
        print("2. Repair")
        print("3. Continue")

        choice = input("\nChoose an option: ")

        if choice == "1":
            try:
                litres = int(
                    input(
                        "How many litres of fuel "
                        "do you want to buy? "
                    )
                )
            except ValueError:
                print("Please enter a valid number.")
                continue

            if litres <= 0:
                print(
                    "Amount must be greater than zero."
                )
                continue

            fuel_space = (
                matatu.fuel_capacity - matatu.fuel
            )

            if fuel_space <= 0:
                print("Fuel tank is already full.")
                continue

            actual_litres = min(
                litres,
                fuel_space
            )

            cost = matatu.calculate_fuel_cost(
                actual_litres
            )

            if cost > player.money:
                print("You don't have enough money.")
                continue

            fuel_added = matatu.refuel(
                actual_litres
            )

            player.spend_money(cost)

            print(
                f"Added {fuel_added}L of fuel "
                f"for KSh {cost}."
            )

        elif choice == "2":
            try:
                amount = int(
                    input(
                        "How much should you repair? "
                    )
                )
            except ValueError:
                print("Please enter a valid number.")
                continue

            if amount <= 0:
                print(
                    "Amount must be greater than zero."
                )
                continue

            available_condition = (
                100 - matatu.condition
            )

            if available_condition <= 0:
                print(
                    "Matatu is already in "
                    "perfect condition."
                )
                continue

            actual_repair = min(
                amount,
                available_condition
            )

            cost = matatu.calculate_repair_cost(
                actual_repair
            )

            if cost > player.money:
                print("You don't have enough money.")
                continue

            repaired = matatu.repair(
                actual_repair
            )

            player.spend_money(cost)

            print(
                f"Repaired {repaired}% "
                f"for KSh {cost}."
            )

        elif choice == "3":
            break

        else:
            print("Invalid choice.")


def garage_menu(player, matatu):
    while True:
        print("\nGARAGE")
        print("=" * 40)

        print(f"Money: KSh {player.money}")

        print("\nAvailable upgrades:")
        print("1. Engine - KSh 5,000")
        print("2. Suspension - KSh 3,000")
        print("3. Seats - KSh 4,000")
        print("4. Fuel Tank - KSh 3,500")
        print("5. Comfort - KSh 2,500")
        print("6. Leave Garage")

        choice = input("\nChoose an upgrade: ")

        upgrades = {
            "1": "engine",
            "2": "suspension",
            "3": "seats",
            "4": "fuel_tank",
            "5": "comfort"
        }

        if choice in upgrades:
            Garage.upgrade_matatu(
                player,
                matatu,
                upgrades[choice]
            )

        elif choice == "6":
            break

        else:
            print("Invalid choice.")


def display_trip_history(database, player_id):
    trips = database.get_trip_history(
        player_id
    )

    print("\nTRIP HISTORY")
    print("=" * 50)

    if not trips:
        print("No trips completed yet.")
        return

    for trip in trips:
        trip_id = trip[0]
        route_name = trip[1]
        passengers = trip[2]
        earnings = trip[3]
        fuel_used = trip[4]
        event_name = trip[5]
        experience = trip[6]
        reputation = trip[7]

        print(f"\nTrip #{trip_id}")
        print(f"Route: {route_name}")
        print(f"Passengers: {passengers}")
        print(f"Earnings: KSh {earnings}")
        print(f"Fuel used: {fuel_used}L")

        if event_name:
            print(f"Event: {event_name}")

        print(f"XP earned: {experience}")
        print(f"Reputation: +{reputation}")


def display_player_stats(player):
    player.display_stats()


def display_matatu_status(matatu):
    print("\nMY MATATU")
    print("=" * 40)

    matatu.display_info()

    input("\nPress Enter to continue...")


def save_game(
    database,
    player_id,
    matatu_id,
    player,
    matatu
):
    database.save_player(
        player_id,
        player
    )

    database.save_matatu(
        matatu_id,
        matatu
    )


def start_trip(
    player,
    matatu,
    routes,
    database,
    player_id,
    matatu_id
):
    print("\nSTART TRIP")
    print("=" * 40)

    if matatu.fuel <= 0:
        print("Your matatu has no fuel.")
        print("Visit Maintenance to refuel.")
        input("\nPress Enter to continue...")
        return

    if matatu.condition <= 0:
        print("Your matatu is badly damaged.")
        print("Visit Maintenance to repair it.")
        input("\nPress Enter to continue...")
        return

    selected_route = choose_route(
        routes,
        player
    )

    if selected_route is None:
        print("\nTrip cancelled.")
        input("\nPress Enter to continue...")
        return

    print("\nSELECTED ROUTE")

    selected_route.display_info()

    passengers = Passenger.generate_passengers(
        selected_route,
        matatu.capacity
    )

    print("\nPASSENGERS")

    for passenger in passengers:
        passenger.display_info()

    if not matatu.can_carry(
        len(passengers)
    ):
        print("\nToo many passengers!")
        input("\nPress Enter to continue...")
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

        database.save_trip(
            player_id,
            trip
        )

        save_game(
            database,
            player_id,
            matatu_id,
            player,
            matatu
        )

        print("\nTrip saved to database.")

    else:
        print("\nTrip could not be completed.")

    input("\nPress Enter to continue...")


def main_menu(
    player,
    matatu,
    routes,
    database,
    player_id,
    matatu_id
):
    while True:
        print("\n" + "=" * 40)
        print("MATWANA")
        print("=" * 40)

        print(f"Driver: {player.name}")
        print(f"Money: KSh {player.money}")
        print(f"Level: {player.level}")
        print(f"Experience: {player.experience}")
        print(f"Reputation: {player.reputation}")

        print("\n1. Start Trip")
        print("2. My Matatu")
        print("3. Maintenance")
        print("4. Garage")
        print("5. Trip History")
        print("6. Player Stats")
        print("7. Exit")

        choice = input("\nChoose an option: ")

        if choice == "1":
            start_trip(
                player,
                matatu,
                routes,
                database,
                player_id,
                matatu_id
            )

        elif choice == "2":
            display_matatu_status(
                matatu
            )

        elif choice == "3":
            maintenance_menu(
                player,
                matatu
            )

            save_game(
                database,
                player_id,
                matatu_id,
                player,
                matatu
            )

            print("\nGame saved.")

        elif choice == "4":
            garage_menu(
                player,
                matatu
            )

            save_game(
                database,
                player_id,
                matatu_id,
                player,
                matatu
            )

            print("\nGame saved.")

        elif choice == "5":
            display_trip_history(
                database,
                player_id
            )

            input("\nPress Enter to continue...")

        elif choice == "6":
            display_player_stats(
                player
            )

            input("\nPress Enter to continue...")

        elif choice == "7":
            save_game(
                database,
                player_id,
                matatu_id,
                player,
                matatu
            )

            print("\nGame saved.")
            print("Thanks for playing Matwana.")

            break

        else:
            print(
                "Invalid choice. "
                "Please select 1-7."
            )


def main():
    database = Database()

    database.create_tables()

    # -------------------------
    # LOAD OR CREATE PLAYER
    # -------------------------

    player = Player("Goon")

    player_data = database.get_player(
        player.name
    )

    if player_data is None:
        player_id = database.create_player(
            player
        )

        print("\nNew player created.")

    else:
        player_id = player_data[0]

        player.name = player_data[1]
        player.money = player_data[2]
        player.level = player_data[3]
        player.experience = player_data[4]
        player.reputation = player_data[5]

        print("\nPlayer progress loaded.")

    # -------------------------
    # LOAD OR CREATE MATATU
    # -------------------------

    matatu_data = database.get_matatu(
        player_id
    )

    if matatu_data is None:
        matatu = Matatu(
            name="Beast",
            model="Toyota Hiace"
        )

        matatu_id = database.create_matatu(
            player_id,
            matatu
        )

        print("New matatu created.")

    else:
        matatu_id = matatu_data[0]

        matatu = Matatu(
            name=matatu_data[1],
            model=matatu_data[2],
            capacity=matatu_data[3]
        )

        matatu.fuel = matatu_data[4]
        matatu.fuel_capacity = matatu_data[5]
        matatu.condition = matatu_data[6]
        matatu.speed = matatu_data[7]
        matatu.comfort = matatu_data[8]

        matatu.engine_level = matatu_data[9]
        matatu.suspension_level = matatu_data[10]
        matatu.seat_level = matatu_data[11]
        matatu.fuel_tank_level = matatu_data[12]
        matatu.comfort_level = matatu_data[13]

        print("Matatu progress loaded.")

    # -------------------------
    # ROUTES
    # -------------------------

    routes = [
        Route(
            name="CBD → Eastleigh",
            start_location="Nairobi CBD",
            destination="Eastleigh",
            distance=8,
            fare=80,
            difficulty="Easy",
            required_level=1
        ),

        Route(
            name="CBD → Kasarani",
            start_location="Nairobi CBD",
            destination="Kasarani",
            distance=12,
            fare=70,
            difficulty="Easy",
            required_level=1
        ),

        Route(
            name="CBD → Rongai",
            start_location="Nairobi CBD",
            destination="Rongai",
            distance=18,
            fare=100,
            difficulty="Medium",
            required_level=2
        ),

        Route(
            name="CBD → Githurai",
            start_location="Nairobi CBD",
            destination="Githurai",
            distance=18,
            fare=100,
            difficulty="Hard",
            required_level=3
        )
    ]

    # -------------------------
    # START GAME
    # -------------------------

    main_menu(
        player,
        matatu,
        routes,
        database,
        player_id,
        matatu_id
    )


if __name__ == "__main__":
    main()