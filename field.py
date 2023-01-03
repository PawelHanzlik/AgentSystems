class Field:

    def __init__(self, cord_x, cord_y, gold_generated, occupied_by, standing_on=None) -> None:
        if standing_on is None:
            standing_on = []
        self.cord_x = cord_x
        self.cord_y = cord_y
        self.gold_generated = gold_generated
        self.occupied_by = occupied_by
        self.standing_on = standing_on

    def __str__(self) -> str:
        return f"({self.cord_x},{self.cord_y}) -> gold: {self.gold_generated}, occupied by {'Red Army' if self.occupied_by == 1 else 'Blue Army' if self.occupied_by == 2 else 'Neutral'}"
