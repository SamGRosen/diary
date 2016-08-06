# Setup PYTHONPATH
import sys
import os
sys.path.append(os.path.join('..', 'diary'))

# Import test dependencies
import unittest
import events_test

if __name__ == '__main__':
    # Setup test objects
    loader = unittest.TestLoader()
    load_func = loader.loadTestsFromTestCase
    all_tests = unittest.TestSuite()

    # Add tests
    all_tests.addTests(load_func(events_test.TestEvent))

    # Run tests
    results = unittest.TestResult()
    all_tests.run(results)

    assert len(results.errors) == 0 and len(results.failures) == 0
