import typing

import json
import threading
import time
import os

from datetime import datetime

DEBRIEFING_LOG_EXTENSION = "log"


class Debriefing:
    def __init__(self):
        self.destroyed_units = {}  # type: typing.Dict[str, typing.Dict[str, int]]

    @classmethod
    def parse(cls, path: str):
        with open(path, "r") as f:
            events = json.load(f)

        return Debriefing()


def debriefing_directory_location() -> str:
    return "build/debriefing"


def _logfiles_snapshot() -> typing.Dict[str, float]:
    result = {}
    for file in os.listdir(debriefing_directory_location()):
        fullpath = os.path.join(debriefing_directory_location(), file)
        result[file] = os.path.getmtime(fullpath)

    return result


def _poll_new_debriefing_log(snapshot: typing.Dict[str, float], callback: typing.Callable):
    should_run = True
    while should_run:
        for file, timestamp in _logfiles_snapshot().items():
            if file not in snapshot or timestamp != snapshot[file]:
                callback(Debriefing.parse(os.path.join(debriefing_directory_location(), file)))
                should_run = False
                break

        time.sleep(1)


def wait_for_debriefing(callback: typing.Callable):
    threading.Thread(target=_poll_new_debriefing_log, args=(_logfiles_snapshot(), callback)).start()

