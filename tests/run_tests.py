# Setup PYTHONPATH
import sys, os, shutil
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

# Import test cases
import unittest
import api_test
import diary_test
import events_test
import formats_test
import levels_test
import logdb_test
import logthread_test

if __name__ == '__main__':
    cleanup = True
    TEST_DIR = os.path.join(os.path.dirname(__file__), 'testing_dir')
    # Setup temp directory
    if not os.path.exists(TEST_DIR):
        os.mkdir(TEST_DIR)

    # Setup test objects
    all_tests = unittest.TestSuite()
    loader = unittest.TestLoader()
    easy_load = lambda test_case: all_tests.addTests(
        loader.loadTestsFromTestCase(test_case))

    # Add tests
    easy_load(api_test.TestAPI)
    easy_load(diary_test.TestDiary)
    easy_load(events_test.TestEvent)
    easy_load(formats_test.TestFormat)
    easy_load(levels_test.TestLevel)
    easy_load(logdb_test.TestDiaryDB)
    easy_load(logthread_test.TestDiaryThread)

    # Run tests
    results = unittest.TestResult()
    all_tests.run(results)

    if not (len(results.errors) == 0 and len(results.failures) == 0):
        for e in results.errors:
            print(''.join(map(str, e)))
        for f in results.failures:
            print(''.join(map(str, f)))
    else:
        print("All {} tests pass.".format(results.testsRun))

    if cleanup:
        shutil.rmtree(TEST_DIR)