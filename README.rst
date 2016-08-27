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
Diary is highest level part of the API; it is where all events are logged and processed.

**Initialization**

| ``class Diary(path, file_name="diary.txt", db_name="diary.db", event=events.Event,``
|   ``log_format=formats.standard, db=logdb.DiaryDB, async=True, debug_enabled=True)``

* ``path`` *str* of a path pointing to:
    - An empty directory where Diary will create a db and log
    - A text file where Diary will append
    - A database file where Diary will read and write
    - A directory with a database and txt file
        - looks for file_name and db_name arguments
    - A nonexistent path where a db or log will be made
* ``file_name`` *str* name for diary to look for during initialization or name of log file to be made
* ``db_name`` *str* name for diary to look for during initialization or name of db file
* ``event`` *Event* Event class which will initialize with logged strings
* ``log_format`` *function* which takes an event parameter and outputs a formatted string
* ``db`` *DiaryDB* Database type to be constructed for logging
* ``async`` *bool* Whether or not Diary should run in async mode
* ``debug_enabled`` *bool* Whether or not Diary should allow debug log level

**Fields** *(Not listed above)*

* ``db_file`` *File* where database is stored
* ``last_logged_event`` *Event* last event that was logged
* ``log_file`` *File* where log file is stored
* ``logdb`` *DiaryDB* set during set_db; DiaryDB instance that is stored to
* ``thread`` *DiaryThread* if run in async mode, the thread that is handling logging
* ``timer`` *RepeatedTimer* set during set_timer; thread to repeat a function
   - Useful for logging information every interval (such as app status)

**Methods**

* ``close()`` Close the resources used (automatically called on exit)
* ``debug(info, **kwargs)`` Log info with the debug level, kwargs passed to levels.debug
* ``error(info, **kwargs)`` Log info with the error level, kwargs passed to levels.error
* ``info(info, **kwargs)`` Log info with the info level, kwargs passed to levels.info
* ``log(info, level=levels.info, **kwargs)`` Log info with the specified level, kwargs passed to level
* ``set_db()`` To keep a db thread safe this is called by the DiaryThread or in the constructor if async is False
* ``set_timer(func, interval, *args, **kwargs)`` Set a func to be called every interval with given parameters
* ``warn(info, **kwargs)`` Log info with the warn level, kwargs passed to levels.warn
* ``write(event)`` Write an event to log_file, db_file, or both

Event
-----
Event describes information that is logged and is easily customized by inheritance.

**Initialization**

    ``class Event(info, level=None, dt=None)``

* ``info`` Information to log
* ``level`` the level that this event falls under
* ``dt`` *datetime* the time this event occurs (automatically set if dt is None)

**Fields** *(Not listed above)*

* ``formatter`` class variable of formatting method either a string or function
* ``level_str`` *str* the level as a readable string

**Methods**

* ``formatted()`` returns the event in a readable fashion for logging
* ``Event.set_formatter(formatter)`` set the class to formatter
* ``set_level(level)`` set level

**Inheriting**

* Event subclasses should set class level variables for formatter
* formatter should be a str which follows str.format syntax and kwarg fields should not contain self
   - GOOD: ``formatter = "|{info}|{level_str}|{dt}|"``
   - BAD: ``formatter = "|{self.info}|{self.level}|{self.dt}|"``
* If an Event subclass has extra fields a DiaryDB subclass will have to be made to put those extra fields in a db

DiaryDB
-------
DiaryDB is used to log Events into a database. DiaryDB uses SQLite3 but this can be changed by creating your own DiaryDB subclass.

DiaryDB can be used in a context manager.

``with DiaryDB("path/to/file") as db:``

**Initialization**
   ``class DiaryDB(path)``

* path *str* path of database to use. If no path is passed and the python command was invoked normally, it will look for a file named 'log.sqlite3' in the root folder of your application. In some edge cases when python programs aren't invoked through the process interface, you will need to pass a custom path even if 'log.sqlite3' is in the root folder of the application.

**Fields** *(Not listed above)*

* ``conn`` *sqlite3.connection* Connection to database
* ``cursor`` *sqlite3.cursor* Cursor for execution to connection

**Methods**

