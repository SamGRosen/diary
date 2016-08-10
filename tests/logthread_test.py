from diary import Diary, DiaryDB, DiaryThread
import unittest
import time
import os


class TestDiaryThread(unittest.TestCase):
    INFO = "event was logged"
    TEMP_DB = "db_test.db"
    TRIALS = 3
    count = 0

    def setUp(self):
        self.log = Diary("testing_dir", file_name="thread_test.txt",
                         db_name=self.TEMP_DB, async=True)

    @classmethod
    def tearDownClass(cls):
        os.remove(os.path.join("testing_dir", cls.TEMP_DB))

    def test_timer(self):
        def log_counter():
            self.count += 1
            self.log.log("event " + str(self.count))

        self.log.set_timer(1, log_counter)

        time.sleep(self.TRIALS + .1)

        self.log.close()

        with DiaryDB(self.log.db_file.name) as db:
            db.assert_event_logged("event " + str(self.count))

    def test_timer_with_args(self):
        def log_arg(arg):
            self.log.log(arg)

        self.log.set_timer(1, log_arg, self.INFO)

        time.sleep(self.TRIALS + .1)

        self.log.close()

        with DiaryDB(self.log.db_file.name) as db:
            entries = db.cursor.execute(
                '''SELECT * FROM logs WHERE log=(?)
                AND level LIKE (?) ORDER BY
                inputDT ASC LIMIT (?)''',
                (self.INFO, '%', self.TRIALS))

            for i in range(self.TRIALS):
                self.assertTrue(entries.fetchone())

    def test_timer_with_kwargs(self):
        repeats = 10
        def log_kwarg(s, repeats=2):
            self.log.log(s * repeats)

        self.log.set_timer(1, log_kwarg, self.INFO, repeats=repeats)

        time.sleep(self.TRIALS + .1)

        self.log.close()

        with DiaryDB(self.log.db_file.name) as db:
            entries = db.cursor.execute(
                '''SELECT * FROM logs WHERE log=(?)
                AND level LIKE (?) ORDER BY
                inputDT ASC LIMIT (?)''',
                (self.INFO * repeats, '%', self.TRIALS))

            for i in range(self.TRIALS):
                self.assertTrue(entries.fetchone())

    def test_timer_all_args(self):
        params = (self.INFO, "abc", "def", "123")
        def log_joined(*args):
            self.log.log(' '.join(args))

        self.log.set_timer(1, log_joined, *params)

        time.sleep(self.TRIALS + .1)

        self.log.close()

        with DiaryDB(self.log.db_file.name) as db:
            entries = db.cursor.execute(
                '''SELECT * FROM logs WHERE log=(?)
                AND level LIKE (?) ORDER BY
                inputDT ASC LIMIT (?)''',
                (' '.join(params), '%', self.TRIALS))

            for i in range(self.TRIALS):
                self.assertTrue(entries.fetchone())
if __name__ == '__main__':
    unittest.main()
