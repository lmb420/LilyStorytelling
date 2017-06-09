from IPC import *
from nitepy import *
from poses import *
import threading
import thread
import sys
import clr
import numpy as np

clr.AddReference('FTCHpy')
import FTCHpy
ftch = FTCHpy.FTCHcalc()

followloss = -1 #the user that was lost while following
pickupfollow=False

lock = threading.Lock()
lock.acquire()
aspects = [[0,-1,-1,-1]] #person id,hips-head dist,sh dist,sh-elbow
skasps = [[0,-1,-1,-1]]	 #skeleton id, ...
shirts = [] #will contain elements like [0,range(0,192) ([user,shirt analysis result])
rightWave=False
leftWave =False
follow = False
stopfollow = False
pauseSkel = False
userOfInt=0
quits = False
e = threading.Event()
lock.release()

pose = poses()

personMappings = {} #dictionary holding mappings from multiple people to one person
personMappings[1]=0
curSkeletonPersonIDs = {} #dictionary where a skeletonID (not index) is paired with a personID
oldSkeletonPersonIDs = {} #old version of curSkeletonPersonIDs dictionary, used to check for changes
personIDAttempts = {} #dictionary where a skeletonID is paired with the number of attempts made to identify the person

gestGivenPID = -1 #personID of the user who provided a gesture

lib.loop(track)

MAX_GUESSES = 30 #maximum number of guesses the face identifier is allowed before a person is considered unrecognized
framecount = 0

