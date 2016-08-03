from datetime import datetime


class Event():

    def __init__(self, info, level, dt=None):
        self.dt = datetime.now() if dt is None else dt
        self.info = info
        self.level = level
