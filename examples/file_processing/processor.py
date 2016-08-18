from diary import Diary, DiaryDB, Event
from random import randint
import os

if not os.path.exists("file_info"):
    os.mkdir("file_info")

def process_file(f):
    """ Simulate success """
    return randint(1,3)


class FileProcessEvent(Event):
    RESULT_TO_STR = ("Success", "Unsuccessful", "Error", "Could not process")
    formatter = "|{dt}|{level_str}|{result_str}|{path} : {info}"

    def __init__(self, info, success, path, level=None):
        Event.__init__(self, info, level)
        self.success = success
        self.path = path

        if self.success >= 1 and self.success <= 3:
            self.result_str = self.RESULT_TO_STR[self.success - 1]
        else:
            self.result_str = self.RESULT_TO_STR[-1]


class FileProcessDB(DiaryDB):
    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS files
            (inputDT TIMESTAMP, level TEXT, info TEXT, path TEXT, success INT)
                            ''')

    def log(self, event):
        with self.conn:
            self.cursor.execute('''
                INSERT INTO files(inputDT, level, info, path, success)
                VALUES(?, ?, ?, ?, ?)''',
                (event.dt, event.level_str, event.info, event.path, event.success))

logger = Diary("file_info", db_name="file_processes.db", db=FileProcessDB,
               file_name="file_processes.log")

target_dir = "data"
# files_to_process = os.listdir(target_dir)
files_to_process = range(10) # We will pretend the numbers up to 10 are files


for f in files_to_process:
    if process_file(f) == 1:
        e = FileProcessEvent("Success!", 1, f)
        logger.info(e)
    elif process_file(f) == 2:
        e = FileProcessEvent("The goal was not achieved", 2, f)
        logger.warn(e)
    elif process_file(f) == 3:
        e = FileProcessEvent("An error occurred", 3, f)
        logger.error(e)
    else:
        e = FileProcessEvent("Could not process file", -1, f)
        logger.debug(e)

logger.close()

with DiaryDB(logger.db_file.name) as db:

    entries = db.cursor.execute('''
                SELECT * FROM files
                ''')
    for row in entries:
        print(row)

