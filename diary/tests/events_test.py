import unittest
import diary

class TestEvent(unittest.TestCase):
    INFO = "something was logged"
    LEVEL = "CRITICAL"
    def setUp(self):
        self.event = events.Event(self.INFO, self.LEVEL)

if __name__ == '__main__':
    unittest.main()
