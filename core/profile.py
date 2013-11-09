"""
Created on November 5, 2013

@author: Claymore
"""
import cProfile
import os
import pstats

if not os.path.exists("profiles"):
            os.makedirs("profiles")


class Profiler(object):
    def __init__(self):
        self.profiles = []
        self.stats = pstats.Stats()

    def add(self, temp):
        for each in self.profiles:
            pass

profiler = Profiler()


def profile(func):
    """
    profile is a Decorator for functions and classes that wraps them in the Profile() function
    in cProfile. It outputs that data into a Stats object.
    """
    def wrapper(*args, **kwargs):
        filename = "profiles/" + func.__name__ + ".profile"
        print func.__name__
        prof = cProfile.Profile()
        results = prof.runcall(func, *args, **kwargs)
        profiler.add(prof)
        prof.dump_stats(filename)
        return results
    return wrapper


