import logging
import traceback
import sys

from io import StringIO
from tkinter import *
from tkinter.scrolledtext import *

_version_string = None


class ShowLogsException(Exception):
    pass


def _error_prompt(oops=True):
    tk = Tk()
    if oops:
        Label(tk, text="Oops, something went wrong.").grid(row=0)
    Label(tk, text="Please send following text to the developer:").grid(row=1)

    text = ScrolledText(tk)
    text.insert("0.0", log_stream.getvalue())
    text.grid(row=2, sticky=NSEW)
    tk.focus()


def _handle_exception(self, exception: BaseException, *args):
    logging.exception(exception)
    _error_prompt(isinstance(exception, ShowLogsException))


def setup_version_string(str):
    global _version_string
    _version_string = str


def version_string():
    return _version_string


if "--stdout" in sys.argv:
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
else:
    log_stream = StringIO()
    logging.basicConfig(stream=log_stream, level=logging.INFO)
    Tk.report_callback_exception = _handle_exception

logging.info("DCS Liberation {}".format(_version_string))
