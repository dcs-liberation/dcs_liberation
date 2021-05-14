import logging
import timeit
from contextlib import contextmanager
from datetime import timedelta
from typing import Iterator


@contextmanager
def logged_duration(event: str) -> Iterator[None]:
    start = timeit.default_timer()
    yield
    end = timeit.default_timer()
    logging.debug("%s took %s", event, timedelta(seconds=end - start))
