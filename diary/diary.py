from __future__ import absolute_import
from __future__ import print_function
import atexit
import os.path
import codecs
import sys

from diary import logdb
from diary import levels
from diary import formats
from diary import events

_PY2 = sys.version_info[0] == 2


class Diary(object):
    """Diary is a low-dependency and easy to use logger"""

    def __init__(self, path, file_name="diary.txt", db_name="diary.db",
                 event=events.Event, log_format=formats.standard,
                 db=logdb.DiaryDB, async=True, debug_enabled=True,
                 encoding="utf-8", also_print=True):
        """
        Initialization takes a file path meant to make startup simple
        :param path: str of a path pointing to:
            * An empty directory where Diary will create a db and log
            * A text file where Diary will append
            * A database file where Diary will read and write
            * A directory with a database and txt file
                - looks for file_name and db_name arguments
            * A nonexistent path for where a db or a log will be made
        :param file_name: a specified name for a log text file
        :param db_name: a specified name for a log database file
        :param event: Event object to construct log info
        :param log_format: function to format logging info (see formats.py)
        :param db: database class for reading/writing database
        :param async: boolean if logging should occur in own thread
        :param debug_enabled: boolean if logger supports debugging
        :param encoding: str type of encoding to use for writing to log file
        :param also_print: boolean if a logged statement will also be printed to the console
        """

        self.path = path
        self.encoding = encoding
        self.log_file = None
        self.db_file = None
        self.also_print = also_print
        if os.path.exists(path):
            if os.path.isdir(path):
                self.log_file = codecs.open(os.path.join(path, file_name), mode='a+', buffering=1, encoding=self.encoding)
                self.db_file = open(os.path.join(path, db_name), 'a')
            elif os.path.isfile(path):
                head, tail = os.path.split(path)
                _, ext = os.path.splitext(tail)
                if ext == '':
                    self.log_file = codecs.open(path, mode='a+', buffering=1, encoding=self.encoding)
                elif tail == db_name or ext[1:] in ('db', 'sql', 'sqlite',
                                                    'sqlite3'):
                    self.db_file = open(path, 'a')
                elif tail == file_name or ext[1:] in ('txt', 'text', 'log'):
                    self.log_file = codecs.open(path, mode='a+', buffering=1, encoding=self.encoding)
                else:
                    raise ValueError("Could not resolve to database or text file {}".format(
                        path))
            else:
                raise ValueError("Could not handle path: {} | {}".format(
                    path, "Was not found a directory or file"))
        else:
            try:
                _, ext = os.path.splitext(path)
                if len(ext) > 1:
                    if ext[1:] in ('db', 'sql', 'sqlite', 'sqlite3'):
                        self.db_file = open(path, 'a')
                    else:
                        self.log_file = codecs.open(path, mode='a+', buffering=1, encoding=self.encoding)
                else:
                    self.log_file = codecs.open(path, mode='a+', buffering=1, encoding=self.encoding)
            except Exception as e:
                raise e

        @atexit.register
        def cleanup():
            """Called on system exit to ensure logs are saved."""
            if self.async:
                self.thread.join()

            if self.db_file:
                self.db_file.close()

                self.logdb.close()
            if self.log_file:
                self.log_file.close()
            self.timer = None

        self.close = cleanup
        self.event = event
        self.format = log_format
        self.db = db
        self.async = async
        self.debug_enabled = debug_enabled

        self.logdb = None
        self.last_logged_event = None

        sets_db = self.db_file is not None
        if async:
            from diary.logthread import DiaryThread
            self.thread = DiaryThread(self, sets_db=sets_db)
        elif sets_db:
            self.set_db()

    def set_db(self):
        """
        In order to keep databases thread safe set_db
        is called by self.thread if async is enabled.
        """
        if self.db_file is None:
            raise ValueError("Cannot set a database without a database file")
        self.logdb = self.db(self.db_file.name)

    def set_timer(self, interval, func, *args, **kwargs):
        """Set a timer to log an event at every interval

        :param interval: time in milliseconds to repeat func
        :param func: func to execute
        :param args: args to pass into func
        :param kwargs: kwargs to pass into func
        """
        if self.async is False:
            raise RuntimeError("In order to set a timer async must be enabled")

        from diary.RepeatedTimer import RepeatedTimer
        self.timer = RepeatedTimer(interval, func, args=args, kwargs=kwargs)
        self.timer.start()

    def _write(self, event):
        """Write an event object to the proper channel

        :param event: event object to log
        """
        if self.db_file:
            self.logdb.log(event)

        if self.log_file:
            if event.formatter is None:
                to_write = self.format(event) + '\n'
            else:
                to_write = event.formatted() + '\n'

            if _PY2:
                to_write = to_write.decode(self.encoding)

            self.log_file.write(to_write)

            if self.also_print:
                print(to_write)

        self.last_logged_event = event

    def log(self, info, level=levels.info, **kwargs):
        """Log info to its relevant level (see levels.py)

        :param info: info for logging
        :param level: @level decorated function handle relevant behavior
        """
        if isinstance(info, events.Event):
            event_to_log = info
        else:
            event_to_log = self.event(info, level)

        if _PY2 and isinstance(event_to_log.info, unicode):  # short-circuiting at its best
            event_to_log.info = event_to_log.info.encode(self.encoding)

        if self.async:
            level(event_to_log, self.thread.add, **kwargs)
        else:
            level(event_to_log, self._write, **kwargs)

    def info(self, info, **kwargs):
        """Log general info

        :param info: info relevant to application processes
        """
        if isinstance(info, events.Event):
            info.set_level(levels.info)

        self.log(info, level=levels.info, **kwargs)

    def warn(self, info, **kwargs):
        """Log info that requires a warning

        :param info: info relevant to a warning
        """
        if isinstance(info, events.Event):
            info.set_level(levels.warn)

        self.log(info, level=levels.warn, **kwargs)

    def error(self, info, **kwargs):
        """Log info that may cause an error

        :param info: info relevant to an error
        """
        if isinstance(info, events.Event):
            info.set_level(levels.error)

        self.log(info, level=levels.error, **kwargs)

    def debug(self, info, **kwargs):
        """Log info that may only be helpful to the developer
        Will only log if debugging is enabled

        :param info: info for the devs
        """
        if isinstance(info, events.Event):
            info.set_level(levels.debug)

        if self.debug_enabled:
            self.log(info, level=levels.debug, **kwargs)