lastrec = -11
def detect_motion():
	global framecount
	global curSkeletonPersonIDs
	global oldSkeletonPersonIDs
	global aspects
	global skasps
	global rightWave
	global leftWave
	global follow
	global stopfollow
	global pickupfollow
	global userOfInt
	global quits
	global track
	global gestGivenPID
	user = 0
	lstage = ["none"] #array of states for left wave.  Each stage is for one person.
	rstage = ["none"] #array of states for right wave.
	follstage = ["none"] #array of states for follow.
	stopfollstage = ["none"] #array of states for  stop follow.
	quitstage = ["none"]  #array of states for quit.
	lstate = [0]
	rstate = [0]
	follstate = [0]
	while True:
		e.wait()   #pauses thread if main thread flag is cleared
		lock.acquire()
		lib.loop(track)	 #grab a new 3D frame
		lock.release()
		#TODO check for monotonic approach to new poses using functions in poses class
		for user in range(0,lib.getUsersCount(track)):
			if len(lstage)<=user:
				lstage.append("none") #there is an additional user, we need more state variables
				rstage.append("none")
				follstage.append("none")
				quitstage.append("none")
				stopfollstage.append("none")
				lstate.append(0)
				rstate.append(0)
				follstate.append(0)
				
			if lstage[user]=="none":  #nothing has happened yet, check if the arm is in a position of interest
				if lib.getUserSkeletonL_HandX(track,user)-lib.getUserSkeletonL_ElbowX(track,user)>100:# or poses.LeftArmAboveLeftSh(pose,user)<200:
					if lib.getUserSkeletonL_HandY(track,user)-lib.getUserSkeletonL_ElbowY(track,user)>0:# or poses.LeftArmAboveLeftSh(pose,user)<200:
						lstage[user] = "ready"
						#lstate[user] = poses.LeftArmExtLeft(pose,user)
			if lstage[user]=="ready":#we hit one point of interest, move to the next if the arm has met the new POI
				if lib.getUserSkeletonL_ElbowX(track,user)-lib.getUserSkeletonL_HandX(track,user)>100:
					if lib.getUserSkeletonL_HandY(track,user)-lib.getUserSkeletonL_ElbowY(track,user)>0:
						lstage[user] = "none"
						lock.acquire()
						leftWave = True
						if lib.getUserID(track, user) in curSkeletonPersonIDs:
							gestGivenPID = curSkeletonPersonIDs[lib.getUserID(track, user)]
						else:
							gestGivenPID = -1
						sys.stderr.write("got left wave from user "+str(user) +"\n")
						lock.release()
			if lib.getUserSkeletonL_HandY(track,user)-lib.getUserSkeletonL_ElbowY(track,user)<0:# or lib.getUserSkeletonL_ElbowConf(track,user)<=0.5:
				lstage[user] = "none"#we hit a point that is un acceptable for this gesture, cancel it
				
			if rstage[user]=="none":#nothing has happened yet, check if the arm is in a position of interest
				if lib.getUserSkeletonR_HandX(track,user)-lib.getUserSkeletonR_ElbowX(track,user)<-100:
					if lib.getUserSkeletonR_HandY(track,user)-lib.getUserSkeletonR_ElbowY(track,user)>0:
						rstage[user] = "ready"
			if rstage[user]=="ready":#we hit one point of interest, move to the next if the arm has met the new POI
				if lib.getUserSkeletonR_ElbowX(track,user)-lib.getUserSkeletonR_HandX(track,user)<-100:
					if lib.getUserSkeletonR_HandY(track,user)-lib.getUserSkeletonR_ElbowY(track,user)>0:
						rstage[user] = "none"
						lock.acquire()
						rightWave = True
						if lib.getUserID(track, user) in curSkeletonPersonIDs:
							gestGivenPID = curSkeletonPersonIDs[lib.getUserID(track, user)]
						else:
							gestGivenPID = -1
						sys.stderr.write("got right wave from user "+str(user)+"\n")
						lock.release()
			if lib.getUserSkeletonR_HandY(track,user)-lib.getUserSkeletonR_ElbowY(track,user)<0 or lib.getUserSkeletonR_ElbowConf(track,user)<=0.5:
				rstage[user] = "none"#we hit a point that is un acceptable for this gesture, cancel it
				
			if follstage[user]=="none":#nothing has happened yet, check if the arm is in a position of interest
				if abs(lib.getUserSkeletonL_HandZ(track,user)-lib.getUserSkeletonR_HandZ(track,user))<100:
					if abs(lib.getUserSkeletonL_HandZ(track,user)-lib.getUserSkeletonL_ShZ(track,user))>300:
						follstage[user] = "ext"
			if follstage[user]=="ext":#we hit one point of interest, move to the next if the arm has met the new POI
				if abs(lib.getUserSkeletonL_HandZ(track,user)-lib.getUserSkeletonR_HandZ(track,user))<100:
					if abs(lib.getUserSkeletonL_HandZ(track,user)-lib.getUserSkeletonL_ShZ(track,user))<150:
						follstage[user]="none"
						lock.acquire()
						userOfInt = lib.getUserID(track,user)
						follow = True
						sys.stderr.write("got follow from user "+str(user)+"\n")
						lock.release()
			if abs(lib.getUserSkeletonL_HandZ(track,user)-lib.getUserSkeletonR_HandZ(track,user))>100 or lib.getUserSkeletonR_HandConf(track,user)<=0.5:
				follstage[user]="none" #invalid for the follow gesture
			if lib.getUserSkeletonL_HandY(track,user)-lib.getUserSkeletonTorsoY(track,user)<0 or lib.getUserSkeletonL_HandConf(track,user)<=0.5:
				follstage[user]="none"#invalid for the follow gesture
			if lib.getUserSkeletonR_HandY(track,user)-lib.getUserSkeletonTorsoY(track,user)<0 or lib.getUserSkeletonR_HandConf(track,user)<=0.5:
				follstage[user]="none"#invalid for the follow gesture

			if stopfollstage[user]=="none":#nothing has happened yet, check if the arm is in a position of interest
				if abs(lib.getUserSkeletonL_HandZ(track,user)-lib.getUserSkeletonR_HandZ(track,user))<100:
					if abs(lib.getUserSkeletonL_HandZ(track,user)-lib.getUserSkeletonL_ShZ(track,user))<150:
						stopfollstage[user] = "close"
			if stopfollstage[user]=="close":#we hit one point of interest, move to the next if the arm has met the new POI
				if abs(lib.getUserSkeletonL_HandZ(track,user)-lib.getUserSkeletonR_HandZ(track,user))<100:
					if abs(lib.getUserSkeletonL_HandZ(track,user)-lib.getUserSkeletonL_ShZ(track,user))>300:
						stopfollstage[user]="none"
						lock.acquire()
						userOfInt = lib.getUserID(track,user)
						stopfollow = True
						pickupfollow = False
						sys.stderr.write("got stop follow from user "+str(user)+"\n")
						lock.release()
			if abs(lib.getUserSkeletonL_HandZ(track,user)-lib.getUserSkeletonR_HandZ(track,user))>100 or lib.getUserSkeletonR_HandConf(track,user)<=0.5:
				stopfollstage[user]="none"#invalid for the stop follow gesture
			if lib.getUserSkeletonL_HandY(track,user)-lib.getUserSkeletonTorsoY(track,user)<0 or lib.getUserSkeletonL_HandConf(track,user)<=0.5:
				stopfollstage[user]="none"#invalid for the stop follow gesture
			if lib.getUserSkeletonR_HandY(track,user)-lib.getUserSkeletonTorsoY(track,user)<0 or lib.getUserSkeletonR_HandConf(track,user)<=0.5:
				stopfollstage[user]="none"#invalid for the stop follow gesture
					
			if quitstage[user]=="none":#nothing has happened yet, check if the arm is in a position of interest
				if lib.getUserSkeletonR_HandX(track,user)-lib.getUserSkeletonNeckX(track,user)<-50:
					quitstage[user]="scut"
			if quitstage[user]=="scut":#we hit one point of interest, move to the next if the arm has met the new POI
				if lib.getUserSkeletonR_HandX(track,user)-lib.getUserSkeletonNeckX(track,user)>50:
					if lib.getUserID(track,user) in curSkeletonPersonIDs and curSkeletonPersonIDs[lib.getUserID(track,user)]>=0:
						quitstage[user]="none"
						lock.acquire()
						quits = True
						if lib.getUserID(track, user) in curSkeletonPersonIDs:
							gestGivenPID = curSkeletonPersonIDs[lib.getUserID(track, user)]
						else:
							gestGivenPID = -1
						sys.stderr.write("goodbye "+str(user)+"\n")
						lock.release()
			if lib.getUserSkeletonR_HandY(track,user)-lib.getUserSkeletonNeckY(track,user)<0 or lib.getUserSkeletonR_HandConf(track,user)<=0.5:
				quitstage[user]="none"#invalid for the quit gesture
			if lib.getUserSkeletonR_HandY(track,user)-lib.getUserSkeletonHeadY(track,user)>0 or lib.getUserSkeletonR_HandConf(track,user)<=0.5:
				quitstage[user]="none"#invalid for the quit gesture

