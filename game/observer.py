class Event(object):
    pass


class Observable(object):
    def __init__(self) -> None:
        self.callbacks = []

    def subscribe(self, callback) -> None:
        self.callbacks.append(callback)

    def unsubscribe(self, callback) -> None:
        self.callbacks.remove(callback)

    def fire(self, **attrs) -> None:
        e = Event()
        e.source = self
        for k, v in attrs.items():
            setattr(e, k, v)
        for fn in self.callbacks:
            fn(e)
