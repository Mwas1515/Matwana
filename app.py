from models.player import Player
from models.matatu import Matatu
from models.route import Route


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

    print("\n Available Routes:")

    for route in routes:
        route.display_info()

    print("\n Welcome to Matwana!")
    print(f"Driver: {player.name}")
    print(f"Money: KSh {player.money}")

    matatu.display_info()


if __name__ == "__main__":
    main()