def remapPeople():
	for key in curSkeletonPersonIDs:
		if curSkeletonPersonIDs[key] in personMappings:
			curSkeletonPersonIDs[key]=personMappings[curSkeletonPersonIDs[key]]


				
# TODO Allow identification to be done using body proportion and color information
# when confidence is high that the user is the correct person, send identifier.
#LMC should be modified to look through current users and delete false recognitions when new recognitions are received 
def facialActions():
	global curSkeletonPersonIDs
	global oldSkeletonPersonIDs
	global personIDAttempts
	global followloss
	global userOfInt
	global pickupfollow
	global follow
	global lastrec
	while True:
		e.wait() #pauses thread if main thread flag is cleared
		lock.acquire()
		lib.takeSnapShot(track)
		lib.detectPeople(track)
		lock.release()
		
		tempSkelIDs = []
		
		lock.acquire()
		for user in range(0, lib.getUsersCount(track)):
			if lib.getUserPersonID(track, user) >= 0:# and not lastrec==lib.getUserPersonID(track, user): 
				curSkeletonPersonIDs[lib.getUserID(track, user)] = lib.getUserPersonID(track, user) #for each user, match skeletonID to personID
				lastrec = lib.getUserPersonID(track, user)
			if not lib.getUserID(track, user) in personIDAttempts.keys():
				personIDAttempts[lib.getUserID(track, user)] = 0
			tempSkelIDs.append(lib.getUserID(track, user))
			
		for key in curSkeletonPersonIDs: #for every skeletonID that has been created
			if not key in tempSkelIDs: #check if it is still on screen
				curSkeletonPersonIDs[key] = -5 #skeleton is no longer on screen
		checkHeight()
		checkShirts()
		remapPeople()
		deleteKeys = [] #holds keys to be deleted
		#check for any changes in the personIDs that correspond to the skeletonIDs
		for key in curSkeletonPersonIDs.keys():
			if key in oldSkeletonPersonIDs.keys(): #check skeletonIDs that were previously on screen
				if (not (curSkeletonPersonIDs[key] == oldSkeletonPersonIDs[key])) and (personIDAttempts[key] < MAX_GUESSES): #if the personID changed for a given skeletonID
					if curSkeletonPersonIDs[key] >= 0 and oldSkeletonPersonIDs[key] < 0:
						#person is now recognized
						p.write("face recognized " + str(key) + " " + str(curSkeletonPersonIDs[key]) + " " + str(time.time()) + "\n")
						personIDAttempts[key] = MAX_GUESSES + 1
						if curSkeletonPersonIDs[key] == followloss and pickupfollow:
							userOfInt = key #follow last user followed
							follow = True
							sys.stderr.write("got follow from userID "+str(userOfInt)+"\n")
						sys.stderr.write("recognized skeleton: " + str(key) + " as person: " + str(curSkeletonPersonIDs[key]) + "\n")
					elif curSkeletonPersonIDs[key] < 0 and oldSkeletonPersonIDs[key] >= 0:
						#recognized person has left the frame
						p.write("face lost " + str(key) + " " + str(oldSkeletonPersonIDs[key]) + " " + str(time.time()) + "\n")
						sys.stderr.write("person: " + str(oldSkeletonPersonIDs[key]) + " has left vision as skeleton: " + str(key) + "\n")
						deleteKeys.append(key)
					elif curSkeletonPersonIDs[key] < 0 and oldSkeletonPersonIDs[key] < 0: #for different negative numbers showing up (any negative number is a failure to recognize
						sys.stderr.write("failed guess for " + str(key) + "\n")
						personIDAttempts[key] = personIDAttempts[key] + 1
					else:
						curSkeletonPersonIDs[key] = oldSkeletonPersonIDs[key] #keep first identification
						sys.stderr.write("both greater, but different\n")
				elif personIDAttempts[key] < MAX_GUESSES:
					sys.stderr.write("failed same guess " + str(key) + "\n")
					personIDAttempts[key] = personIDAttempts[key] + 1 #attempt failed to identify user
				elif personIDAttempts[key] == MAX_GUESSES:
					#person was failed to be recognized
					p.write("face unrecognized " + str(time.time()) + "\n")
					sys.stderr.write(" user is unrecognizable\n")
					personIDAttempts[key] = personIDAttempts[key] + 1
				elif personIDAttempts[key] > MAX_GUESSES:
					if curSkeletonPersonIDs[key] == -5:
						deleteKeys.append(key) #skeleton has used max guesses and then left the screen
						if oldSkeletonPersonIDs[key] >= 0: #recognized person left
							p.write("face lost " + str(key) + " " + str(oldSkeletonPersonIDs[key]) + " " + str(time.time()) + "\n")
							sys.stderr.write("person: " + str(oldSkeletonPersonIDs[key]) + " has left vision as skeleton: " + str(key) + "\n")
					curSkeletonPersonIDs[key] = oldSkeletonPersonIDs[key]
				else:
					sys.stderr.write("equal and not other three\n")
			else:
				personIDAttempts[key] = personIDAttempts[key] + 1
				if curSkeletonPersonIDs[key] >= 0:
					#if face is recognized in one try (user comes on and is immediately recognized
					p.write("face recognized " + str(key) + " " + str(curSkeletonPersonIDs[key]) + " " + str(time.time()) + "\n")
					personIDAttempts[key] = MAX_GUESSES + 1
					sys.stderr.write("recognized skeleton: " + str(key) + " as person: " + str(curSkeletonPersonIDs[key]) + "\n")
					if curSkeletonPersonIDs[key] == followloss and pickupfollow:
						userOfInt = key #follow last user followed
						follow = True
						sys.stderr.write("got follow from userID "+str(userOfInt)+"\n")

				else:
					sys.stderr.write("first guess fail " + str(key) + "\n")
		for key in deleteKeys:
			sys.stderr.write("deleted skeleton " + str(key) + " as person " + str(oldSkeletonPersonIDs[key])+ "\n")
			del curSkeletonPersonIDs[key] #removes from dictionary any skeletons that have left the field of vision
			del personIDAttempts[key] #removes skeleton that has been lost so that the skeletonID can be reused
		oldSkeletonPersonIDs = dict(curSkeletonPersonIDs)
		
		lock.release()
	   
		time.sleep(.3)
				
