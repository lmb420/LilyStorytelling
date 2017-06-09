"""This class acts as a wrapper for activity functions that serve as the
interaction between user and story. By passing both the function reference
and the necessary parameters, it allows the story to dynamically call the
correct activity when necessary."""
from player import Player

class Activity(object):
    def __init__(self, func, *args):
        self.func = func
        self.args = args

    def doActivity(self, player):
        #node is set to completed BEFORE the activity is executed
        player.completed[player.location.name] = True
        if len(self.args) == 0:
            return self.func(player)
        else:
            return self.func(player, self.args)
