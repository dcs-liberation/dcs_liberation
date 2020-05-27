
class Information():

    def __init__(self, title="", text="", turn=0):
        self.title = title
        self.text = text
        self.turn = turn

    def __str__(self):
        s = "[" + str(self.turn) + "] " + self.title + "\n" + self.text
        return s