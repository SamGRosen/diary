"""
Formats are ways to write your logged info to a text file.
For help creating your own:
    https://docs.python.org/3.5/library/datetime.html#strftime-strptime-behavior
Format functions take two parameters: level, and text
    def example(level, text):
        return "Level: {} {}".format(level, time, text)
"""

import datetime


def standard(level, text):
    """A simple default format
    ex: [INFO]:[2016-07-30 20:18:09.401149]: example text
    """
    return "[{name}]:[{time}]: {text}".format(
        name=level.__name__.upper(),
        time=datetime.datetime.now(),
        text=text.strip()
    )


def min(level, text):
    """A straight to the point format
    ex: INFO: 07/30/16 20:15:48: example text
    """
    return "{name}: {0:%x} {0:%X}: {text}".format(
        datetime.datetime.now(),
        name=level.__name__.upper(),
        text=text.strip()
    )

def alarms(level, text):
    """A format to emphasize important logs
    ex: !!INFO!!
    """
    seperators = "!!" if level.__name__ == 'error' else "-"
    return "{sep}{name}{sep}{dt}{sep}{text}{sep}".format(
        sep=seperators,
        name=level.__name__.upper(),
        text=text.strip(),
        dt=datetime.datetime.now()
    )

def easy_read(level, text):
    """An easier to read format
    ex: |INFO| On 07/30/16 @ 08:18.55PM | example text
    """
    return "|{name}| On {0:%x} @ {0:%I:%M.%S%p} | {text}".format(
        datetime.datetime.now(),
        name=level.__name__.upper(),
        text=text.strip()
    )
