from models.player import Player
from models.matatu import Matatu
from models.route import Route
from models.passenger import Passenger
from models.trip import Trip
from models.garage import Garage
from models.matatu_shop import MatatuShop
from database.database import Database


# ==========================================
# MATATU HELPERS
# ==========================================

def create_matatu_from_data(matatu_data):
    """Create a Matatu object from database data."""

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

    return matatu


# ==========================================
# ROUTE MENU
# ==========================================

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


# ==========================================
# MAINTENANCE
# ==========================================

def maintenance_menu(player, matatu):
    while True:
        print("\nMAINTENANCE")
        print("=" * 40)

        print(
            f"Money: KSh {player.money}"
        )

        print(
            f"Fuel: "
            f"{matatu.fuel:g}L / "
            f"{matatu.fuel_capacity:g}L"
        )

        print(
            f"Condition: "
            f"{matatu.condition:g}%"
        )

        print("\n1. Refuel")
        print("2. Repair")
        print("3. Continue")

        choice = input(
            "\nChoose an option: "
        )

        if choice == "1":

            try:
                litres = int(
                    input(
                        "How many litres of fuel "
                        "do you want to buy? "
                    )
                )

            except ValueError:
                print(
                    "Please enter a valid number."
                )

                continue

            if litres <= 0:
                print(
                    "Amount must be greater than zero."
                )

                continue

            fuel_space = (
                matatu.fuel_capacity
                - matatu.fuel
            )

            if fuel_space <= 0:
                print(
                    "Fuel tank is already full."
                )

                continue

            actual_litres = min(
                litres,
                fuel_space
            )

            cost = matatu.calculate_fuel_cost(
                actual_litres
            )

            if cost > player.money:
                print(
                    "You don't have enough money."
                )

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
                print(
                    "Please enter a valid number."
                )

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
                print(
                    "You don't have enough money."
                )

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


# ==========================================
# GARAGE
# ==========================================

def garage_menu(player, matatu):
    while True:
        print("\nGARAGE")
        print("=" * 40)

        print(
            f"Money: KSh {player.money}"
        )

        Garage.display_upgrades(matatu)

        print("\n6. Leave Garage")

        choice = input(
            "\nChoose an upgrade: "
        )

        upgrades = {
            "1": "engine",
            "2": "suspension",
            "3": "seats",
            "4": "fuel_tank",
            "5": "comfort"
        }

        if choice in upgrades:
            upgrade = upgrades[choice]

            Garage.upgrade_matatu(
                player,
                matatu,
                upgrade
            )

        elif choice == "6":
            break

        else:
            print("Invalid choice.")


# ==========================================
# MATATU SHOP
# ==========================================

