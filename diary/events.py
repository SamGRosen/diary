from datetime import datetime


class Event():
    """Events are meant to be configurable and easy to create."""

    def __init__(self, info, level, dt=None):
        """All events should have info, level, and dt. Devs should inherit this
        class and add what parameters they see fit to the constructor.
        Note: Using a custom event will likely require a custom LoggerDB and
        formatter to get the most out of the most event. Appropriate
        inheritance of DiaryDB, Event, and a custom format makes Diary very
        configurable.

        :param info: information relevant to the log
        :param level: a level of classification to the log
        :param dt: time of logging, automatically set on init unless specified
        """
        self.dt = datetime.now() if dt is None else dt
        self.info = info
        self.level = level
