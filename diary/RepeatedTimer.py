try:
    from threading import _Timer
except ImportError:  # python3
    from threading import Timer as _Timer


class RepeatedTimer(_Timer):
    """RepeatedTimer overrides threading.Timer to run multiple times"""

    def __init__(self, interval, func, *args, **kwargs):
        """
        :param interval: time in milliseconds to repeat func
        :param func: func to execute
        :param args: args to pass into func
        :param kwargs: kwargs to pass into func
        """
        _Timer.__init__(self, interval, func, *args, **kwargs)
        self.daemon = True

    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)
