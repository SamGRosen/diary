from diary import levels
import unittest

report_count = 0


def reporter(event):
    global report_count
    report_count += 1


@levels.level
def mock_level(event, repeats, double_repeats=False):
    return event * repeats * (1 + int(double_repeats))


class TestLevel(unittest.TestCase):
    INFO = "!"
    LEVEL = mock_level

    def setUp(self):
        self.report_count = report_count

    def test_reporter(self):
        output = mock_level(self.INFO, reporter, 1)

        self.assertEquals(self.report_count + 1, report_count)

    def test_level_return(self):
        output = mock_level(self.INFO, reporter, 1)

        self.assertEquals(output, self.INFO)

    def test_level_args(self):
        output = mock_level(self.INFO, reporter, 2)

        self.assertEquals(output, "!!")

    def test_level_kwargs(self):
        output = mock_level(self.INFO, reporter, 1, True)

        self.assertEquals(output, "!!")

    def test_level_both_args(self):
        output = mock_level(self.INFO, reporter, 2, True)

        self.assertEquals(output, "!!!!")

    def test_placeholder_levels(self):
        levels.debug(self.INFO, reporter)
        levels.warn(self.INFO, reporter)
        levels.info(self.INFO, reporter)

        self.assertEquals(self.report_count + 3, report_count)

    def test_error_level(self):
        with self.assertRaises(Exception):
            levels.error(self.INFO, reporter, raises=True)

        self.assertEquals(self.report_count + 1, report_count)

    def test_error_level_specific(self):
        with self.assertRaises(ValueError, msg=self.INFO):
            levels.error(self.INFO, reporter, raises=True, e_type=ValueError)

        self.assertEquals(self.report_count + 1, report_count)

if __name__ == '__main__':
    unittest.main()
