Diary
=====

Diary is a lightweight, no-dependency, asynchronous logging module. Diary has an
easy to use API for the simple and extensive use case.

.. image:: https://codecov.io/gh/GreenVars/diary/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/GreenVars/diary

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

Simple API
----------

Quick Use
^^^^^^^^^
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
^^^^^^^^^^^^^

Defining a custom level::

    from diary import log_level

    @log_level
    def critical(event):
        event.info = "!!" + event.info + "!!"

    logger = Diary("EmergencyLogs.log")
    logger.log("URGENT ATTENTION NEEDED", level=critical)

    with open(logger.log_file.name) as f:
        print(f.readline()) # !! [CRITICAL]:[2016-08-15 05:12:27.566642]: URGENT ATTENTION NEEDED !!

Defining a custom formatter::

    def emergency_format(event):
        return "!!!|{dt}|{level}|{info}|!!!".format(
            dt=event.dt, level=event.level_text, info=event.info
        )
    logger = Diary("EmergencyLogs2.log", log_format=emergency_format)

    # OR We can define a custom event with a formatter
    from diary import Event

    class EmergencyEvent(Event):
        formatter = "|{dt}|{level_Text}|{info}|"

    logger = Diary("EmergencyLogs3.log", event=EmergencyEvent)
    logger.log("There is a catastrophic issue")

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


Upgrading
---------
To upgrade to the latest version::

    $ pip install -U diary

Support
-------
Please feel free to make issues on the `github repo. <http://github.com/GreenVars/diary>`_

Pull requests are more than welcome.

Documentation
=============


Copyrights and License
======================

Diary is protected by MIT license