"""
Formats are ways to write your logged info to a text file.
For help creating your own:
    https://docs.python.org/3.5/library/datetime.html#strftime-strptime-behavior
Format functions take an event instance parameter
    def example(event):
        return "Level: {} {}".format(event.level, event.dt, event.info)
"""


def standard(event):
    """A simple default format
    ex: [INFO]:[2016-07-30 20:18:09.401149]: example text
    """
    return "[{name}]:[{time}]: {text}".format(
        name=event.level.__name__.upper(),
        time=event.dt,
        text=event.info.strip()
    )


def min(event):
    """A straight to the point format
    ex: INFO: 07/30/16 20:15:48: example text
    """
    return "{name}: {0:%x} {0:%X}: {text}".format(
        event.dt,
        name=event.level.__name__.upper(),
        text=event.info.strip()
    )


def alarms(event):
    """A format to emphasize important logs
    ex: !!ERROR!!2016-07-31 21:55:00.165649!!NOOOOO!!
    """
    seperators = "!!" if event.level.__name__ == 'error' else "-"
    return "{sep}{name}{sep}{dt}{sep}{text}{sep}".format(
        sep=seperators,
        name=event.level.__name__.upper(),
        text=event.info.strip(),
        dt=event.dt
    )


def easy_read(event):
    """An easier to read format
    ex: |INFO| On 07/30/16 @ 08:18.55PM | example text
    """
    return "|{name}| On {0:%x} @ {0:%I:%M.%S%p} | {text}".format(
        event.dt,
        name=event.level.__name__.upper(),
        text=event.info.strip()
    )
