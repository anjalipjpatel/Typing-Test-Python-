# makes use of replit db feature - program built in replit

import random
import time
import os
#from replit import db
import getpass

# clear console output
def clear():
	os.system("clear")
	time.sleep(1)


# username and password function
def LoginSys():
	ls = 0
	while ls < 1 or ls > 3:
		try:
			print("WELCOME TO THE TYPING TEST GAME!")
			ls = int(input("Do you want to:\n[1] Sign Up\n[2] Login\n[3] Continue Without Login\n→ "))
		except ValueError:
			ls = 0
	if ls == 1:
		susername = input("Username: ")
		if susername in db.keys():
			print("username already in use")
			time.sleep(2)
			clear()
			return ""
		spassword = getpass.getpass("Password: ")
		db[susername] = [spassword,"0"]
		print("\u001b[32mSuccessfully Signed Up!\u001b[0m")
		return LS()
	elif ls == 2:
		username = input("Username: ")
		password = getpass.getpass("Password: ")
		allUsernames = db.keys()
		if username in allUsernames:
			actualpass = db[username][0]
			if password == actualpass:
				print("\u001b[32mLogin Successful!\u001b[0m")
				time.sleep(1)
				clear()
				return username
			else:
				print("\u001b[31mPassword is wrong!\u001b[0m")
				time.sleep(1)
				clear()
				return ""
		else:
			print("\u001b[31mUsername Not Found!\u001b[0m")
			time.sleep(1)
			clear()
			return ""
	elif ls == 3:
		global CurrentGuestUsed
		time.sleep(0.5)
		clear()
		i = random.randint(1,9999)
		while CurrentGuestUsed[i]:
			i = random.randint(0,9999)
		user = "guest" + str(i)
		CurrentGuestUsed[i] = True
		db[user] = ["","0"]
		return user

# display and choose options
def MainMenu():
	print("***********************")
	print("1: Typing Test with no recorded data")
	print("2: Typing Test with recorded data")
	print("3: Load Scores from File")
	# 4. user data such as avearge wpm, number of tests taken, top wpm [if no entries output that]
	print("4. Exit")
	print("***********************")
	optn = -1
	while optn < 1 or optn > 4:
		try:
			print("Enter the option which you would like to select: ")
			optn = int(input())
		except ValueError:
			optn = -1
	return optn

# user chooses the number of words they want to do the test using
def GetNumOfWords():
	numWords = -1
	while numWords < 5 or numWords > 100:
		try:
			numWords = int(input("Enter the number of words you would like to complete the test using! (MUST BE BETWEEN 5 and 100): "))
			print("")
		except ValueError:
			numWords = -1
	return numWords

# create string of text based on the number of words chosen - randomly generated
def GenerateText(numWords):
	global allWords
	global stringToType, allWords
	randNum = -1
	string = ""
	for i in range(numWords):
		randNum = random.randint(1,len(allWords))
		string += allWords[randNum]
		string += " "
	return string

# output start timer
def Countdown(numToCount):
	for i in range(numToCount):
		amber = [5,4]
		red = [3,2,1]
		if numToCount in amber:
			print("\u001b[33m",numToCount,"\u001b[0m")
		elif numToCount in red:
			print("\u001b[31m",numToCount,"\u001b[0m")
		else:
			print("\u001b[32m",numToCount,"\u001b[0m")
		numToCount -= 1
		time.sleep(1)
	print("\u001b[32mGO\u001b[0m")
	
# calculations to be made and output colour coded user input if correct or not
def Calculation(time):
	global stringToType,userReturn,currentUsername
	if abs(len(stringToType)-len(userReturn)) > 10:
		return False,-1,-1
	else:
		score = len(stringToType)
		i = 0
		colReturn = ""
		while i < len(stringToType) and i < len(userReturn):
			if userReturn[i] != stringToType[i]:
				colReturn = colReturn + "\u001b[31m" + userReturn[i] + "\u001b[0m"
				score -= 1
			else:
				colReturn = colReturn + "\u001b[32m" + userReturn[i] + "\u001b[0m"
			i += 1
		db[currentUsername][1] = str(int(db[currentUsername][1]) + score)
		print(db[currentUsername][1])
		print(colReturn)
		numWordsStandardisted = int(len(stringToType) / 5)
		timeinmins = timeTaken/60
		wordspm = round(((numWordsStandardisted/timeinmins)))
		
		return True,score,wordspm

# print the scores
def DisplayScore(val,t,s,w):
	if val:
		print("it took you ", t, " seconds")
		print("your score is: ", s)
		print("your wpm is: ", w)
	else:
		print("invalid attempt.")

# get and print the top 10 wpm from file
def OutputTopTen():
		
	allScores = []
	topScores = []
	for i in range(10):
		topScores.append(["",""])
	try:
		f = open("scores.txt","r")
		allScores = f.read().splitlines()
		f.close()
		# implement linear search to see if bigger and if is then insert - sorting alg.
		for i in range(1,len(allScores)):
			currentline = allScores[i].split("*")
			for j in range(len(topScores)):
				if currentline[1] > topScores[j][1]:
					temp = topScores[j]
					topScores[j] = currentline
					currentline = temp
	
		# output top scores to screen
		print("*** TOP 10 ***")
		print("pos", "	", "name", "	", "wpm")
		for i in range(len(topScores)):
			if topScores[i] != ["",""]:
				print(i+1, " : ", topScores[i][0], "	", topScores[i][1])
	except IOError:
		print("ERROR: please report to developer")

# write data to file
def WriteToFile(fName,text):
	try:
		f = open(fName,"a")
		f.write(text)
		f.close()
	except IOError:
		print("ERROR: report to developer")


#################################################################
##################### MAIN PROGRAM ##############################
#################################################################


# put all words into array
f = open("words.txt", "r")
allWords = f.read().splitlines()
f.close()


# variable declarations
cont = True
currentUsername = ""
CurrentGuestUsed = [False] * 10000


# allow user to login or continue as guest
while currentUsername == "":
	currentUsername = LoginSys()


while cont:
	# choose desired option from main menu
	select = MainMenu()
	
	if select == 1 or select == 2: # perform a test
		time.sleep(0.5)
		numberOfWords = GetNumOfWords()
		stringToType = ""
		stringToType = GenerateText(numberOfWords)

		# countdown and begin test
		clear()
		print("*****************")
		print("GET READY TO GO!")
		print("*****************")
		time.sleep(0.5)
		Countdown(5)
		
		# output string and take in user input of text
		print("")
		print(stringToType)
		print("")
		startT = time.time()
		userReturn = str(input("→ "))
		endT = time.time()	# when enter, timer stops
		timeTaken = round(endT - startT,2)
		score = -1 
		# calculate scores
		isValid,score,wpm = Calculation(timeTaken)
		# display score and wpm/cpm
		DisplayScore(isValid,timeTaken,score,wpm)
		
		if select == 2:
			# save data to text file too with username - [make sure no * symbols so file works]
			line = currentUsername + "*" + str(wpm) + "\n"
			WriteToFile("scores.txt",line)
		input("press enter to continue: ")

		time.sleep(5)
		
	elif select == 3: # print hte top 10
		time.sleep(1)
		OutputTopTen()
		time.sleep(1)
		
	else: # exit loop - do not want to continue
		cont = False

time.sleep(0.5)
print("THANK YOU FOR USING THIS TYPING TEST")
time.sleep(0.5)

# top wpm each username stored in datatbase,average wpm etc.

# output score

# add clear pages in to make code more clear

# improved error checking by checking each word instead of the entire string