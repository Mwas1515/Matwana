from models.player import Player
from models.matatu import Matatu
from models.route import Route
from models.passenger import Passenger
from models.trip import Trip
from models.garage import Garage
from models.matatu_shop import MatatuShop
from database.database import Database
from models.achievement_manager import AchievementManager
from models.achievement import Achievement
from gui.main_window import MainWindow


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

    # Restore saved upgrade levels.
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

        print(f"Money: KSh {player.money}")

        print(
            f"Fuel: {matatu.fuel:g}L / "
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

        # -------------------------
        # REFUEL
        # -------------------------

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
                    "Amount must be greater "
                    "than zero."
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

                print(
                    f"Required: KSh {cost}"
                )

                print(
                    f"Available: "
                    f"KSh {player.money}"
                )

                continue

            fuel_added = matatu.refuel(
                actual_litres
            )

            player.spend_money(cost)

            print(
                f"Added {fuel_added:g}L of fuel "
                f"for KSh {cost}."
            )

        # -------------------------
        # REPAIR
        # -------------------------

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
                    "Amount must be greater "
                    "than zero."
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

                print(
                    f"Required: KSh {cost}"
                )

                print(
                    f"Available: "
                    f"KSh {player.money}"
                )

                continue

            repaired = matatu.repair(
                actual_repair
            )

            player.spend_money(cost)

            print(
                f"Repaired {repaired:g}% "
                f"for KSh {cost}."
            )

        # -------------------------
        # CONTINUE
        # -------------------------

        elif choice == "3":
            break

        else:
            print("Invalid choice.")


# ==========================================
# GARAGE
# ==========================================

def garage_menu(
    player,
    matatu,
    database,
    player_id,
    matatu_id
):
    """Upgrade the active matatu."""

    while True:
        print("\nGARAGE")
        print("=" * 40)

        print(
            f"Money: KSh {player.money}"
        )

        print(
            f"Matatu: "
            f"{matatu.name} "
            f"({matatu.model})"
        )

        Garage.display_upgrades(
            matatu
        )

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

            upgraded = Garage.upgrade_matatu(
                player,
                matatu,
                upgrade
            )

            if upgraded:
                database.save_matatu(
                    matatu_id,
                    matatu
                )

                database.save_player(
                    player_id,
                    player
                )

                print(
                    "\nUpgrade saved."
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
        print("=" * 40)

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

        # -------------------------
        # PURCHASE VALIDATION
        # -------------------------

        can_buy, message = MatatuShop.can_buy(
            player,
            key,
            owned_models
        )

        if not can_buy:
            print(
                f"\n{message}"
            )

            input(
                "\nPress Enter to continue..."
            )

            continue

        # -------------------------
        # PURCHASE CONFIRMATION
        # -------------------------

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
            f"KSh {shop_matatu['price']}"
        )

        print(
            f"Capacity: "
            f"{shop_matatu['capacity']} passengers"
        )

        print(
            f"Fuel Capacity: "
            f"{shop_matatu['fuel_capacity']}L"
        )

        print(
            f"Speed: "
            f"{shop_matatu['speed']}"
        )

        print(
            f"Comfort: "
            f"{shop_matatu['comfort']}"
        )

        confirm = input(
            "\nBuy this matatu? (y/n): "
        ).lower()

        if confirm != "y":
            print(
                "\nPurchase cancelled."
            )
            continue

        # -------------------------
        # CREATE MATATU
        # -------------------------

        new_matatu = MatatuShop.create_matatu(
            key
        )

        if new_matatu is None:
            print(
                "\nUnable to create matatu."
            )
            continue

        # -------------------------
        # PAY FOR MATATU
        # -------------------------

        purchase_price = shop_matatu["price"]

        if not player.spend_money(
            purchase_price
        ):
            print(
                "\nPurchase failed."
            )
            continue

        # -------------------------
        # SAVE MATATU
        # -------------------------

        database.create_matatu(
            player_id,
            new_matatu,
            active=False
        )

        database.save_player(
            player_id,
            player
        )

        # -------------------------
        # PURCHASE SUCCESS
        # -------------------------

        print("\n" + "=" * 40)
        print("PURCHASE SUCCESSFUL")
        print("=" * 40)

        print(
            f"You bought the "
            f"{new_matatu.name}!"
        )

        print(
            f"Model: "
            f"{new_matatu.model}"
        )

        print(
            f"Money remaining: "
            f"KSh {player.money}"
        )

        print(
            "\nThe matatu has been added "
            "to My Matatus."
        )

        input(
            "\nPress Enter to continue..."
        )


# ==========================================
# MY MATATUS
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
        active = matatu_data[14]

        status = (
            "ACTIVE"
            if active
            else "Owned"
        )

        print(
            f"{index}. {name} - {model} "
            f"[{status}]"
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


def my_matatus_menu(
    database,
    player_id,
    player,
    current_matatu_id
):
    while True:
        print("\nMY MATATUS")
        print("=" * 40)

        print(
            f"Money: KSh {player.money}"
        )

        matatus = database.get_all_matatus(
            player_id
        )

        if not matatus:
            print(
                "\nYou don't own any matatus."
            )

            print("\n4. Back")

            choice = input(
                "\nChoose an option: "
            )

            if choice == "4":
                return current_matatu_id

            print("Invalid choice.")
            continue

        for index, matatu_data in enumerate(
            matatus,
            start=1
        ):
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
                f"   Capacity: {capacity}"
            )

            print(
                f"   Fuel: "
                f"{fuel:g}/{fuel_capacity:g}L"
            )

            print(
                f"   Condition: "
                f"{condition:g}%"
            )

            print(
                f"   Status: {status}"
            )

            print(
                f"   Engine: "
                f"Level {matatu_data[9]}/5"
            )

            print(
                f"   Suspension: "
                f"Level {matatu_data[10]}/5"
            )

            print(
                f"   Seats: "
                f"Level {matatu_data[11]}/5"
            )

            print(
                f"   Fuel Tank: "
                f"Level {matatu_data[12]}/5"
            )

            print(
                f"   Comfort: "
                f"Level {matatu_data[13]}/5"
            )

        switch_option = len(matatus) + 1
        back_option = len(matatus) + 2

        print(
            f"\n{switch_option}. Switch Matatu"
        )

        print(
            f"{back_option}. Back"
        )

        choice = input(
            "\nChoose an option: "
        )

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

        # Database structure:
        # 0 = id
        # 1 = route_name
        # 2 = distance
        # 3 = passengers
        # 4 = earnings
        # 5 = fuel_used
        # 6 = event_name
        # 7 = experience
        # 8 = reputation

        distance = trip[2]
        passengers = trip[3]
        earnings = trip[4]
        fuel_used = trip[5]
        event_name = trip[6]
        experience = trip[7]
        reputation = trip[8]

        print(f"\nTrip #{trip_id}")
        print(f"Route: {route_name}")
        print(f"Distance: {distance} km")
        print(f"Passengers: {passengers}")
        print(f"Earnings: KSh {earnings}")
        print(f"Fuel used: {fuel_used}L")

        if event_name:
            print(
                f"Event: {event_name}"
            )

        print(
            f"XP earned: {experience}"
        )

        print(
            f"Reputation: +{reputation}"
        )


# ==========================================
# ACHIEVEMENTS
# ==========================================

def display_achievements(
    database,
    player_id
):
    print("\nACHIEVEMENTS")
    print("=" * 50)

    unlocked_ids = (
        database.get_achievement_ids(
            player_id
        )
    )

    all_achievements = (
        Achievement.get_all_achievements()
    )

    if not all_achievements:
        print(
            "No achievements are available."
        )

        input(
            "\nPress Enter to continue..."
        )

        return

    for achievement_id in all_achievements:
        achievement = (
            Achievement.get_achievement(
                achievement_id
            )
        )

        if achievement is None:
            continue

        unlocked = (
            achievement_id in unlocked_ids
        )

        if unlocked:
            status = "UNLOCKED"
        else:
            status = "LOCKED"

        print("\n" + "-" * 50)

        print(
            f"{achievement['name']}"
        )

        print(
            f"Status: {status}"
        )

        print(
            f"Description: "
            f"{achievement['description']}"
        )

        print(
            f"Reward: "
            f"KSh {achievement['reward']}"
        )

    print("\n" + "=" * 50)

    print(
        f"Unlocked: "
        f"{len(unlocked_ids)}/"
        f"{len(all_achievements)}"
    )

    input(
        "\nPress Enter to continue..."
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
        print("\nTrip cancelled.")

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

        # -------------------------
        # SAVE TRIP
        # -------------------------

        database.save_trip(
            player_id,
            trip
        )

        # -------------------------
        # PROCESS ACHIEVEMENTS
        # -------------------------

        new_achievements = (
            AchievementManager.process_achievements(
                player,
                database,
                player_id
            )
        )

        # -------------------------
        # SAVE PLAYER + MATATU
        # -------------------------

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

        if new_achievements:
            print(
                f"{len(new_achievements)} "
                f"achievement(s) unlocked!"
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
        print("\n" + "=" * 45)
        print("MATWANA")
        print("=" * 45)

        print(
            f"Driver: {player.name}"
        )

        print(
            f"Money: KSh {player.money}"
        )

        print(
            f"Level: {player.level}"
        )

        print(
            f"Experience: {player.experience}"
        )

        print(
            f"Reputation: {player.reputation}"
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
        print("9. Achievements")
        print("10. Exit")

        choice = input(
            "\nChoose an option: "
        )

        # -------------------------
        # START TRIP
        # -------------------------

        if choice == "1":
            start_trip(
                player,
                matatu,
                routes,
                database,
                player_id,
                matatu_id
            )

        # -------------------------
        # MY MATATU
        # -------------------------

        elif choice == "2":
            display_matatu_status(
                matatu
            )

        # -------------------------
        # MAINTENANCE
        # -------------------------

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

        # -------------------------
        # GARAGE
        # -------------------------

        elif choice == "4":
            garage_menu(
                player,
                matatu,
                database,
                player_id,
                matatu_id
            )

            save_game(
                database,
                player_id,
                matatu_id,
                player,
                matatu
            )

            print("\nGame saved.")

        # -------------------------
        # MATATU SHOP
        # -------------------------

        elif choice == "5":
            matatu_shop_menu(
                player,
                database,
                player_id
            )

        # -------------------------
        # MY MATATUS
        # -------------------------

        elif choice == "6":
            new_matatu_id = my_matatus_menu(
                database,
                player_id,
                player,
                matatu_id
            )

            if new_matatu_id != matatu_id:
                new_matatu_data = (
                    database.get_matatu_by_id(
                        player_id,
                        new_matatu_id
                    )
                )

                if new_matatu_data:
                    matatu_id = new_matatu_id

                    matatu = (
                        create_matatu_from_data(
                            new_matatu_data
                        )
                    )

                    print(
                        f"\nActive matatu: "
                        f"{matatu.name}"
                    )

        # -------------------------
        # TRIP HISTORY
        # -------------------------

        elif choice == "7":
            display_trip_history(
                database,
                player_id
            )

            input(
                "\nPress Enter to continue..."
            )

        # -------------------------
        # PLAYER STATS
        # -------------------------

        elif choice == "8":
            display_player_stats(
                player
            )

            input(
                "\nPress Enter to continue..."
            )

        # -------------------------
        # ACHIEVEMENTS
        # -------------------------

        elif choice == "9":
            display_achievements(
                database,
                player_id
            )

        # -------------------------
        # EXIT
        # -------------------------

        elif choice == "10":
            save_game(
                database,
                player_id,
                matatu_id,
                player,
                matatu
            )

            print("\nGame saved.")

            print(
                "Thanks for playing Matwana."
            )

            break

        else:
            print(
                "Invalid choice. "
                "Please select 1-10."
            )


# ==========================================
# ROUTES
# ==========================================

def create_routes():
    """Create all available game routes."""

    return [
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


# ==========================================
# MAIN
# ==========================================

def main():
    """Start Matwana."""

    database = Database()

    # ==========================================
    # DATABASE SETUP
    # ==========================================

    database.create_tables()

    # ==========================================
    # PLAYER
    # ==========================================

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

    # ==========================================
    # ACTIVE MATATU
    # ==========================================

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

    # ==========================================
    # ROUTES
    # ==========================================

    routes = create_routes()

    # ==========================================
    # START GUI
    # ==========================================

    window = MainWindow(
        player,
        database,
        player_id
    )

    window.run()


# ==========================================
# PROGRAM ENTRY POINT
# ==========================================

if __name__ == "__main__":
    main()