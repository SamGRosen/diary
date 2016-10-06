from timeit import default_timer
from functools import wraps
from diary import Diary
import os
import shutil

TEST_DIR = os.path.join(os.path.dirname(__file__), 'performance_test_dir')
TRIAL_COUNT = 1000
def timed(timed_function):

    @wraps(timed_function)
    def timed_wrapper(trials=TRIAL_COUNT):
        start = default_timer()
        timed_function(trials)
        total_time = default_timer() - start
        print("Completed {} in {} seconds ({} trials)".format(
            timed_function.__name__, total_time, trials
        ))
        print("\t {} seconds per trial".format(total_time/trials))

    return timed_wrapper

def create_test_dir():
    try:
        os.mkdir(TEST_DIR)
    except OSError:
        pass

def cleanup():
    shutil.rmtree(TEST_DIR)

@timed
def test_simple_performance(trials=TRIAL_COUNT):
    simple_logger = Diary(TEST_DIR, file_name="simple.log", db_name="simple.db", async=True)
    for i in range(trials):
        simple_logger.log("info")
    simple_logger.close()


@timed
def test_simple_performance_no_async(trials=TRIAL_COUNT):
    simple_logger = Diary(TEST_DIR, file_name="simple_no_async.log", db_name="simple_no_async.db", async=False)
    for i in range(trials):
        simple_logger.log("info")

@timed
def test_simple_performance_no_db(trials=TRIAL_COUNT):
    simple_logger = Diary(os.path.join(TEST_DIR, "simple_no_db.log"), async=True)
    for i in range(trials):
        simple_logger.log("info")
    simple_logger.close()

@timed
def test_simple_performance_no_log_file(trials=TRIAL_COUNT):
    simple_logger = Diary(os.path.join(TEST_DIR, "simple_no_log.db"), async=True)
    for i in range(trials):
        simple_logger.log("info")
    simple_logger.close()

if __name__ == '__main__':
    create_test_dir()
    test_simple_performance()
    test_simple_performance_no_async()
    test_simple_performance_no_db()
    test_simple_performance_no_log_file()
    cleanup()

