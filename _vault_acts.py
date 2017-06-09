from player import Player
from speech_recog import *
from text_to_speech import *
from story_node import StoryNode
import random

#each method must pass player as a parameter
#and return None, the name of the next node, or "quit"

def main_act(player):
    current = player.location
    if "key" in player.completed.keys():
        speak("You open the door. The End.")
        return "quit"
    for child in current.children:
        if player.completed[child.name] == True:
            speak("You still haven't found the key. Keep looking in either room.")
            return None
    speak("Welcome. You awake and find yourself in a dimly lit room. There is nothing but a vault in here, but you don't have a key. There is a door on either side of the room.")
    speak("Which door do you go through? Left or right?")
    return None

def left_act(player):
    speak("Look! There's a box in the corner over there!")
    speak("You look inside and find the key.")
    player.completed["key"] = True
    return "main"

def right_act(player):
    speak("Well, this just looks like an empty room. Let's go back.")
    return "main"
