from story_node import StoryNode
from player import Player
#import ctypes
#import time
#lib = ctypes.CDLL('FakeInputWin')
from speech_recog import *
from text_to_speech import *
from nltk.stem.snowball import SnowballStemmer

"""This class represents a story which is built from StoryNodes
and a Player. Given a list of nodes, with the first being the starting node
in the story, it is able to walk between nodes. When a node is visited it
is added as a string in the dictionary of the player. Additionally, any tokens
that are prerequisites for later nodes are added. For example, a box office
node, when visited, will add a 'ticket' to the completed dictionary in player"""

stemmer = SnowballStemmer('english')

class Story(object):
    # set up player and story
    def __init__(self, a_player, the_nodes):
        self.player = a_player
        self.nodes = the_nodes
    # returns child node given by players response, s, if s is a child of the current node
    # otherwise the current node is returned because s is not a valid choice
    def getNextNode(self, current, s):
        #check if user says exactly the node's name
        for child in current.children:
            if s.lower() == child.name.lower():
                return child

        #checks if user says node's name in a longer sentence (node's name can be multiple words)
        stems = []                          #get root of every word to compare                    
        for word in s.lower().split():
            stems.append(stemmer.stem(word))
        
        if "quit" in s:
            return None

        for c in current.children_stems:     #for every child of current
            count = 0
            for stem in c:                #for every word in current.child's name
                if stem in stems:         #if the user said that word
                    count += 1          #success, look for next word in name, if applicable
                                        #otherwise, check next child
            if count == len(c):         #if the user said every word in current.child's name
                return current.children[current.children_stems.index(c)]
        return current
        
    def prereqsValid(self, player, newCurrent):
        for prereq in newCurrent.prereqs:
            if not prereq in player.completed.keys() or player.completed[prereq] == False:
                speak("You do not have your " + prereq + " yet! Choose somewhere else to go.")
                return False
        return True
                
    # moves the player to the next node in the story based on getNextNode
    def nextNode(self, player):
	# sets current working node to the players present position
        current = player.location
		
	# automated greeting for node 
	# TODO develop better automated 'welcome'
        #speak("Welcome to the " + current.name)
		
	# a node can have multiple activities associated with it
	# each activity must be completed before moving to next node
        s = current.activity.doActivity(player)
	
		
	# prompts user to choose next node out of options
        #speak("You are at the " + current.name + ". Where would you like to go now?")
        #self.printChildren(current)

	#if activity method did not return the next node, then get user's choice
        speechOptions = []
        for c in current.children:
            speechOptions.append(c.name)
            
        if s == None:
            s = getInputString(speechOptions)
	# check if a valid choice has been made or if getNextNode has returned the current working node
        newCurrent = self.getNextNode(current, s)
        while (not newCurrent == None) and (newCurrent == current or (not self.prereqsValid(player, newCurrent))):
            if newCurrent == current:
                speak("Sorry, that confused me. Please say one of the following:")
                for c in current.children:
                    speak(c.name)
            s = getInputString(speechOptions)
            newCurrent = self.getNextNode(current, s)
        #once a valid choice is made set current node then return it

        return newCurrent
    
            
    def walk(self, player):                         # function to 'play' the story
        while player.location != None:              # while there are still nodes to visit, visit them using nextNode
            player.location = self.nextNode(player)

    def printChildren(self, current):
        for index,child in enumerate(current.children):
            speak(child.name)


