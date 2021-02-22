import datetime


class Information:
    def __init__(self, title="", text="", turn=0):
        self.title = title
        self.text = text
        self.turn = turn
        self.timestamp = datetime.datetime.now()

    def __str__(self):
        return "[{}][{}] {} {}".format(
            self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            if self.timestamp is not None
            else "",
            self.turn,
            self.title,
            self.text,
        )
