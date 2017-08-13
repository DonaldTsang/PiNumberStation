#!/usr/bin/python

import subprocess # for calling console
# import math
import time
import wave
import sys
# import random

#from encryption import encrypt, decrypt
#enable_encryption = False
#encKey = 0

# Turn on buzzer:
buzzer_number = 4

monolith_on = False

# Give the pifm extension executable rights.
subprocess.call(["sudo", "chmod", "+x", "pifm"])

# Message to synthesize and broadcast
message = "123456789 abcdefghijklmnopqrstuvwxyz"
# Would you like to repeat the message infinitely? 
repeat = True

loadFromFile = True
freq = "108.8" #default frequency, will change if run with arguments.

# Sounds for digits/numbers.
sounds = ["Zero", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Niner"]

# Sounds for alphanumeric. Use NATO Phonetic
upper = ["Alpha", "Bravo", "Charlie", "Delta", "Echo", "Foxtrot", "Georgie", "Hotel",
    "Item", "Johnny", "Kilo", "Lima", "Monkey", "Nanny", "Oscar", "Papa", "Quebec",
    "Robert", "Sugar", "Tango", "Uncle", "Victor", "Whisky", "X-ray", "Yankee", "Zeebra"]

lower = ["Abe", "Beer", "Cheeese", "Dog", "Edison", "Fred", "Golf", "How", "India",
    "Juliet", "King", "Love", "Mike", "November", "Orange", "Pipe", "Queen", "Romeo",
    "Sierra", "Tom", "Uniform", "Vinegar", "William", "Excellent", "Yoke", "Zoo"]

if (len(sys.argv) > 1):
	# if arguments present
	freq = sys.argv[1]
	print("Broadcast on " + str(freq))


def main():
	
	print("PiNumberStation started...")
	'''
	for x in range(0, len(message)):
		print(str(message[x]))
	'''

	import os.path
	if (os.path.isfile(sys.path[0] + "/vo/upper/Alpha.wav") == False):
		print("Synthesis Failure: NO ALPHANUMERIC SUPPORT")
		time.sleep(5)

	return
	
def constructWavFromFile( fileName):
	fMsg = open(sys.path[0] + "/" + fileName, 'r')
	strMessage = fMsg.read()
	constructWav( strMessage )
	
	return
	
def playMessage():
	
	print("Broadcast Begin..")

	subprocess.call(["sudo", sys.path[0] + "/pifm", sys.path[0] + "/message.wav", freq])
	
	return
	
def getVO( character ):
	if character.isdigit() == True: return "/number/" + sounds[int(character)] + ".wav" 
	if character.isupper() == True: return "/upper/" + upper[ord(character) - ord('A')] + ".wav"
	if character.islower() == True: return "/lower/" + lower[ord(character) - ord('a')] + ".wav"
		
	
def constructWav( strMessage ):
	
	print("Synthesizing Message..")
	
	infiles = []
	
	#if enable_encryption == True:
	#	strMessageOut = encrypt(strMessage, encKey)
	#else:
	#	strMessageOut = strMessage
	
	strMessageOut = strMessage
	
	'''
	import audiolab, scipy
	a, fs, enc = audiolab.wavread('file1.wav')
	b, fs, enc = audiolab.wavread('file2.wav')
	c = scipy.vstack((a,b))
	audiolab.wavwrite(c, 'file3.wav', fs, enc)
	'''
	
	# determine infiles for message.
	i=0
	if buzzer_number > 0:
		j=0
		while (j < buzzer_number):
			infiles.append(sys.path[0] +"/vo/misc/buzzer.wav")
			j=j+1

	infiles.append(sys.path[0] + "/vo/misc/on3.wav")

	if monolith_on == True:
		infiles.append(sys.path[0] + "/vo/misc/monolith.wav")

	for character in strMessageOut:
		infiles.append(sys.path[0] + "/vo/" + getVO(character))
		print(infiles[i+2])
		i = i + 1
		
	infiles.append(sys.path[0] + "/vo/misc/off3.wav")
	
	#infiles = ["sound_1.wav", "sound_2.wav"]
	
	outfile = sys.path[0] + "/message.wav"
	
	data= []
	for infile in infiles:
	    w = wave.open(infile, 'rb')
	    data.append( [w.getparams(), w.readframes(w.getnframes())] )
	    w.close()

	output = wave.open(outfile, 'wb')
	output.setparams(data[0][0])
	
	for x in range(0, len(infiles)):
		output.writeframes(data[x][1])
	
	#output.writeframes(data[0][1])
	#output.writeframes(data[1][1])
	#output.writeframes(data[2][1])
	output.close()
	
	print("Synthesis Complete..")
	
	return
	

# START:
main()

if (loadFromFile == False):
	constructWav(message)
else:
	constructWavFromFile("message.txt")
	
if repeat == False:
	playMessage()
else:
	while (1):
		if (loadFromFile == False):
			constructWav(message)
		else:
			constructWavFromFile("message.txt")
		print("Construction Complete..")
		playMessage()
		print("Playing..")

#kill pifm because it doesn't kill itself, for some stupid reason.
subprocess.call(["sudo", "killall", "pifm"])
print("Done")
