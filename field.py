class Field:

    def __init__(self, cord_x, cord_y, gold_generated, occupied_by) -> None:
        self.cord_x = cord_x
        self.cord_y = cord_y
        self.gold_generated = gold_generated
        self.occupied_by = occupied_by

    def __str__(self) -> str:
        return f"({self.cord_x},{self.cord_y}) -> gold: {self.gold_generated}, occupied by {'Red Army' if self.occupied_by == 1 else 'Blue Army' if self.occupied_by == 2 else 'Neutral'}"

