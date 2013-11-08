__author__ = 'Claymore'

import unittest
import profile
import profiler


class ProfileTests(unittest.TestCase):
    def setUp(self):
        self.profile = profile.Profile("test")

    def testName(self):
        self.assertEqual(self.profile.name, "test")

    def testStartTime(self):
        print self.profile.start()

    def testSomething(self):
        self.assertEqual(True, False)


class ProfilerTests(unittest.TestCase):
    def setUp(self):
        self.profiler = profiler.Profiler()

    def testAddProfile(self):
        self.profiler.profile("test")
        self.assertEqual(self.profiler.profiles[0].name, "test")


if __name__ == '__main__':
    unittest.main()
