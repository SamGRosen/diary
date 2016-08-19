Diary
=====

Diary is a lightweight, no-dependency, asynchronous logging module. Diary has an
easy to use API for the simple and extensive use case.

.. image:: https://coveralls.io/repos/github/GreenVars/diary/badge.svg?branch=master
   :target: https://coveralls.io/github/GreenVars/diary?branch=master


.. image:: https://img.shields.io/pypi/pyversions/diary.svg?maxAge=2592000
   :target: https://pypi.python.org/pypi/diary/

.. image:: https://img.shields.io/pypi/v/diary.svg?maxAge=2592000
   :target: https://pypi.python.org/pypi/diary/


.. contents:: Table of Contents


Features
========
 - All logging processes are asynchronous to not disrupt the flow of the program
 - No dependencies
 - Write to a database, text file, or both
 - Use custom:
    - Formatting
    - Database configurations
    - Logging levels

Installation
============

From pypi::

    $ pip install diary

Or::

    $ easy_install diary

Or clone from github::

    $ git clone https://github.com/GreenVars/diary.git
    $ cd diary
    $ sudo python setup.py install

Support
-------
Please feel free to make issues on the `github repo. <http://github.com/GreenVars/diary>`_

Pull requests are more than welcome.

Simple API
==========

Quick Use
---------
Import the main object::

    from diary import Diary
    logger = Diary("log.txt")
    logger.log("Started app")
    number = 10
    logger.log("Initialized numbers")

Use different logging levels::

    from diary import levels
    # Diary.log defaults to the info level but can be specified as a keyword argument
    logger.log("Starting levels demonstration", level=levels.debug)
    logger.info("This is the default log level")
    logger.warn("This seems fishy")
    logger.error("Contact admin")
    logger.debug("Failed import; using alternate")

Customization
-------------

Defining a custom level::

    from diary import log_level

    @log_level
    def critical(event):
        event.info = "!! " + event.info + " !!"

    logger = Diary("EmergencyLogs.log")
    logger.log("URGENT ATTENTION NEEDED", level=critical)
    with open(logger.log_file.name) as f:
        print(f.readline())  # [CRITICAL]:[2016-08-15 05:12:27.566642]: !! URGENT ATTENTION NEEDED !!

Defining a custom formatter::

    def emergency_format(event):
        return "!!!|{dt}|{level}|{info}|!!!".format(
            dt=event.dt, level=event.level_text, info=event.info
        )
    logger = Diary("EmergencyLogs2.log", log_format=emergency_format)

    # OR We can define a custom event with a formatter
    from diary import Event

    class EmergencyEvent(Event):
        formatter = "|{dt}|{level_str}|{info}|"

    logger = Diary("EmergencyLogs3.log", event=EmergencyEvent)
    logger.log("There is a catastrophic issue")

Using a custom event::

    class UserEvent(Event):
        formatter = "[{level_str}]|{dt}|{info}|{user_name}"

        def __init__(self, info, level=None, user_name=""):
              Event.__init__(self, info, level)
              self.user_name = ""

    logger = Diary("UserEvents.txt", event=UserEvent)
    logger.log("Start logging")
    logger.info(UserEvent("admin logged in", user_name="admin"))  # Directly log events
    logger.warn(UserEvent("Unknown user logged in", user_name="127.0.0.1"))

Using a custom database::

    from diary import DiaryDB
    class UserActivityDB(DiaryDB):
        def create_tables(self):
             self.cursor.execute('''CREATE TABLE IF NOT EXISTS user_activity
                                    (inputDT TIMESTAMP, level TEXT, log TEXT, user TEXT)''')
        def log(self, event):
            with self.conn:
                self.cursor.execute('''
                                    INSERT INTO user_activity(inputDT, level, log, user)
                                                     VALUES(?, ?, ?, ?)''',
                                    (event.dt, event.level_str, event.info, event.user_name))

    logger = Diary("UserActivity.txt", event=UserEvent, db=UserActivityDB)
    logger.log("Starting app")
    logger.debug(UserEvent("Super user logged in", user_name="super"))
    logger.log(UserEvent("Hacker logged in", user_name="badguy"), level=critical)
    logger.close()
    with UserActivityDB(logger.db_file.name) as db:
        db.cursor.execute("SELECT * FROM user_activity")

Documentation
=============

Diary
-----
**Initialization**

    ``class Diary(path, file_name="diary.txt", db_name="diary.db", event=events.Event, log_format=formats.standard, db=logdb.DiaryDB, async=True, debug_enabled=True)``

* path *str* of a path pointing to:
    - An empty directory where Diary will create a db and log
    - A text file where Diary will append
    - A database file where Diary will read and write
    - A directory with a database and txt file
        - looks for file_name and db_name arguments
    - A nonexistent path where a db or log will be made
* file_name *str* name for diary to look for during initialization or name of log file to be made
* db_name *str* name for diary to look for during initialization or name of db file
* event *Event* Event class which will initialize with logged strings
* log_format *function* which takes an event parameter and outputs a formatted string
* db *DiaryDB* Database type to be constructed for logging
* async *bool* Whether or not Diary should run in async mode
* debug_enabled *bool* Whether or not Diary should allow debug log level

**Fields** *(Not listed above)*

* db_file *File* where database is stored
* last_logged_event *Event* last event that was logged
* log_file *File* where log file is stored
* logdb *DiaryDB* set during set_db; DiaryDB instance that is stored to
* thread *DiaryThread* if run in async mode, the thread that is handling logging
* timer *RepeatedTimer* set during set_timer; thread to repeat a function
   - Useful for logging information every interval (such as app status)

**Methods**

* close() Close the resources used (automatically called on exit)
* debug(info, \*\*kwargs) Log info with the debug level, kwargs passed to levels.debug
* error(info, \*\*kwargs) Log info with the error level, kwargs passed to levels.error
* info(info, \*\*kwargs) Log info with the info level, kwargs passed to levels.info
* log(info, level=levels.info, \*\*kwargs) Log info with the specified level, kwargs passed to level
* set_db() To keep a db thread safe this is called by the DiaryThread or in the constructor if async is False
* set_timer(func, interval, \*args, \*\*kwargs) Set a func to be called every interval with given parameters
* warn(info, \*\*kwargs) Log info with the warn level, kwargs passed to levels.warn
* write(event) Write an event to log_file, db_file, or both

Event
-----
**Initialization**
    ``class Event(info, level=None, dt=None)``

**Fields** *(Not listed above)*

* formatter
* level_str

**Methods**

* formatted
* set_formatter
* set_level

**Inheriting**

DiaryDB
-------
**Initialization**

**Fields** *(Not listed above)*

* conn
* cursor

**Methods**

* assert_event_logged
* close
* create_tables
* log

**Inheriting**

**Using different databases**

DiaryThread
-----------
**Initialization**

**Fields** *(Not listed above or inherited)*

* queue

**Methods**

* add
* join
* run

formats
-------
* alarms
* easy_read
* minimal
* standard
* stringify_info
* stringify_level

levels
------
log_level
^^^^^^^^^

* debug
* error
* info
* log
* warn

Copyrights and License
======================

Diary is protected by the MIT license