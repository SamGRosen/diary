# Setup PYTHONPATH
import sys
import os
sys.path.append(os.path.join('..', 'diary'))

# Import test cases
import unittest
import events_test
import formats_test
import levels_test
import logdb_test

if __name__ == '__main__':
    # Setup test objects
    all_tests = unittest.TestSuite()
    loader = unittest.TestLoader()
    easy_load = lambda test_case: all_tests.addTests(
        loader.loadTestsFromTestCase(test_case))

    # Add tests
    easy_load(events_test.TestEvent)
    easy_load(formats_test.TestFormat)
    easy_load(levels_test.TestLevel)
    easy_load(logdb_test.TestLoggerDB)

    # Run tests
    results = unittest.TestResult()
    all_tests.run(results)

    if not(len(results.errors) == 0 and len(results.failures) == 0):
        for e in results.errors:
            print(''.join(map(str, e)))
        for f in results.failures:
            print(''.join(map(str, f)))
    else:
        print("All {} tests pass.".format(results.testsRun))