def matatu_shop_menu(
    player,
    database,
    player_id
):
    while True:
        owned_matatus = database.get_all_matatus(
            player_id
        )

        owned_models = [
            matatu_data[2]
            for matatu_data in owned_matatus
        ]

        print("\nMATATU SHOP")
        print("=" * 50)

        MatatuShop.display_shop(
            player,
            owned_models
        )

        print("\n0. Leave Shop")

        choice = input(
            "\nChoose a matatu: "
        )

        if choice == "0":
            break

        if not choice.isdigit():
            print(
                "\nPlease enter a valid number."
            )

            continue

        choice = int(choice)

        selected = MatatuShop.get_matatu_by_index(
            choice
        )

        if selected is None:
            print(
                "\nInvalid choice."
            )

            continue

        key, shop_matatu = selected

        if shop_matatu["model"] in owned_models:
            print(
                "\nYou already own this matatu."
            )

            input(
                "\nPress Enter to continue..."
            )

            continue

        price = shop_matatu["price"]

        if player.money < price:
            print(
                "\nYou don't have enough money."
            )

            print(
                f"Required: KSh {price}"
            )

            print(
                f"Your money: KSh {player.money}"
            )

            input(
                "\nPress Enter to continue..."
            )

            continue

        print("\nPURCHASE")
        print("=" * 40)

        print(
            f"Matatu: "
            f"{shop_matatu['name']}"
        )

        print(
            f"Model: "
            f"{shop_matatu['model']}"
        )

        print(
            f"Price: "
            f"KSh {price}"
        )

        confirm = input(
            "\nBuy this matatu? (y/n): "
        ).lower()

        if confirm != "y":
            print(
                "\nPurchase cancelled."
            )

            continue

        new_matatu = Matatu(
            name=shop_matatu["name"],
            model=shop_matatu["model"],
            capacity=shop_matatu["capacity"]
        )

        new_matatu.fuel_capacity = (
            shop_matatu["fuel_capacity"]
        )

        new_matatu.fuel = (
            shop_matatu["fuel_capacity"]
        )

        new_matatu.speed = (
            shop_matatu["speed"]
        )

        new_matatu.comfort = (
            shop_matatu["comfort"]
        )

        player.spend_money(price)

        database.create_matatu(
            player_id,
            new_matatu,
            active=False
        )

        database.save_player(
            player_id,
            player
        )

        print("\n" + "=" * 40)
        print("PURCHASE SUCCESSFUL")
        print("=" * 40)

        print(
            f"You bought the "
            f"{new_matatu.name}!"
        )

        print(
            f"Money remaining: "
            f"KSh {player.money}"
        )

        input(
            "\nPress Enter to continue..."
        )


# ==========================================
# MY MATATUS
# ==========================================

def my_matatus_menu(
    database,
    player_id,
    player,
    current_matatu_id
):
    """
    Display all owned matatus.

    The player can select a matatu,
    switch the active vehicle, or go back.
    """

    while True:
        matatus = database.get_all_matatus(
            player_id
        )

        print("\nMY MATATUS")
        print("=" * 40)

        print(
            f"Money: KSh {player.money}"
        )

        if not matatus:
            print(
                "\nYou don't own any matatus."
            )

            print("\n1. Back")

            choice = input(
                "\nChoose an option: "
            )

            if choice == "1":
                return current_matatu_id

            print(
                "\nInvalid choice."
            )

            continue

        # ----------------------------------
        # DISPLAY OWNED MATATUS
        # ----------------------------------

        for index, matatu_data in enumerate(
            matatus,
            start=1
        ):
            matatu_id = matatu_data[0]
            name = matatu_data[1]
            model = matatu_data[2]
            capacity = matatu_data[3]
            fuel = matatu_data[4]
            fuel_capacity = matatu_data[5]
            condition = matatu_data[6]
            active = matatu_data[14]

            status = (
                "ACTIVE"
                if active
                else "Owned"
            )

            print(
                f"\n{index}. "
                f"{name} - {model}"
            )

            print(
                f"   Capacity: "
                f"{capacity}"
            )

            print(
                f"   Fuel: "
                f"{fuel:g}/"
                f"{fuel_capacity:g}L"
            )

            print(
                f"   Condition: "
                f"{condition:g}%"
            )

            print(
                f"   Status: "
                f"{status}"
            )

        print(
            f"\n{len(matatus) + 1}. "
            f"Switch Matatu"
        )

        print(
            f"{len(matatus) + 2}. "
            f"Back"
        )

        choice = input(
            "\nChoose an option: "
        )

        # ----------------------------------
        # SWITCH MATATU
        # ----------------------------------

        switch_option = len(matatus) + 1
        back_option = len(matatus) + 2

        if choice == str(switch_option):

            current_matatu_id = switch_matatu(
                database,
                player_id,
                current_matatu_id
            )

        elif choice == str(back_option):

            return current_matatu_id

        else:
            print(
                "\nInvalid choice."
            )


# ==========================================
# SWITCH MATATU
# ==========================================

