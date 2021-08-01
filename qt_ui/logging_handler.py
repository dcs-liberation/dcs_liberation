import logging
import typing

LogHook = typing.Callable[[str], None]


class HookableInMemoryHandler(logging.Handler):
    """Hookable in-memory logging handler for logs window"""

    _log: str
    _hook: typing.Optional[typing.Callable[[str], None]]

    def __init__(self, *args, **kwargs):
        super(HookableInMemoryHandler, self).__init__(*args, **kwargs)
        self._log = ""
        self._hook = None

    @property
    def log(self) -> str:
        return self._log

    def emit(self, record):
        msg = self.format(record)
        self._log += msg + "\n"
        if self._hook is not None:
            self._hook(msg)

    def write(self, m):
        pass

    def clearLog(self) -> None:
        self._log = ""

    def setHook(self, hook: typing.Callable[[str], None]) -> None:
        self._hook = hook

    def clearHook(self) -> None:
        self._hook = None
