import unittest
import datetime as dt
from diary import Event


class TestEvent(unittest.TestCase):
    INFO = "something was logged"
    LEVEL = "CRITICAL"

    def setUp(self):
        self.event = Event(self.INFO, self.LEVEL)

    def test_has_dt(self):
        self.assertIsNotNone(self.event.dt)

    def test_takes_arguments(self):
        given_dt = dt.datetime.now()
        self.event = Event(self.INFO, self.LEVEL, given_dt)
        self.assertEquals(self.event.dt, given_dt)
        self.assertEquals(self.event.info, self.INFO)
        self.assertEquals(self.event.level, self.LEVEL)


if __name__ == '__main__':
    unittest.main()