def checkHeight():
	global curSkeletonPersonIDs
	global oldSkeletonPersonIDs	
	global aspects
	global skasps
		
			   
			
	#keys are skeleton id's (not indexies)
	for key in curSkeletonPersonIDs.keys():
		if curSkeletonPersonIDs[key]>=0:
			found = False
			i = 0
			for aspect in aspects:
				if aspect[0] == curSkeletonPersonIDs[key]:
					found = True
					break
				i=i+1
			if found==False:
				aspects.append([curSkeletonPersonIDs[key],-1,-1,-1])
			found = False
			user = 0
			for j in range(0,lib.getUsersCount(track)):
				if lib.getUserID(track, j) == key:
					user = j
					found = True
					break
			if found==False:
				sys.stderr.write("failed to find")
				continue #the skeleton of this person isn't present
			if lib.getUserSkeletonHeadConf(track,user)>0.5 and lib.getUserSkeletonR_HipConf(track,user)>0.5:# and lib.getUserSkeletonR_ElbowConf(track,user)>0.5 and lib.getUserSkeletonL_ElbowConf(track,user)>0.5:
				#TODO check distance and average it
				if aspects[i][1] < 0:
					aspects[i][1] = (np.sqrt((lib.getUserSkeletonHeadX(track,user)-lib.getUserSkeletonR_HipX(track,user))**2 + (lib.getUserSkeletonHeadY(track,user)-lib.getUserSkeletonR_HipY(track,user))**2 + (lib.getUserSkeletonHeadZ(track,user)-lib.getUserSkeletonR_HipZ(track,user))**2) + np.sqrt((lib.getUserSkeletonHeadX(track,user)-lib.getUserSkeletonL_HipX(track,user))**2 + (lib.getUserSkeletonHeadY(track,user)-lib.getUserSkeletonL_HipY(track,user))**2 + (lib.getUserSkeletonHeadZ(track,user)-lib.getUserSkeletonL_HipZ(track,user))**2))/2 #avg dist from hip to head
				else:
					aspects[i][1] = (aspects[i][1]+(np.sqrt((lib.getUserSkeletonHeadX(track,user)-lib.getUserSkeletonR_HipX(track,user))**2 + (lib.getUserSkeletonHeadY(track,user)-lib.getUserSkeletonR_HipY(track,user))**2 + (lib.getUserSkeletonHeadZ(track,user)-lib.getUserSkeletonR_HipZ(track,user))**2) + np.sqrt((lib.getUserSkeletonHeadX(track,user)-lib.getUserSkeletonL_HipX(track,user))**2 + (lib.getUserSkeletonHeadY(track,user)-lib.getUserSkeletonL_HipY(track,user))**2 + (lib.getUserSkeletonHeadZ(track,user)-lib.getUserSkeletonL_HipZ(track,user))**2))/2)/2 #avg dist from hip to head
				if aspects[i][2] < 0: #sh dist
					aspects[i][2] = np.sqrt((lib.getUserSkeletonL_ShX(track,user)-lib.getUserSkeletonR_ShX(track,user))**2 + (lib.getUserSkeletonL_ShY(track,user)-lib.getUserSkeletonR_ShY(track,user))**2 + (lib.getUserSkeletonL_ShZ(track,user)-lib.getUserSkeletonR_ShZ(track,user))**2)
				else:
					aspects[i][2] = (aspects[i][2]+np.sqrt((lib.getUserSkeletonL_ShX(track,user)-lib.getUserSkeletonR_ShX(track,user))**2 + (lib.getUserSkeletonL_ShY(track,user)-lib.getUserSkeletonR_ShY(track,user))**2 + (lib.getUserSkeletonL_ShZ(track,user)-lib.getUserSkeletonR_ShZ(track,user))**2))/2
				if aspects[i][3] < 0: #sh dist
					aspects[i][3] = np.sqrt((lib.getUserSkeletonL_ShX(track,user)-lib.getUserSkeletonR_ShX(track,user))**2 + (lib.getUserSkeletonL_ShY(track,user)-lib.getUserSkeletonR_ShY(track,user))**2 + (lib.getUserSkeletonL_ShZ(track,user)-lib.getUserSkeletonR_ShZ(track,user))**2)
				else:
					aspects[i][3] = (aspects[i][3]+np.sqrt((lib.getUserSkeletonL_ShX(track,user)-lib.getUserSkeletonR_ShX(track,user))**2 + (lib.getUserSkeletonL_ShY(track,user)-lib.getUserSkeletonR_ShY(track,user))**2 + (lib.getUserSkeletonL_ShZ(track,user)-lib.getUserSkeletonR_ShZ(track,user))**2))/2

