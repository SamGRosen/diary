import atexit
import os.path

import logdb
import levels
import formats
import events


class Diary(object):
    """Diary is a low-dependency and easy to use logger"""

    def __init__(self, path, file_name="diary.txt", db_name="diary.db",
                 event=events.Event, log_format=formats.standard,
                 db=logdb.DiaryDB, async=True, debug=True):
        """
        Initialization takes a file path meant to make startup simple
        :param path: str of a path pointing to:
            * An empty directory where Diary will initiate
            * A text file where Diary will append
            * A database file where Diary will read and write
            * A directory with a database and txt file
                - looks for file_name and db_name arguments
            * A nonexistent path for assumed writing
        :param file_name: a specified name for a log text file
        :param db_name: a specified name for a log database file
        :param event: Event object to construct log info
        :param log_format: function to format logging info (see formats.py)
        :param db: database class for reading/writing database
        :param async: boolean if logging should occur in own thread
        :param debug: boolean if logger supports debugging
        """

        self.path = path
        self.log_file = None
        self.db_file = None
        if os.path.exists(path):
            if os.path.isdir(path):
                self.log_file = open(os.path.join(path, file_name), 'a+')
                self.db_file = open(os.path.join(path, db_name), 'a+')
            elif os.path.isfile(path):
                head, tail = os.path.split(path)
                _, ext = os.path.splitext(tail)
                if ext == '':
                    self.log_file = open(path, 'a')
                elif tail == db_name or ext[1:] in ('db', 'sql', 'sqlite',
                                                    'sqlite3'):
                    self.db_file = open(path, 'a')
                elif tail == file_name or ext[1:] in ('txt', 'text', 'log'):
                    self.log_file = open(path, 'a')
                else:
                    raise ValueError("Could not resolve to database or text file {}".format(
                        path))
            else:
                raise ValueError("Could not handle path: {} | {}".format(
                    path, "Was not found a directory or file"))
        else:
            try:
                self.log_file = open(path, 'a')
            except Exception as e:
                raise e

        @atexit.register
        def cleanup():
            """Called on system exit to ensure logs are saved."""
            if self.log_file:
                self.log_file.close()
            if self.db_file:
                self.db_file.close()
                if self.async:
                    self.thread.join()
                self.logdb.close()

        self.close = cleanup
        self.event = event
        self.format = log_format
        self.db = db
        self.async = async
        self.debug_enabled = debug

        self.logdb = None
        self.last_logged_event = None

        sets_db = self.db_file is not None
        if async:
            from logthread import DiaryThread
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
        """Set a timer to log an event at every interval"""
        if self.async is False:
            raise Exception("In order to set a timer async must be enabled")

        from RepeatedTimer import RepeatedTimer
        self.timer = RepeatedTimer(interval, func, *args, **kwargs)
        self.timer.start()

    def write(self, event):
        """Write an event object to the proper channel

        :param event: event object to log
        """
        if self.db_file:
            self.logdb.log(event)
        if self.log_file:
            self.log_file.write(self.format(event))
        self.last_logged_event = event

    def log(self, info, level=levels.info):
        """Log info to its relevant level (see levels.py)

        :param info: info for logging
        :param level: @level decorated function handle relevant behavior
        """
        event_to_log = self.event(info, level)
        if self.async:
            level(event_to_log, self.thread.add)
        else:
            level(event_to_log, self.write)

    def info(self, info):
        """Log general info

        :param info: info relevant to application processes
        """
        self.log(info, level=levels.info)

    def warn(self, info):
        """Log info that requires a warning

        :param info: info relevant to a warning
        """
        self.log(info, level=levels.warn)

    def error(self, info):
        """Log info that may cause an error

        :param info: info relevant to an error
        """
        self.log(info, level=levels.error)

    def debug(self, info):
        """Log info that may only be helpful to the developer
        Will only log if debugging is enabled

        :param info: info for the devs
        """
        if self.debug_enabled:
            self.log(info, level=levels.debug)
