from diary import Event, formats
import datetime as dt
import unittest


class TestFormat(unittest.TestCase):
    INFO = "event is logged"
    LEVEL = "CRITICAL"
    TIMESTAMP = dt.datetime(1901, 2, 3, 4, 5, 6)
    SIMPLE_EVENT = Event(INFO, LEVEL, TIMESTAMP)

    def setUp(self):
        pass

    def test_standard(self):
        output = formats.standard(self.SIMPLE_EVENT)
        self.assertEquals(output,
                          "[CRITICAL]:[1901-02-03 04:05:06]: event is logged")

    def test_min(self):
        output = formats.minimal(self.SIMPLE_EVENT)
        self.assertEquals(output,
                          "CRITICAL: 02/03/01 04:05:06: event is logged")

    def test_alarms(self):
        output = formats.alarms(self.SIMPLE_EVENT)
        self.assertEquals(output,
                          " - CRITICAL - 1901-02-03 04:05:06 - event is logged - ")

        output = formats.alarms(Event(
            self.INFO, 'ERROR', self.TIMESTAMP))
        self.assertEquals(output,
                          "!!!ERROR!!!1901-02-03 04:05:06!!!event is logged!!!")

    @unittest.skip("May fail based on location because different date format")
    def test_easy_read(self):
        output = formats.easy_read(self.SIMPLE_EVENT)
        self.assertEquals(output,
                          "|CRITICAL| On 02/03/01 @ 04:05.06AM | event is logged")


if __name__ == '__main__':
    unittest.main()
