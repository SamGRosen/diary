from threading import Timer
from levels import info, warn, error, debug as \
    _info, _warn, _error, _debug


class Elementary(object):
    """ Elementary is a low-dependency and easy to use logger """

    def __init__(self, path, async=False):
        """
            Initialization takes a file path meant to make startup simple
            :param path: str of a path pointing to -
                * An empty directory where Elementary will initiate
                * A txt file where Elementary will write
                * A database file where Elementary will read and write
                * A directory with a database and txt file
                * A nonexistent path for assumed writing
            :param async: boolean if logging should occur in own thread
        """
        self.path = path
        self.async = async
        self.debug_enabled = True
        if async:
            from .thread import ElemThread

    def set_timer(self, interval, func, *args, **kwargs):
        """ Set a timer to run a function at every interval """
        self.timer = Timer(interval, func, *args, **kwargs)

    def log(self, info, level=None):
        output = level(info)
        self.write(output)

    def info(self, info):
        self.log(info, level=_info)

    def warn(self, info):
        self.log(info, level=_warn)

    def error(self, info):
        self.log(info, level=_error)

    def debug(self, info):
        if self.debug_enabled:
            self.log(info, level=_debug)


if __name__ == '__main__':
    # from elementary import Elementary as el
    el = Elementary
    example_el = el("")
    example_el.log("")
