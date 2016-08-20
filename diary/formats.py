"""
Formats are ways to write your logged info to a text file.
For help creating your own:
    https://docs.python.org/3.5/library/datetime.html#strftime-strptime-behavior
Format functions take an event instance parameter
    def example(event):
        return "Level: {} {} {}".format(event.level, event.dt, event.info)
"""

from types import FunctionType


def stringify_level(level):
    """Turn level functions into a clean string

    :param level: any object to be stringified
    :return: level as a string
    """
    if type(level) is FunctionType:
        return level.__name__.upper()
    else:
        return str(level)

def stringify_info(info):
    """Turn info into a readadble string

    :param info:
    :return: info as a string
    """
    return str(info).strip()

def standard(event):
    """A simple default format
    ex: [INFO]:[2016-07-30 20:18:09.401149]: example text
    """
    return "[{name}]:[{time}]: {text}".format(
        name=stringify_level(event.level),
        time=event.dt,
        text=stringify_info(event.info)
    )


def minimal(event):
    """A straight to the point format
    ex: INFO: 07/30/16 20:15:48: example text
    """
    return "{name}: {0:%x} {0:%X}: {text}".format(
        event.dt,
        name=stringify_level(event.level),
        text=stringify_info(event.info)
    )


def alarms(event):
    """A format to emphasize important logs
    ex: !!ERROR!!2016-07-31 21:55:00.165649!!NOOOOO!!
    """
    separators = "!!!" if stringify_level(event.level) == 'ERROR' else " - "
    return "{sep}{name}{sep}{dt}{sep}{text}{sep}".format(
        sep=separators,
        name=stringify_level(event.level),
        text=stringify_info(event.info),
        dt=event.dt
    )


def easy_read(event):
    """An easier to read format
    ex: |INFO| On 07/30/16 @ 08:18.55PM | example text
    """
    return "|{name}| On {0:%x} @ {0:%I:%M.%S%p} | {text}".format(
        event.dt,
        name=stringify_level(event.level),
        text=stringify_info(event.info)
    )
