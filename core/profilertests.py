from time import sleep
import unittest
from profile import profile
import os
import pstats


@profile
def runner():
        sleep(1)


@profile
class ClassRunner(object):
    def __init__(self):
        self.runner()

    def runner(self):
        sleep(1)


class ProfileTests(unittest.TestCase):
    def setUp(self):
        pass

    def testFunctionDecoratorMakesProfile(self):
        runner()
        self.assertTrue(os.path.exists("profiles/runner.profile"))

    def testClassDecoratorMakesProfile(self):
        ClassRunner()
        self.assertTrue(os.path.exists("profiles/ClassRunner.profile"))

    def testMoreThanOneFile(self):
        for name in os.listdir("profiles"):
            print name
        self.assertGreater(1, len([name for name in os.listdir('profiles') if os.path.isfile(name)]))

if __name__ == '__main__':
    unittest.main()
