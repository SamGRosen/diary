import os, shutil
import unittest
import command_test

if __name__ == '__main__':
    test_directory = os.path.join(os.path.dirname(__file__), 'testing_dir')
    if not os.path.exists(test_directory):
        os.mkdir(test_directory)

    tests = unittest.TestSuite()
    loader = unittest.TestLoader()
    easy_load = lambda test_case: tests.addTests(loader.loadTestsFromTestCase(test_case))

    easy_load(command_test.SqliteTest)

    results = unittest.TestResult()
    tests.run(results)

    failure = False
    if not (len(results.errors) == 0 and len(results.failures) == 0):
        for e in results.errors:
            print(''.join(map(str, e)))
        for f in results.failures:
            print(''.join(map(str, f)))
        failure = True
    else:
        print("All {} tests pass.".format(results.testsRun))

    shutil.rmtree(test_directory)

    if failure:
        raise AssertionError("Not all tests passed")
