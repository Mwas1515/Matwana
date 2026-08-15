class Matatu:
    def __init__(self, name, model, capacity=14):
        self.name = name
        self.model = model

        self.capacity = capacity

        self.fuel = 60
        self.fuel_capacity = 60

        self.condition = 100

        self.speed = 50
        self.comfort = 50

        self.fuel_price = 200
        self.repair_price = 500

        self.engine_level = 1
        self.suspension_level = 1
        self.seat_level = 1
        self.fuel_tank_level = 1
        self.comfort_level = 1

    def refuel(self, litres):
        if litres <= 0:
            return 0

        available_space = (
            self.fuel_capacity - self.fuel
        )

        fuel_added = min(
            litres,
            available_space
        )

        self.fuel += fuel_added

        return fuel_added

    def calculate_fuel_cost(self, litres):
        return litres * self.fuel_price

    def use_fuel(self, litres):
        self.fuel = max(
            self.fuel - litres,
            0
        )

    def repair(self, amount):
        if amount <= 0:
            return 0

        available_condition = (
            100 - self.condition
        )

        repaired = min(
            amount,
            available_condition
        )

        self.condition += repaired

        return repaired

    def calculate_repair_cost(self, amount):
        return amount * self.repair_price

    def damage(self, amount):
        self.condition = max(
            self.condition - amount,
            0
        )

    def can_carry(self, passenger_count):
        return passenger_count <= self.capacity

    def upgrade_engine(self):
        self.engine_level += 1
        self.speed += 10

    def upgrade_suspension(self):
        self.suspension_level += 1

    def upgrade_seats(self):
        self.seat_level += 1
        self.capacity += 2

    def upgrade_fuel_tank(self):
        self.fuel_tank_level += 1
        self.fuel_capacity += 10
        self.fuel += 10

    def upgrade_comfort(self):
        self.comfort_level += 1
        self.comfort += 10

    def display_info(self):
        print(f"\n{self.name}")
        print(f"Model: {self.model}")
        print(f"Capacity: {self.capacity} passengers")

        print(
            f"Fuel: {self.fuel}L / "
            f"{self.fuel_capacity}L"
        )

        print(f"Condition: {self.condition}%")
        print(f"Speed: {self.speed}")
        print(f"Comfort: {self.comfort}")

        print("\nUPGRADES")
        print(f"Engine: Level {self.engine_level}")
        print(
            f"Suspension: Level "
            f"{self.suspension_level}"
        )
        print(f"Seats: Level {self.seat_level}")
        print(
            f"Fuel Tank: Level "
            f"{self.fuel_tank_level}"
        )
        print(
            f"Comfort: Level "
            f"{self.comfort_level}"
        )