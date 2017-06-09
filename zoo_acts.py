from player import Player
from speech_recog import *
from text_to_speech import *
import random
from run_gif import *

#activities must return None or the name of the next node or "quit"

yes = ['yes']
yes_syns = [['yes', 'yup', 'yeah', 'yea', 'indeed', 'sure']]


def entranceAct(player):
	speak("Hi " + player.name + ". Welcome to the San Diego Zoo!")
	x = random.random()
	if x > 0.99:
		speak("Oh no! You forgot your wallet!")
		speak("The End.")
		return "quit"
	speak("We have a bunch of great exhibits for you today.")
	speak("Say the name of the animal you want to see to go there.")
	speak("Say goodbye at any time to leave the zoo.")
	speak("Have a fun time!")
	speak("Where should we start?")
	sayChildren(player)
    #for x in player.location.children:
    #    speak(x.name)
	return None
    
def parking_lotAct(player):
    speak("You've reached the parking lot.")
    x = random.random()
    if x > 0.75:
            speak("Oh no! Some monkeys escaped.")
            speak("They have gotten into your car!")
            runGif("ZooGifs/monkey_steals_wheel_cover.gif")
            speak("Those thieves got away!")
    speak("We get new exhibits often, so come back soon to see something new.")
    speak("It's time to go home now. The End.")
    return "quit"

def monkeyAct(player):
    speak("Look at the cute monkeys!")
    runGif("ZooGifs/monkey.gif")
    speak("Where to now?")
    sayChildren(player)
    return None

def elephantAct(player):
    speak("Elephants are my favorite. Check out its cool painting.")
    runGif("ZooGifs/GIF-Elephant-painting.gif")
    speak("What's next, " + player.name + "?")
    sayChildren(player)
    return None

def lionAct(player):
    speak("Look, that lion must be hungry.")
    runGif("ZooGifs/lion_tries_to_grab_baby.gif")
    speak("Where would you like to go now?")
    sayChildren(player)
    return None
    
def penguinAct(player):
    speak("That penguin is a jokester.")
    runGif("ZooGifs/penguin.gif")
    x = random.random()
    if x > 0.25:
        speak("Great timing. They are feeding the penguins.")
        speak("Should we stay and watch?")
        s = getInputString(yes_syns[0])
        if player.get_target(s, yes, yes_syns) == 'yes': 
            runGif("ZooGifs/penguin_feeding.gif")
    speak("Which animal do you want to see now?")
    sayChildren(player)
    return None

def tigerAct(player):
    speak("Look at that bird flying into the tiger enclosure.")
    runGif("ZooGifs/tiger_and_bird.gif")
    x = random.random()
    if x > 0.5:
        speak("There are baby tigers too!")
        speak("Do you want to look?")
        s = getInputString(yes_syns[0])
        if player.get_target(s, yes, yes_syns) == 'yes': 
            runGif("ZooGifs/baby_tiger.gif")
    speak("What exhibit should we go to from here?")
    sayChildren(player)
    return None

def otterAct(player):
    speak("Check it out - there are otters playing basketball!")
    runGif("ZooGifs/otter_basketball.gif")
    x = random.random()
    if x > 0.6:
        speak("Look! There is a special great white shark exhibit!")
        speak("Do you want to stop?")
        s = getInputString(yes_syns[0])
        if player.get_target(s, yes, yes_syns) == 'yes': 
            runGif("ZooGifs/white_shark_feeding.gif")
    speak("Which of these animals do you want to see next?")
    sayChildren(player)
    return None

def pandaAct(player):
    speak("Look at all of the silly pandas!")
    runGif("ZooGifs/pandas.gif")
    speak("Where do you want to go now, " + player.name + "?")
    sayChildren(player)
    return None

def sayChildren(player):
	for x in range(0, len(player.location.children) - 1):
		speak(player.location.children[x].name)

