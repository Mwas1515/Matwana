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
    def display_shop(cls, player, owned_matatus=None):
        print("\nMATATU SHOP")
        print("=" * 50)

        print(f"Money: KSh {player.money}")

        owned_names = set()

        if owned_matatus:
            for matatu in owned_matatus:
                owned_names.add(
                    matatu[1].lower()
                )

        for index, (key, matatu) in enumerate(
            cls.MATATUS.items(),
            start=1
        ):
            print("\n" + "-" * 50)

            print(
                f"{index}. "
                f"{matatu['name']} "
                f"({matatu['model']})"
            )

            print(
                f"Price: "
                f"KSh {matatu['price']}"
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
                f"Speed: "
                f"{matatu['speed']}"
            )

            print(
                f"Comfort: "
                f"{matatu['comfort']}"
            )

            if matatu["name"].lower() in owned_names:
                print("Status: OWNED")
            elif player.money >= matatu["price"]:
                print("Status: AVAILABLE")
            else:
                print("Status: TOO EXPENSIVE")

    @classmethod
    def get_matatu(cls, matatu_key):
        return cls.MATATUS.get(
            matatu_key
        )

    @classmethod
    def get_matatu_by_index(cls, index):
        matatus = list(cls.MATATUS.items())

        if index < 1 or index > len(matatus):
            return None

        key, matatu = matatus[index - 1]

        return key, matatu