"""
Created on November 4, 2013

@author: Claymore
We have the profiler class, which creates and manages a list of 'profiles'
for the kernel. Each 'profile' has a name and holds onto data about that
particular part of the kernel.
"""
from profile import Profile


class Profiler(object):

    def __init__(self):
        self.profiles = []

    def profile(self, name):
        #check to see if we have a profile in our list with that name, if we do
        #pull up the data there already and append the new data. Otherwise
        #create a new profile and add it to the list.
        for profile in self.profiles:
            if not profile.isValid:
                if profile.name is name:
                    pass
                    #update info in profile
        #create new profile
        self.profiles.append(Profile(name))
