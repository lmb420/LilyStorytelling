import speech_recognition as sr
from text_to_speech import *

r = sr.Recognizer()
r.pause_threshold = 1


def getInputString(targetStrings = None):                    
	s = None
	while( s == None):
		with sr.Microphone() as source:                 # use the default microphone as the audio source
                        r.energy_threshold = 2200
			audio = r.adjust_for_ambient_noise(source, duration = 0.5)
			print "Listening..."
			audio = r.listen(source)                    # listen for the first phrase and extract it into audio dataprint "heard"
		try:
			all_list = r.recognize_google_cloud(audio, preferred_phrases = targetStrings)
			s = ''+all_list
			# recognize speech using Google Speech Recognition
		except sr.UnknownValueError:                            # speech is unintelligible
			speak("Sorry, I didn't hear that.")
			s = None
	print(s)
	return str(s)
