from models.player import Player
from models.matatu import Matatu


def main():
    player = Player("Goon")

    matatu = Matatu(
        name="Beast",
        model="Toyota Hiace"
    )

    print("Welcome to Matwana!")
    print(f"Driver: {player.name}")
    print(f"Money: KSh {player.money}")

    matatu.display_info()

    print("\nStarting a trip...")

    matatu.use_fuel(15)
    matatu.damage(5)

    print("\nAfter the trip:")
    matatu.display_info()


if __name__ == "__main__":
    main()