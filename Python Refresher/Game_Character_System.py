#  🎮 Game Character System — Inheritance + Polymorphism

class Character:
    def __init__(self, name, health, attack):
        self.name = name
        self.health = health
        self.attack = attack

    def take_damage(self, damage):
        self.health = max(0, self.health - damage)

    def is_alive(self):
        return self.health > 0

    def attack_enemy(self, enemy):
        enemy.take_damage(self.attack)

    def display(self):
        print(
            f"{self.name} | "
            f"Health: {self.health} | "
            f"Attack: {self.attack}"
        )


class Warrior(Character):
    def attack_enemy(self, enemy):
        damage = self.attack + 20
        enemy.take_damage(damage)
        print(f"{self.name} dealt {damage} damage!")


class Mage(Character):
    def attack_enemy(self, enemy):
        damage = self.attack * 2
        enemy.take_damage(damage)
        print(f"{self.name} cast a spell for {damage} damage!")


class Archer(Character):
    def attack_enemy(self, enemy):
        damage = self.attack

        if enemy.health < 50:
            damage += 15

        enemy.take_damage(damage)
        print(f"{self.name} shot for {damage} damage!")


warrior = Warrior("Thor", 150, 30)
mage = Mage("Gandalf", 100, 25)
archer = Archer("Robin", 120, 35)

characters = [warrior, mage, archer]

for character in characters:
    character.display()

print("\nBattle:\n")

warrior.attack_enemy(mage)
mage.attack_enemy(warrior)
archer.attack_enemy(mage)

print("\nFinal Status:\n")

for character in characters:
    character.display()