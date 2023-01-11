from army import Army
from unit import Unit


class Kingdom:
    def __init__(self, number, armies, money, morale):
        self.number = number
        self.armies = armies
        self.money = money
        self.morale = morale
        self.identifier = 0

    def recruitUnit(self, army, gridSize):
        for i in range(len(self.armies)):
            if len(self.armies[i].units) + len(self.armies[i].units_merged) < 10:
                self.armies[i].recruitUnit(army, gridSize)
                self.morale += 0.02
                break
            elif len(self.armies[i].units) + len(self.armies[i].units_merged) >= 10 and i == len(self.armies)-1:
                if army == "A":
                    unit = Unit(0, 0, 0, 0, 5, 'images/blueUnit.png')
                    n_army = Army('images/blueArmy.png', self.identifier, 1, 0, 0, [unit], [unit], 800, False, 1.5)
                    self.armies.append(n_army)
                elif army == "B":
                    unit = Unit(0, gridSize-1, gridSize-1, 0, 5, 'images/redUnit.png')
                    n_army = Army('images/redArmy.png', self.identifier, 2, gridSize-1, gridSize-1, [unit], [unit], 800, False, 1.5)
                    self.armies.append(n_army)
                self.identifier += 1
                self.morale += 3
        self.money -= 5000
