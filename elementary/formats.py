"""
    Formats are ways to write your logged info to a text file.
    For help creating your own:
        https://docs.python.org/3.5/library/datetime.html#strftime-strptime-behavior
"""

import datetime


def standard(level, text):
    return "[{name}]:[{time}]: {text}".format(
        name=level.__name__.upper(),
        time=datetime.datetime.now(),
        text=text.strip()
    )


def min(level, text):
    return "{name}: {0:%x} {0:%X}: {text}".format(
        datetime.datetime.now(),
        name=level.__name__.upper(),
        text=text.strip()
    )


def easy_read(level, text):
    return "|{name}| On {0:%x} @ {0:%I:%M.%S%p} | {text}".format(
        datetime.datetime.now(),
        name=level.__name__.upper(),
        text=text.strip()
    )
