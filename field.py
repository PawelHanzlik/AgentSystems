class Field:

    def __init__(self, cord_x, cord_y, gold_generated, occupied_by) -> None:
        self.cord_x = cord_x
        self.cord_y = cord_y
        self.gold_generated = gold_generated
        self.occupied_by = occupied_by

    def __str__(self) -> str:
        return " "
