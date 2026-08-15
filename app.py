from models.player import Player


def main():
    player = Player("Goon")

    print("🚐 Welcome to Matwana!")
    print(f"Driver: {player.name}")
    print(f"Money: KSh {player.money}")
    print(f"Level: {player.level}")
    print(f"Experience: {player.experience}")
    print(f"Reputation: {player.reputation}")

    player.earn_money(1500)

    print(f"\nAfter completing a trip:")
    print(f"Money: KSh {player.money}")


if __name__ == "__main__":
    main()