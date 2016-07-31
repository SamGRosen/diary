import levels
import formats


class Elementary(object):
    """ Elementary is a low-dependency and easy to use logger """

    def __init__(self, path, format=formats.standard, async=False):
        """
        Initialization takes a file path meant to make startup simple
        :param path: str of a path pointing to -
            * An empty directory where Elementary will initiate
            * A txt file where Elementary will write
            * A database file where Elementary will read and write
            * A directory with a database and txt file
            * A nonexistent path for assumed writing
        :param format: function to format logging info (see formats.py)
        :param async: boolean if logging should occur in own thread
        """
        self.path = path
        self.format = format
        self.async = async
        self.debug_enabled = True
        if async:
            from logthread import ElemThread
            self.thread = ElemThread(self)

    def set_timer(self, interval, func, *args, **kwargs):
        """Set a timer to run a function at every interval"""
        from threading import Timer

        self.timer = Timer(interval, func, *args, **kwargs)

    def write(self, level, text):
        print(self.format(level, text))

    def log(self, info, level=levels.info):
        """Log info to its relevant level (see levels.py)

        :param info: info for logging
        :param level: @level decorated function handle relevant behavior
        """
        if self.async:
            level(info, self.thread.add)
        else:
            level(info, self.write)

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


if __name__ == '__main__':
    # from elementary import Elementary as el
    el = Elementary
    help(el)
    example_el = el("", format=formats.easy_read, async=True)
    example_el.log("hello")
    example_el.warn("oh no")
