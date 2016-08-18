from diary import Diary, DiaryDB, Event, levels, log_level, formats
import unittest
import shutil
import os

@log_level
def critical(event):
    event.info = "!!" + event.info + "!!"

def emergency_format(event):
    return "!!!|{dt}|{level}|{info}|!!!".format(
        dt=event.dt, level=event.level_str, info=event.info
    )


class UserEvent(Event):
    formatter = "[{level_str}]|{dt}|{info}|{user_name}"

    def __init__(self, info, level=None, user_name=""):
        Event.__init__(self, info, level)
        self.user_name = user_name


class UserActivityDB(DiaryDB):
    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS user_activity
                                (inputDT TIMESTAMP, level TEXT, log TEXT, user TEXT)''')

    def log(self, event):
        with self.conn:
            self.cursor.execute('''
                                INSERT INTO user_activity(inputDT, level, log, user)
                                                 VALUES(?, ?, ?, ?)''',
                                (event.dt, event.level_str, event.info, event.user_name))


class TestAPI(unittest.TestCase):
    API_DIR = os.path.join(os.path.dirname(__file__),
                                 'testing_dir', 'api_testing')
    INFO = "event was logged"
    LEVEL = "LEVEL"

    @classmethod
    def setUpClass(cls):
        if not os.path.exists(cls.API_DIR):
            os.mkdir(cls.API_DIR)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.API_DIR)

    def test_custom_level(self):
        logger = Diary(os.path.join(self.API_DIR))
        logger.log("URGENT ATTENTION NEEDED", level=critical)
        logger.close()
        with open(logger.log_file.name) as f:
            self.assertEquals(f.readline(), formats.standard(logger.last_logged_event) + '\n')

    def test_custom_format_init(self):
        logger = Diary(self.API_DIR, log_format=emergency_format,
                       file_name="EmergencyLogs2.log", db_name="EmergencyDB2.db")

        logger.log(self.INFO)
        logger.close()
        with open(logger.log_file.name) as f:
            self.assertEquals(f.readline(), emergency_format(logger.last_logged_event) + '\n')

        with DiaryDB(logger.db_file.name) as db:
            db.assert_event_logged(self.INFO)

    def test_custom_format_event(self):
        class FormattedEvent(Event):
            formatter = "|{dt}|{info}|{level_str}|"

        logger = Diary(self.API_DIR, file_name="formatted.txt", db_name="formattedDB.db", event=FormattedEvent, async=False)
        logger.log(self.INFO)
        logger.close()

        with open(logger.log_file.name) as f:
            self.assertEquals(f.readline(), logger.last_logged_event.formatted() + '\n')

        with DiaryDB(logger.db_file.name) as db:
            db.assert_event_logged(self.INFO, "INFO")

    def test_custom_event(self):
        logger = Diary(self.API_DIR, file_name="UserEvents.txt", event=UserEvent)
        logger.log("Start logging")
        logger.info(UserEvent(self.INFO, user_name="admin"))  # Directly log events
        logger.close()

        with open(logger.log_file.name) as f:
            contents = f.read()
            self.assertTrue("Start logging" in contents)
            self.assertTrue(logger.last_logged_event.formatted() in contents)

        with DiaryDB(logger.db_file.name) as db:
            db.assert_event_logged(self.INFO, "INFO")

    def test_custom_db_formatted_event(self):
        logger = Diary(self.API_DIR, file_name="withdb.txt", db_name="user_events.db",
                       db=UserActivityDB, event=UserEvent)

        logger.log("Starting app")
        event_to_log = UserEvent("Super user logged in", user_name="super")
        logger.debug(event_to_log)
        logger.close()
        with open(logger.log_file.name) as f:
            contents = f.read()
            self.assertTrue("Starting app" in contents)
            self.assertTrue(logger.last_logged_event.formatted() in contents)

        with UserActivityDB(logger.db_file.name) as db:
            entries = db.cursor.execute("""SELECT * FROM user_activity WHERE
                                        log=(?) AND level LIKE (?) AND user=(?)""",
                              (event_to_log.info, event_to_log.level_str, event_to_log.user_name))
            entry = entries.fetchone()

            self.assertEquals(entry[0], event_to_log.dt)
            self.assertEquals(entry[1], event_to_log.level_str)
            self.assertEquals(entry[2], event_to_log.info)
            self.assertEquals(entry[3], event_to_log.user_name)

    def test_custom_everything(self):
        logger = Diary(self.API_DIR, file_name="withlevel.txt", db_name="level_user_events.db",
                       db=UserActivityDB, event=UserEvent)
        event_to_log = UserEvent(self.INFO, user_name="super")
        logger.log(event_to_log, level=critical)
        logger.close()
        with open(logger.log_file.name) as f:
            self.assertTrue(event_to_log.formatted() + '\n', f.readline())

        with UserActivityDB(logger.db_file.name) as db:
            entries = db.cursor.execute("""SELECT * FROM user_activity WHERE
                                        log=(?) AND level LIKE (?) AND user=(?)""",
                              (event_to_log.info, event_to_log.level_str, event_to_log.user_name))
            entry = entries.fetchone()

            self.assertEquals(entry[0], event_to_log.dt)
            self.assertEquals(entry[1], event_to_log.level_str)
            self.assertEquals(entry[2], event_to_log.info)
            self.assertEquals(entry[3], event_to_log.user_name)

if __name__ == '__main__':
    unittest.main()
