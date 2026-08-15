class MatatuShop:
    MATATUS = {
        "shadow": {
            "name": "Shadow",
            "model": "Nissan Caravan",
            "price": 150000,
            "capacity": 16,
            "fuel_capacity": 70,
            "speed": 60,
            "comfort": 60
        },

        "king": {
            "name": "King",
            "model": "Toyota Quantum",
            "price": 250000,
            "capacity": 18,
            "fuel_capacity": 80,
            "speed": 70,
            "comfort": 70
        },

        "monster": {
            "name": "Monster",
            "model": "Mercedes Sprinter",
            "price": 400000,
            "capacity": 20,
            "fuel_capacity": 100,
            "speed": 80,
            "comfort": 80
        }
    }

    @classmethod
    def display_shop(cls, player, owned_models=None):
        print("\nMATATU SHOP")
        print("=" * 50)

        print(f"Money: KSh {player.money}")

        if owned_models is None:
            owned_models = []

        for index, (key, matatu) in enumerate(
            cls.MATATUS.items(),
            start=1
        ):
            print("\n" + "-" * 50)

            print(
                f"{index}. {matatu['name']} "
                f"({matatu['model']})"
            )

            print(
                f"Price: KSh {matatu['price']}"
            )

            print(
                f"Capacity: "
                f"{matatu['capacity']} passengers"
            )

            print(
                f"Fuel Capacity: "
                f"{matatu['fuel_capacity']}L"
            )

            print(
                f"Speed: {matatu['speed']}"
            )

            print(
                f"Comfort: {matatu['comfort']}"
            )

            if matatu["model"] in owned_models:
                print("Status: ALREADY OWNED")
            else:
                print("Status: AVAILABLE")

    @classmethod
    def get_matatu(cls, matatu_key):
        return cls.MATATUS.get(matatu_key)

    @classmethod
    def get_matatu_by_index(cls, index):
        matatus = list(cls.MATATUS.items())

        if index < 1 or index > len(matatus):
            return None

        key, matatu = matatus[index - 1]

        return key, matatu