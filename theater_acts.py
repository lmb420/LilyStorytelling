from player import Player
from speech_recog import *
from text_to_speech import *
import webbrowser
import win32com.client
import time
from nltk.stem.snowball import SnowballStemmer

stemmer = SnowballStemmer('english')

#activities must return None or the name of the next node or "quit"

def theaterActivity(player):
    speak("Hello! Welcome to the Lehigh Valley Movie Theater")
    speak("You can go to the box office and get your ticket")
    speak("Or you can go to the concessions for some snacks.")
    speak("Where would you like to go, " + player.name + "?")

    return None

def boxOfficeActivity(player, box_args):
    speak("Welcome to the box office")
    speak("Which movie would you like to watch?")
    speechOptions = []
    for i in range(len(box_args[0])):
       speak(str(box_args[0][i]))
       speechOptions.append(str(box_args[0][i]))
    movieChoice = getInputString(speechOptions)
    movie_index = inList(box_args[0], movieChoice)
    while  movie_index == -1:
        speak("Sorry, we don't have that movie. Pick another.")
        for i in range(len(box_args[0])):
            speak(str(box_args[0][i]))
        movieChoice = getInputString(speechOptions)
        movie_index = inList(box_args[0], movieChoice)
    player.completed["ticket"] = box_args[0][movie_index]
    speak("Here's your ticket. Enjoy the show.")
    speak("Would you like to go to the concessions?")
    speak("Or would you like to go to the ticket checker?")

    return None

def concessionsActivity(player, menu):
    done = False

    speechOptions = []
    for i in range(len(menu[0])):
        speechOptions.append(str(menu[0][i]))

    speak("What can I get for you?")
    while not done:
        for i in range(len(menu[0])):
            if not menu[0][i].lower() in player.completed.keys():
                speak(str(menu[0][i]))
        menuChoice = getInputString(speechOptions)
        menu_index = inList(menu[0], menuChoice)
        while menu_index == -1:
            speak("Sorry, we don't have that. Pick another.")
            menuChoice = getInputString(speechOptions)
            menu_index = inList(menu[0], menuChoice)
        if "finished" in menuChoice.lower().split():
            done = True
        else:
            player.completed[menu[0][menu_index]] = True
            speak("Can I get anything else for you?")
    speak("Thank you. Next please!")

    speak("If you do not have your ticket yet, go to the box office")
    speak("Otherwise you can go to the ticket checker.")

    return None

def ticketCheckerActivity(player):
    speak("Hello, ticket please.")
    if player.completed["ticket"].lower() == "inside out":
        speak("Inside Out is in theater 3 A, enjoy the show!")
    if player.completed["ticket"].lower() == "tomorrowland":
        speak("Tomorrowland is in theater 1 D, enjoy your movie!")
    if player.completed["ticket"].lower() == "minions":
        speak("Minions is in theater 3 B, enjoy the show!")
    if player.completed["ticket"].lower() == "home":
        speak("Home is in theater 1 A, enjoy your movie!")
    speak("Say movie to sit down and watch.")

    return None

def movieActivity(player):
	speak("Please power off your cellular devices.")
	speak("Sit back, relax and enjoy the show.")
	win32com.client.Dispatch("WScript.Shell").SendKeys('{ESC}')
	if player.completed["ticket"].lower() == "inside out":
		webbrowser.open("https://www.youtube.com/watch?v=_MC3XuMvsDI", new=1)
		fullscreen(130)

	if player.completed["ticket"].lower() == "tomorrowland":
		webbrowser.open("https://www.youtube.com/watch?v=1k59gXTWf-A", new=1)
		fullscreen(132)
		
	if player.completed["ticket"].lower() == "minions":
		webbrowser.open("https://www.youtube.com/watch?v=eisKxhjBnZ0", new=1)
		fullscreen(167)
		
	if player.completed["ticket"].lower() == "home":
		webbrowser.open("https://www.youtube.com/watch?v=MyqZf8LiWvM", new=1)
		fullscreen(150)
		
	return "quit"

#checks if user says a target phrase in a longer sentence (phrase can be multiple words)
def inList(lst, s):
    for x in lst:                   #if you say exactly phrase in list
        if s.lower() == x.lower():
            return lst.index(x)
    if "quit" in s.lower().split(): 
        return None
    s = s.lower().split()           #check if you said phrase inside a longer sentence
    temp = []
    for i in s:                     #get root word of user input
        temp.append(stemmer.stem(i))
    s = temp
    for l in lst:                   #for every element in the (movie, food)
        count = 0
        words = l.lower().split()
        for w in words:             #for every word in l(movie title, food name)
            w = stemmer.stem(w)     #compare root words, to increase generaltiy
            if w in s:              #if that word is in what you said
                count += 1
        if count == len(words):      #if you said every word in l
            return lst.index(l)
    return -1
        

def fullscreen(length):
	time.sleep(10)
	win32com.client.Dispatch("WScript.Shell").SendKeys('f')
	time.sleep(length)
	win32com.client.Dispatch("WScript.Shell").SendKeys('f')
	win32com.client.Dispatch("WScript.Shell").SendKeys('%{F4}',0)
       
