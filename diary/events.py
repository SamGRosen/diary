from __future__ import absolute_import

from diary.formats import stringify_level
from datetime import datetime
from types import FunctionType


class Event(object):
    """Events to log
    Give a class level variable called formatter to set an Event subclass format:
        class CustomEvent(Event):
            formatter = "{info}::{dt}::{level_str}"

        OR

        def format_my_event(event):
            return "{info}::{dt}::{level_str}".format(
                info=event.info, dt=event.dt, level_str=event.level_str)

        class CustomEvent(Event):
            formatter = format_my_event
    """
    formatter = None

    def __init__(self, info, level=None, dt=None):
        """All events should have info, level, and dt. Devs should inherit this
        class and add what parameters they see fit to the constructor.
        Note: Using a custom event will likely require a custom DiaryDB and
        formatter to get the most out of the event. Appropriate
        inheritance of DiaryDB, Event, and a custom format makes Diary very
        configurable.

        :param info: information relevant to the log
        :param level: a level of classification to the log
        :param dt: time of logging, automatically set on init unless specified
        """
        self.dt = datetime.now() if dt is None else dt
        self.info = info
        self.level = level
        self.level_str = stringify_level(self.level)

    def _formatted_setup(self):
        """
        Set class formatter
        :return: event formatted in a string
        """
        if self.formatter:
            self.set_formatter(self.formatter)  # Set class formatter discarding this method
            return self.formatted()
        else:
            raise AttributeError("{} does not have a valid formatter: {}".format(self, self.formatter))

    def formatted(self):
        """
        :return: event formatted in a string
        """
        return self._formatted_setup()

    @classmethod
    def set_formatter(cls, formatter):
        """Set the class formatter

        :param formatter: valid string or func to format events
        :return: None
        """
        cls.formatted = cls._formatted_setup
        cls.formatter = formatter
        if formatter:
            if isinstance(formatter, str):
                cls.formatted = lambda self: formatter.format(**self.__dict__)
            elif type(formatter) is FunctionType:
                cls.formatted = cls.formatter
            else:
                raise ValueError('Could not identify formatter {}'.format(formatter))

    def set_level(self, level):
        """
        Set the event level
        :param level: @log_level func or other level classifier
        :return: None
        """
        self.level = level
        self.level_str = stringify_level(self.level)

    def __str__(self):
        if self.formatter:
            return self.formatted()
        return repr(self)
