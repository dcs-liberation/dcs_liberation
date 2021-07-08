import datetime


class Information:
    def __init__(self, title: str = "", text: str = "", turn: int = 0) -> None:
        self.title = title
        self.text = text
        self.turn = turn
        self.timestamp = datetime.datetime.now()

    def __str__(self) -> str:
        return "[{}][{}] {} {}".format(
            self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            if self.timestamp is not None
            else "",
            self.turn,
            self.title,
            self.text,
        )