def switch_matatu(
    database,
    player_id,
    current_matatu_id
):
    matatus = database.get_all_matatus(
        player_id
    )

    if not matatus:
        print(
            "\nYou don't own any matatus."
        )

        input(
            "\nPress Enter to continue..."
        )

        return current_matatu_id

    print("\nSWITCH MATATU")
    print("=" * 40)

    for index, matatu_data in enumerate(
        matatus,
        start=1
    ):
        name = matatu_data[1]
        model = matatu_data[2]
        capacity = matatu_data[3]
        active = matatu_data[14]

        status = (
            "ACTIVE"
            if active
            else "Owned"
        )

        print(
            f"\n{index}. "
            f"{name} - {model}"
        )

        print(
            f"   Capacity: "
            f"{capacity}"
        )

        print(
            f"   Status: "
            f"{status}"
        )

    print("\n0. Cancel")

    while True:
        choice = input(
            "\nChoose a matatu: "
        )

        if choice == "0":
            return current_matatu_id

        if not choice.isdigit():
            print(
                "Please enter a valid number."
            )

            continue

        choice = int(choice)

        if choice < 1 or choice > len(matatus):
            print(
                "Invalid choice."
            )

            continue

        selected_matatu = matatus[
            choice - 1
        ]

        selected_id = selected_matatu[0]

        if selected_id == current_matatu_id:
            print(
                "\nThat matatu is already active."
            )

            input(
                "\nPress Enter to continue..."
            )

            return current_matatu_id

        success = database.set_active_matatu(
            player_id,
            selected_id
        )

        if not success:
            print(
                "\nUnable to switch matatu."
            )

            input(
                "\nPress Enter to continue..."
            )

            return current_matatu_id

        print("\n" + "=" * 40)
        print("MATATU SWITCHED")
        print("=" * 40)

        print(
            f"You are now driving "
            f"{selected_matatu[1]}."
        )

        print(
            f"Model: "
            f"{selected_matatu[2]}"
        )

        input(
            "\nPress Enter to continue..."
        )

        return selected_id


# ==========================================
# TRIP HISTORY
# ==========================================

def display_trip_history(
    database,
    player_id
):
    trips = database.get_trip_history(
        player_id
    )

    print("\nTRIP HISTORY")
    print("=" * 50)

    if not trips:
        print(
            "No trips completed yet."
        )

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

        print(
            f"\nTrip #{trip_id}"
        )

        print(
            f"Route: {route_name}"
        )

        print(
            f"Passengers: "
            f"{passengers}"
        )

        print(
            f"Earnings: "
            f"KSh {earnings}"
        )

        print(
            f"Fuel used: "
            f"{fuel_used}L"
        )

        if event_name:
            print(
                f"Event: "
                f"{event_name}"
            )

        print(
            f"XP earned: "
            f"{experience}"
        )

        print(
            f"Reputation: "
            f"+{reputation}"
        )


# ==========================================
# PLAYER / MATATU STATUS
# ==========================================

def display_player_stats(player):
    player.display_stats()


def display_matatu_status(matatu):
    print("\nMY MATATU")
    print("=" * 40)

    matatu.display_info()

    input(
        "\nPress Enter to continue..."
    )


# ==========================================
# SAVE GAME
# ==========================================

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