def checkShirts():
	global shirts
	TH = 40
	for index in range(0,lib.getUsersCount(track)):
		if lib.getShirt(track,index)==0:
			sizeY = abs(lib.getShirtSizeY(track))
			sizeX = abs(lib.getShirtSizeX(track))
			ftch.setImageSize(sizeX, sizeY)
			flag = 0
			if sizeX/(1.0*sizeY)<0.25:
				flag = 1
			for x in range(0,sizeX):
				for y in range(0,sizeY):
					color = lib.getColor(track,x,y)
					if color == -1:
						flag = 1
					ftch.setVal(x,y,color)#load in pixel values (FCTH)
			if flag == 1: #bad data
				sys.stderr.write("skipping\n")
				continue
			if ftch.calc()==-1:#run calculation
				sys.stderr.write("skipping calc\n")
				continue
			result = range(0,192)
			sum = 0
			for i in range(0,192):
				result[i] = ftch.result(i)#retrieve result values
				sum=sum+result[i]
			#sys.stderr.write(str(sum)+"\n")
			match = -1 #last location of match found to the personID in shirts
			diff = np.zeros(len(shirts))
			for i in range(0,len(shirts)):
				#sys.stderr.write("\n"+str(shirts[i][0])+"\n\n")
				if lib.getUserID(track,index) in curSkeletonPersonIDs and curSkeletonPersonIDs[lib.getUserID(track,index)] == shirts[i][0]:#already have shirt data
					diff[i] = 0
					for j in range(0,192):
						diff[i] = diff[i] + (shirts[i][1][j] - result[j])**2 #square difference
					#sys.stderr.write(str(diff[i])+"\n")
					if diff[i]>TH:
						if match>=0:
							shirts[match][1] = shirts[i][1]
							shirts[i][1] = result #clearly this shirt value should be updated (the user has a new shirt)
							match=i
							sys.stderr.write("replaced shirt\n")
							break
					else: 
						for j in range(0,192):#merge old results with new ones
							shirts[i][1][j] = result[j]#(shirts[i][1][j] + result[j])/2
						match=i
						sys.stderr.write("updated shirt\n")
						break
					
					match=i
			if lib.getUserID(track,index) in curSkeletonPersonIDs and curSkeletonPersonIDs[lib.getUserID(track,index)]>=0:
				if match<0:
					#add 2 entries to shirts
					shirts.append([curSkeletonPersonIDs[lib.getUserID(track,index)],result])
					shirts.append([curSkeletonPersonIDs[lib.getUserID(track,index)],result])
					#sys.stderr.write("recorded shirts\n")
					#sys.stderr.write(str(len(shirts))+"\n")
			else:
				for i in range(0,len(shirts)):
					if diff[i]<=TH:#compare to recorded
						heightTemp  =(np.sqrt((lib.getUserSkeletonHeadX(track,index)-lib.getUserSkeletonR_HipX(track,index))**2 + (lib.getUserSkeletonHeadY(track,index)-lib.getUserSkeletonR_HipY(track,index))**2 + (lib.getUserSkeletonHeadZ(track,index)-lib.getUserSkeletonR_HipZ(track,index))**2) + np.sqrt((lib.getUserSkeletonHeadX(track,index)-lib.getUserSkeletonL_HipX(track,index))**2 + (lib.getUserSkeletonHeadY(track,index)-lib.getUserSkeletonL_HipY(track,index))**2 + (lib.getUserSkeletonHeadZ(track,index)-lib.getUserSkeletonL_HipZ(track,index))**2))/2
						found = False
						for j in range(0,len(aspects)):
							if shirts[i][0] == aspects[j][0]:
								user = j
								found = True
								break
						if found:
							if heightTemp<aspects[user][1]*1.02 and heightTemp>aspects[user][1]*0.98:
								curSkeletonPersonIDs[lib.getUserID(track,index)] = shirts[i][0]
								sys.stderr.write("recognized shirt\n")
								break#successful recognition
				
		
		
		
		
		#store and compare
								
