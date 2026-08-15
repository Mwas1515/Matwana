from models.matatu import Matatu


class MatatuShop:
    MATATUS = {
        "shadow": {
            "name": "Shadow",
            "model": "Nissan Caravan",
            "price": 150000,
            "capacity": 16,
            "fuel_capacity": 70,
            "speed": 60,
            "comfort": 60,
            "required_level": 1
        },

        "king": {
            "name": "King",
            "model": "Toyota Quantum",
            "price": 250000,
            "capacity": 18,
            "fuel_capacity": 80,
            "speed": 70,
            "comfort": 70,
            "required_level": 3
        },

        "monster": {
            "name": "Monster",
            "model": "Mercedes Sprinter",
            "price": 400000,
            "capacity": 20,
            "fuel_capacity": 100,
            "speed": 80,
            "comfort": 80,
            "required_level": 5
        }
    }

    # ==========================================
    # DISPLAY SHOP
    # ==========================================

    @classmethod
    def display_shop(
        cls,
        player,
        owned_models=None
    ):
        print("\nMATATU SHOP")
        print("=" * 50)

        print(
            f"Money: KSh {player.money}"
        )

        if owned_models is None:
            owned_models = []

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
                f"Required Level: "
                f"{matatu['required_level']}"
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

            # -------------------------
            # STATUS
            # -------------------------

            if matatu["model"] in owned_models:
                print(
                    "Status: ALREADY OWNED"
                )

            elif player.level < matatu["required_level"]:
                print(
                    "Status: LOCKED"
                )

                print(
                    f"Requires Level "
                    f"{matatu['required_level']}"
                )

            elif player.money < matatu["price"]:
                print(
                    "Status: TOO EXPENSIVE"
                )

            else:
                print(
                    "Status: AVAILABLE"
                )

    # ==========================================
    # GET MATATU
    # ==========================================

    @classmethod
    def get_matatu(cls, matatu_key):
        return cls.MATATUS.get(
            matatu_key
        )

    # ==========================================
    # GET MATATU BY INDEX
    # ==========================================

    @classmethod
    def get_matatu_by_index(cls, index):
        matatus = list(
            cls.MATATUS.items()
        )

        if index < 1 or index > len(matatus):
            return None

        key, matatu = matatus[
            index - 1
        ]

        return key, matatu

    # ==========================================
    # PURCHASE VALIDATION
    # ==========================================

    @classmethod
    def can_buy(
        cls,
        player,
        matatu_key,
        owned_models=None
    ):
        matatu = cls.get_matatu(
            matatu_key
        )

        if matatu is None:
            return False, "Invalid matatu."

        if owned_models is None:
            owned_models = []

        if matatu["model"] in owned_models:
            return False, (
                "You already own this matatu."
            )

        if player.level < matatu["required_level"]:
            return False, (
                f"You need Level "
                f"{matatu['required_level']} "
                f"to buy this matatu."
            )

        if player.money < matatu["price"]:
            return False, (
                f"You need KSh "
                f"{matatu['price']} "
                f"to buy this matatu."
            )

        return True, "Purchase available."

    # ==========================================
    # CREATE MATATU
    # ==========================================

    @classmethod
    def create_matatu(
        cls,
        matatu_key
    ):
        shop_matatu = cls.get_matatu(
            matatu_key
        )

        if shop_matatu is None:
            return None

        matatu = Matatu(
            name=shop_matatu["name"],
            model=shop_matatu["model"],
            capacity=shop_matatu["capacity"]
        )

        matatu.fuel_capacity = (
            shop_matatu["fuel_capacity"]
        )

        matatu.fuel = (
            shop_matatu["fuel_capacity"]
        )

        matatu.speed = (
            shop_matatu["speed"]
        )

        matatu.comfort = (
            shop_matatu["comfort"]
        )

        return matatu