* ``assert_event_logged(log, level='%', limit=-1)`` Assert that an event matching the given parameters exists
* ``close()`` Close the database connection
* ``create_tables()`` Called on construction, creates tables in database for use
* ``log(event)`` Log an event into the database, automatically commits executions.

**Inheriting**

* If an Event subclass with extra attributes is logged only its datetime, info, and level are put into the database
* To Create a DiaryDB capable of handling specific Event subclasses\.\.\.
   - override the create_tables method to create a table with a column for each attribute
   - override the log method to execute the event attributes into your created tables
   - If you would like to use Diary to validate tests it is recommended you override assert_event_logged to accommodate specific events.

**Using different configurations**

To use a different database configurations simple inherit DiaryDB and
override __init__, create_tables, log, and close.

DiaryThread
-----------
DiaryThread is used by Diary to complete all logging processes asynchronously.
It has very little source code and is easily understood.
However inheriting from DiaryThread is not recommended and can only be utilized in a Diary subclass.

**Initialization**

    ``class DiaryThread(diary, sets_db=False, name="Diary Logger")``

* ``diary`` *Diary* diary to complete logging
* ``sets_db`` *bool* if database is set in run method
* ``name`` *str* identifier of thread

**Fields** *(Not listed above or inherited)*

* ``queue`` *Queue* events waiting to be logged

**Methods**

* ``add(event)`` queue an event for logging
* ``join([timeout])`` Process all events in queue and stop thread
* ``run()`` Main worker for DiaryThread

formats
-------
Formats are predefined functions that can be passed into Diary __init__ to give logs a more appropriate format.
 All formats only support name, info, and dt attributes of events.
 Write a custom format for your custom events, however it is recommended to give your Event subclasses a formatter field.

* ``alarms`` Separate event attributes with ! if an event has an error level
   - !!ERROR!!2016-07-31 21:55:00.165649!!NOOOOO!!
* ``easy_read`` An easy to read format
   - \|INFO\| On 07/30/16 @ 08:18.55PM \| example text
* ``minimal`` A minimal format
   - INFO: 07/30/16 20:15:48: example text
* ``standard`` A standard format
   - [INFO]:[2016-07-30 20:18:09.401149]: example text
* ``stringify_info(info)`` return info as a readable string
* ``stringify_level(level)`` return level as a readable string

levels
------
Levels are used to appropriately handle events based on their significance.
Developers are encouraged to define their own levels as the provided levels either have no side effects or have limited extra use.

log_level
^^^^^^^^^
Levels should be functions decorated by **@log_level** to ensure they are reported correctly.
Level calls should look like ``level(event, reporter, **kwargs)``; this allows an event to be reported and handled based on the kwargs.
Keyword arguments are always passed into the decorated level function.

* ``debug(event)`` Info only pertinent to developers, no side effects.
* ``error(event, raises=False, e_type=Exception, log_trace=True, limit=None)`` Errors in the program execution
   - ``raises`` *bool* Stops the program if an error is logged
      - ``e_type`` *Exception* type of exception to be raised
   - ``log_trace`` *bool* Add to event.info the stacktrace leading up to error
      - ``limit`` *int* Depth of stacktrace
* ``info(event)`` General info, no side effects
* ``warn(event, log_trace=False)`` Warnings for potential issues
   - ``log_trace`` *bool* Add to event.info the stacktrace leading up to the warning

Diary Command Line
==================

Diary comes with a command line tool, ``diary``, which can be used to generate a SQLite3 database for your diary application. Running the command is simple ::

    diary generate sqlite [path]

This will generate a SQLite3 database for diary at ``[path]``. The default path is ``log.sqlite3``. You should run this command in either the root directory of your project or within a logs folder for your project. If it is ran in the root directory and you use DiaryDB, diary will automatically know where to put your logs.

Contributing
============

Getting Started
---------------
Right now, diary is looking for contributors to help create formats, levels, and different database configurations. To begin contributing:

1. Fork or clone the repository ::

     git clone https://github.com/GreenVars/diary.git

2. Read the source and setup a virtual environment ::

     virtualenv venv
     source venv/bin/activate

3. Run the unit tests ::

     python tests/run_tests.py

4. Implement your changes and write unit tests for them.

5. Submit a pull request.

License
=======

Diary is protected by the MIT license