# ==========================================
# START TRIP
# ==========================================

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
        print(
            "Your matatu has no fuel."
        )

        print(
            "Visit Maintenance to refuel."
        )

        input(
            "\nPress Enter to continue..."
        )

        return

    if matatu.condition <= 0:
        print(
            "Your matatu is badly damaged."
        )

        print(
            "Visit Maintenance to repair it."
        )

        input(
            "\nPress Enter to continue..."
        )

        return

    selected_route = choose_route(
        routes,
        player
    )

    if selected_route is None:
        print(
            "\nTrip cancelled."
        )

        input(
            "\nPress Enter to continue..."
        )

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
        print(
            "\nToo many passengers!"
        )

        input(
            "\nPress Enter to continue..."
        )

        return

    print(
        f"\n{len(passengers)} "
        f"passengers boarded."
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

        print(
            "\nTrip saved to database."
        )

    else:

        print(
            "\nTrip could not be completed."
        )

    input(
        "\nPress Enter to continue..."
    )


# ==========================================
# MAIN MENU
# ==========================================

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

        print(
            f"Driver: "
            f"{player.name}"
        )

        print(
            f"Money: "
            f"KSh {player.money}"
        )

        print(
            f"Level: "
            f"{player.level}"
        )

        print(
            f"Experience: "
            f"{player.experience}"
        )

        print(
            f"Reputation: "
            f"{player.reputation}"
        )

        print(
            f"\nActive Matatu: "
            f"{matatu.name}"
        )

        print("\n1. Start Trip")
        print("2. My Matatu")
        print("3. Maintenance")
        print("4. Garage")
        print("5. Matatu Shop")
        print("6. My Matatus")
        print("7. Trip History")
        print("8. Player Stats")
        print("9. Exit")

        choice = input(
            "\nChoose an option: "
        )

        # ----------------------------------
        # START TRIP
        # ----------------------------------

        if choice == "1":

            start_trip(
                player,
                matatu,
                routes,
                database,
                player_id,
                matatu_id
            )

        # ----------------------------------
        # MY MATATU
        # ----------------------------------

        elif choice == "2":

            display_matatu_status(
                matatu
            )

        # ----------------------------------
        # MAINTENANCE
        # ----------------------------------

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

            print(
                "\nGame saved."
            )

        # ----------------------------------
        # GARAGE
        # ----------------------------------

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

            print(
                "\nGame saved."
            )

        # ----------------------------------
        # MATATU SHOP
        # ----------------------------------

        elif choice == "5":

            matatu_shop_menu(
                player,
                database,
                player_id
            )

        # ----------------------------------
        # MY MATATUS
        # ----------------------------------

        elif choice == "6":

            new_matatu_id = (
                my_matatus_menu(
                    database,
                    player_id,
                    player,
                    matatu_id
                )
            )

            if new_matatu_id != matatu_id:

                new_matatu_data = (
                    database.get_matatu_by_id(
                        player_id,
                        new_matatu_id
                    )
                )

                if new_matatu_data:

                    matatu_id = (
                        new_matatu_id
                    )

                    matatu = (
                        create_matatu_from_data(
                            new_matatu_data
                        )
                    )

                    print(
                        f"\nActive matatu: "
                        f"{matatu.name}"
                    )

        # ----------------------------------
        # TRIP HISTORY
        # ----------------------------------

        elif choice == "7":

            display_trip_history(
                database,
                player_id
            )

            input(
                "\nPress Enter to continue..."
            )

        # ----------------------------------
        # PLAYER STATS
        # ----------------------------------

        elif choice == "8":

            display_player_stats(
                player
            )

            input(
                "\nPress Enter to continue..."
            )

        # ----------------------------------
        # EXIT
        # ----------------------------------

        elif choice == "9":

            save_game(
                database,
                player_id,
                matatu_id,
                player,
                matatu
            )

            print(
                "\nGame saved."
            )

            print(
                "Thanks for playing Matwana."
            )

            break

        else:

            print(
                "Invalid choice. "
                "Please select 1-9."
            )


# ==========================================
# MAIN
# ==========================================

def main():

    database = Database()

    database.create_tables()

    # ======================================
    # PLAYER
    # ======================================

    player = Player("Goon")

    player_data = database.get_player(
        player.name
    )

    if player_data is None:

        player_id = database.create_player(
            player
        )

        print(
            "\nNew player created."
        )

    else:

        player_id = player_data[0]

        player.name = player_data[1]
        player.money = player_data[2]
        player.level = player_data[3]
        player.experience = player_data[4]
        player.reputation = player_data[5]

        print(
            "\nPlayer progress loaded."
        )

    # ======================================
    # ACTIVE MATATU
    # ======================================

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
            matatu,
            active=True
        )

        print(
            "New matatu created."
        )

    else:

        matatu_id = matatu_data[0]

        matatu = (
            create_matatu_from_data(
                matatu_data
            )
        )

        print(
            "Matatu progress loaded."
        )

    # ======================================
    # ROUTES
    # ======================================

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

    # ======================================
    # START GAME
    # ======================================

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