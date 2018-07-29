import logging
import traceback

from io import StringIO
from tkinter import *
from tkinter.scrolledtext import *

log_stream = StringIO()
logging.basicConfig(stream=log_stream, level=logging.INFO)


def _error_prompt():
    tk = Tk()
    Label(tk, text="Oops, something went wrong.").grid(row=0)
    Label(tk, text="Please send following text to the developer:").grid(row=1)

    text = ScrolledText(tk)
    text.insert("0.0", log_stream.getvalue())
    text.grid(row=2, sticky=NSEW)
    tk.focus()


def _handle_exception(self, exception: BaseException, *args):
    logging.exception(exception)
    _error_prompt()


Tk.report_callback_exception = _handle_exception
logging.info("DCS Libration 1.3 RC2")
