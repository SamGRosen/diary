from diary import level, levels
import unittest

report_count = 0


def reporter(event):
    global report_count
    report_count += 1

@level
def mock_level(event, repeats, double_repeats=False):
    global result
    result = event * repeats * (1 + int(double_repeats))


class TestLevel(unittest.TestCase):
    INFO = "!"
    LEVEL = mock_level

    def setUp(self):
        self.report_count = report_count

    def test_reporter(self):
        mock_level(self.INFO, reporter, 1)

        self.assertEquals(self.report_count + 1, report_count)

    def test_level_return(self):
        mock_level(self.INFO, reporter, 1)

        self.assertEquals(result, self.INFO)

    def test_level_args(self):
        mock_level(self.INFO, reporter, 2)

        self.assertEquals(result, "!!")

    def test_level_kwargs(self):
        mock_level(self.INFO, reporter, 1, True)

        self.assertEquals(result, "!!")

    def test_level_both_args(self):
        mock_level(self.INFO, reporter, 2, True)

        self.assertEquals(result, "!!!!")

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
            levels.error(self.INFO, reporter, raises=True, e_type=ValueError, log_trace=False)

        self.assertEquals(self.report_count + 1, report_count)

if __name__ == '__main__':
    unittest.main()
