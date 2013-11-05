'''
Created on November 4, 2013

@author: Claymore
We have the profiler class, which creates and manages a list of 'profiles'
for the kernel. Each 'profile' has a name and holds onto data about that
particular part of the kernel.
'''

class profiler(object):

    def __init__(self):
        self.profiles = []

    def profile(self, name):
        #check to see if we have a profile in our list with that name, if we do
        #pull up the data there already and append the new data. Otherwise
        #create a new profile and add it to the list.

