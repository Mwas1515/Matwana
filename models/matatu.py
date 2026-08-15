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

    def refuel(self, amount):
        self.fuel = min(self.fuel + amount, self.fuel_capacity)

    def use_fuel(self, amount):
        self.fuel = max(self.fuel - amount, 0)

    def repair(self, amount):
        self.condition = min(self.condition + amount, 100)

    def damage(self, amount):
        self.condition = max(self.condition - amount, 0)

    def display_info(self):
        print(f"\n {self.name}")
        print(f"Model: {self.model}")
        print(f"Capacity: {self.capacity} passengers")
        print(f"Fuel: {self.fuel}%")
        print(f"Condition: {self.condition}%")
        print(f"Speed: {self.speed}")
        print(f"Comfort: {self.comfort}")