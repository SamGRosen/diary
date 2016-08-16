import unittest
import datetime as dt
from diary import Event

DEFAULT_FORMATTER = "({level})({info})"
class FormattedEvent(Event):
    formatter = DEFAULT_FORMATTER


class TestEvent(unittest.TestCase):
    INFO = "something was logged"
    LEVEL = "CRITICAL"
    DEFAULT_FORMATTER = DEFAULT_FORMATTER

    def setUp(self):
        self.basicEvent = Event(self.INFO, self.LEVEL)
        self.formatted_event = FormattedEvent(self.INFO, self.INFO)
        FormattedEvent.set_formatter(DEFAULT_FORMATTER)

    def test_has_dt(self):
        event = Event(self.INFO, self.LEVEL)
        self.assertIsNotNone(self.basicEvent.dt)

    def test_takes_arguments(self):
        given_dt = dt.datetime.now()
        event = Event(self.INFO, self.LEVEL, given_dt)
        self.assertEquals(event.dt, given_dt)
        self.assertEquals(event.info, self.INFO)
        self.assertEquals(event.level, self.LEVEL)
        self.assertEquals(event.formatter, None)

    def test_func_formatter(self):
        def quick_format(e):
            return "({level})({text})".format(level = e.level,
                                              text = e.info)

        FormattedEvent.set_formatter(quick_format)

        event = FormattedEvent(self.INFO, self.LEVEL)

        self.assertEquals(event.formatted(), "({level})({text})".format(
            level = event.level, text = event.info))

        self.assertEquals(str(event), "({level})({text})".format(
            level=event.level, text=event.info))

        event.info = ""

        self.assertEquals(event.formatted(), "({level})({text})".format(
            level = event.level, text = event.info))

        self.assertEquals(str(event), "({level})({text})".format(
            level=event.level, text=event.info))

    def test_str_formatter(self):
        event = FormattedEvent(self.INFO, self.LEVEL)

        self.assertEquals(event.formatted(), "({level})({text})".format(
            level=event.level, text=event.info))

        self.assertEquals(str(event), "({level})({text})".format(
            level=event.level, text=event.info))

        self.assertEquals(event.formatter, DEFAULT_FORMATTER)

        event.info = ""

        self.assertEquals(event.formatted(), "({level})({text})".format(
            level=event.level, text=event.info))

        self.assertEquals(str(event), "({level})({text})".format(
            level=event.level, text=event.info))

    def test_bad_formatter(self):
        formatter = 5
        with self.assertRaises(ValueError,
            msg="Could not identify formatter {}".format(formatter)):
            event = FormattedEvent(self.INFO, self.LEVEL)
            event.set_formatter(formatter)

    def test_set_formatter(self):
        class MutableFormattedEvent(Event):
            pass
        event = MutableFormattedEvent(self.INFO, self.LEVEL)
        self.assertIsNone(event.formatter)
        with self.assertRaises(AttributeError,
            msg="Event instance has no attribute 'formatted'"):
            event.formatted()

        event.set_formatter("({level})({info})")
        self.assertEquals(event.formatted(), "({level})({info})".format(
            level=event.level, info=event.info))

        event.set_formatter(None)
        self.assertIsNone(event.formatter)

    def test_no_formatter(self):
        self.assertIsNone(self.basicEvent.formatter)

        with self.assertRaises(AttributeError,
            msg="{} does not have a valid formatter: {}".format(
                self.basicEvent, self.basicEvent.formatter)
            ):
            self.basicEvent.formatted()

        self.assertEquals(str(self.basicEvent), repr(self.basicEvent))

    def test_set_level(self):
        mock_level = lambda: None
        event_to_change = Event(self.INFO, mock_level)
        self.assertIs(event_to_change.level, mock_level)
        self.assertEquals(event_to_change.level_str, mock_level.__name__.upper())

        new_level = lambda: None
        event_to_change.set_level(new_level)
        self.assertIs(event_to_change.level, new_level)
        self.assertEquals(event_to_change.level_str, new_level.__name__.upper())



if __name__ == '__main__':
    unittest.main()
