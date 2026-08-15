class Player:
    def __init__(self, name):
        self.name = name
        self.money = 5000
        self.level = 1
        self.experience = 0
        self.reputation = 0

    def earn_money(self, amount):
        self.money += amount

    def spend_money(self, amount):
        if amount > self.money:
            return False

        self.money -= amount
        return True

    def add_experience(self, amount):
        self.experience += amount

    def add_reputation(self, amount):
        self.reputation += amount