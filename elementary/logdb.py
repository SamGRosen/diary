import sqlite3


class LoggerDB():

    def __init__(self, path):
        self.conn = sqlite3.connect(path)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
                            CREATE TABLE logs
                                (inputTime DATE, level TEXT, log TEXT)
                            ''')

    def log(self, text, level=INFO):
        l = level(text)
        self.cursor.execute('''
                            INSERT INTO logs(log) VALUES(?)
                            ''', (,))
