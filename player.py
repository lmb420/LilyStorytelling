from text_to_speech import *
from speech_recog import *
from nltk.stem.snowball import SnowballStemmer

stemmer = SnowballStemmer('english')

yes_syns = [['yes', 'yup', 'yeah', 'yea', 'indeed', 'sure']]

class Player:
    def __init__(self, list_of_StoryNodes):
        #requires that first StorNode in list is start node
        self.location = list_of_StoryNodes[0]
        self.completed = {}

        self.name = self.setName()

        #put all nodes in story in dictionary as not completed
        for node in list_of_StoryNodes:
            self.completed[node.name] = False

    def get_target(self, s, targets, targets_syn):  #this method looks for a one word target in user's speech
        #check if user says exactly the node's name
        temp = []
        for i in targets_syn: 
            temp2 = []
            for j in i:
                temp2.append(stemmer.stem(j))
            temp.append(temp2)
        targets_syn = temp
        
        for t in targets:
            if s.lower() == t.lower():
                return t
        
        s = s.lower().split()
        temp = []
        for i in s:
            temp.append(stemmer.stem(i))
        s = temp
        for word in s:
            for t in targets_syn:
                if word in t:
                    return targets[targets_syn.index(t)]
        return None

    def setName(self):
        yes = 'no'
        while self.get_target(yes, ['yes'], yes_syns) != 'yes':
            speak("What is your name?")
            s = getInputString()
            speak("Is your name " + s + "?")
            yes = getInputString(yes_syns[0])
        return s

    
