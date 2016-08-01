from datetime import datetime

class Event():
    def __init__(self, info, level):
        self.dt = datetime.now()
        self.info = info
        self.level = level
