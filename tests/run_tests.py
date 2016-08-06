# Setup PYTHONPATH
import sys
import os
sys.path.append(os.path.join('..', 'diary'))

# Import test cases
import unittest
import events_test
import logdb_test
import formats_test

if __name__ == '__main__':
    # Setup test objects
    loader = unittest.TestLoader()
    load_func = loader.loadTestsFromTestCase
    all_tests = unittest.TestSuite()

    # Add tests
    all_tests.addTests(load_func(events_test.TestEvent))
    all_tests.addTests(load_func(logdb_test.TestLoggerDB))
    all_tests.addTests(load_func(formats_test.TestFormat))

    # Run tests
    results = unittest.TestResult()
    all_tests.run(results)

    if not(len(results.errors) == 0 and len(results.failures) == 0):
        for e in results.errors:
            print(''.join(map(str, e)))
        for f in results.failures:
            print(''.join(map(str, f)))
