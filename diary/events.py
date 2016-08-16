from __future__ import absolute_import

from diary.formats import stringify_level
from datetime import datetime
from types import FunctionType


class Event(object):
    formatter = None
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
        :param formatter: str that is mappable to str.format or function that returns
            a formatted string
            ex.
                "[{info}][{level_text}][{dt}]" is equivalent to
                def formatted(self):
                    return "[{info}][{level}][{dt}]".format(
                        info=self.info,
                        level=self.level_str,
                        dt=self.dt)
        """
        self.dt = datetime.now() if dt is None else dt
        self.info = info
        self.level = level
        self.level_str = stringify_level(self.level)

    def formatted(self):
        if self.formatter:
            self.set_formatter(self.formatter) # Set class formatter discarding this method
            return self.formatted()
        else:
            raise AttributeError("{} does not have a valid formatter: {}".format(self, self.formatter))

    @classmethod
    def set_formatter(cls, formatter):
        cls.formatter = formatter
        if formatter:
            if isinstance(formatter, str):
                cls.formatted = lambda self: cls.formatter.format(**self.__dict__)
            elif type(formatter) is FunctionType:
                cls.formatted = cls.formatter
            else:
                raise ValueError('Could not identify formatter {}'.format(formatter))

    def set_level(self, level):
        self.level = level
        self.level_str = stringify_level(self.level)

    def __str__(self):
        if self.formatter:
            return self.formatted()
        return repr(self)

