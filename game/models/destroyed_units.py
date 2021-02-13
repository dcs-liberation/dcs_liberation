class DestroyedUnit:
    """
    Store info about a destroyed unit
    """

    x: int
    y: int
    name: str

    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name