def handleLine():
	global userOfInt
	global follow
	global stopfollow
	global pickupfollow
	if p.line == "follow\n": #follow command comes from master control because the follow speech command was given
		if lib.getUsersCount(track)>0:
			lock.acquire()
			userOfInt = lib.getUserID(track,0) #default to following user 0 regardless of recognition or number of users
			follow = True
			sys.stderr.write("got follow from userID "+str(userOfInt)+"\n")
			lock.release()
		else:
			sys.stderr.write("no users\n")
	elif p.line == "follow stop\n": #follow stop command from master control because the stop command was given by speech
		stopfollow = True
		pickupfollow = False
		follow = False
		sys.stderr.write("got stop follow\n")
	elif p.line == "sleep\n":
		e.clear()  #pauses the other threads until ready for them to start again
	elif p.line == "wake\n":
		e.set()	#allows other threads to continue
	else:
		sys.stderr.write("handle line " + p.line)

thread.start_new_thread(detect_motion,()) #gesture recognition
thread.start_new_thread(facialActions, ()) #face recognition

sys.stderr.write("starting KM process\n")

p = process(True,"KM")
p.setOnReadLine(handleLine)
InitSync()
e.set()

while True:
	p.tryReadLine()
	lock.acquire()
	if stopfollow:
		p.write("follow stop "+str(time.time()) + "\n") #received command to stop following
		follow = False
		stopfollow = False
	if quits:
		p.write("quit " + str(gestGivenPID) + " " + str(time.time()) + "\n") #if person is unknown, master control/speaking program will handle
		gestGivenPID = -1 #reset it to an unknown person
		exit()
	if follow:
		#sys.stderr.write(str(track) + " " + str(userOfInt) + "\n")
		pickupfollow=True
		user = -1
		index = 0
		while index<lib.getUsersCount(track): #find index of userOfInt which is a UserID. (user is an index)
			#sys.stderr.write("in while loop\n")
			if lib.getUserID(track,index)==userOfInt:
				user = index
			index = index + 1
		if user>=0: #we found the user
			if lib.isUserTracked(track, user):
				#sys.stderr.write("is following\n")
				if userOfInt in curSkeletonPersonIDs.keys() and curSkeletonPersonIDs[userOfInt] >= 0: #user is recognized and skeletonID should be sent
					followloss = curSkeletonPersonIDs[userOfInt]
					if lib.getUserSkeletonTorsoZ(track,user)/1000 == 0 and lib.getUserSkeletonTorsoX(track,user)/1000==0:
						curSkeletonPersonIDs[userOfInt]=-1
						stopfollow = True
					else:
						p.write("follow "+str(lib.getUserSkeletonTorsoZ(track,user)/1000)+" "+str(lib.getUserSkeletonTorsoX(track,user)/1000)+ " " + str(userOfInt) + " " + str(time.time()) + "\n")
				else: #user is unrecognized, send anyways in case follow was started by voice command and let the master control handle. should not send skeletonID.
					p.write("follow "+str(lib.getUserSkeletonTorsoZ(track,user)/1000)+" "+str(lib.getUserSkeletonTorsoX(track,user)/1000)+ " " + str(time.time()) + "\n")
			else:#they aren't tracked
				stopfollow = True
				
		else:#they're not here
			stopfollow = True
			
	if rightWave:
		rightWave=False
		p.write("rightWave " + str(gestGivenPID) + " " + str(time.time()) + "\n") #if person is unknown, master control/speaking program will handle
		gestGivenPID = -1 #reset it to an unknown person
	if leftWave:
		leftWave=False
		p.write("leftWave " + str(gestGivenPID) + " " + str(time.time()) + "\n") #if person is unknown, master control/speaking program will handle
		gestGivenPID = -1 #reset it to an unknown person
	lock.release()
	
	Sync()
