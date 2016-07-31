from threading import Thread
try:
    from queue import Queue
except ImportError:  # python 2
    from Queue import Queue


class ElemThread(Thread):
    """A thread for logging as to not disrupt the logged application"""

    def __init__(self, elem, name="Elementary Logger"):
        """Construct a thread for logging

        :param elem: An Elementary instance to handle logging
        :param name: A string to represent this thread
        """
        Thread.__init__(self, name=name)
        self.daemon = True  # py2 constructor requires explicit
        self.elem = elem
        self.queue = Queue()
        self.start()

    def add(self, level, text):
        """Add a logged event to queue for logging"""
        self.queue.put((level, text))

    def run(self):
        """Main for thread to run"""
        while True:
            self.elem.write(*self.queue.get())
