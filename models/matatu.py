class Matatu:
    def __init__(self, name, model, capacity=14):
        self.name = name
        self.model = model
        self.capacity = capacity

        self.fuel = 100
        self.fuel_capacity = 100

        self.condition = 100

        self.speed = 50
        self.comfort = 50

        self.fuel_price = 200
        self.repair_price = 500

    def refuel(self, amount):
        if amount <= 0:
            return 0

        available_space = self.fuel_capacity - self.fuel

        fuel_added = min(
            amount,
            available_space
        )

        self.fuel += fuel_added

        return fuel_added

    def calculate_fuel_cost(self, amount):
        return amount * self.fuel_price

    def use_fuel(self, amount):
        self.fuel = max(
            self.fuel - amount,
            0
        )

    def repair(self, amount):
        if amount <= 0:
            return 0

        available_condition = 100 - self.condition

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

    def needs_repair(self):
        return self.condition < 100

    def display_info(self):
        print(f"\n{self.name}")
        print(f"Model: {self.model}")
        print(f"Capacity: {self.capacity} passengers")
        print(f"Fuel: {self.fuel}%")
        print(f"Condition: {self.condition}%")
        print(f"Speed: {self.speed}")
        print(f"Comfort: {self.comfort}")