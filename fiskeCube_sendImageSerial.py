import serial
import cv2
import struct
import datetime
import sys, os

dataDirName = os.path.dirname(__file__) + '/data/'

#####INITIALIZATION


## LOAD ALL THE IMAGES INTO AN ARRAY OF IMAGES
imageList = []
for filename in sorted(os.listdir(dataDirName)):
	if filename.endswith(".bmp"):
		imageList.append(cv2.imread(dataDirName + filename))
	else:
		continue


ser = serial.Serial('/dev/ttyACM0') ## CHANGE TO WHATEVER PORT IS BEING USED
ser.baudrate = 2000000

s = str.encode('s') ### START READ VAR
f = str.encode('f') ### SHOW LEDS VAR
c = str.encode('c') ### CLEAR LEDS VAR

#####Functions
def sendFrame(thisFrame, currentImage):
	framesWidth = currentImage.shape[1]
	ledCount = 0
	stripNum = 0
	sendPacket = struct.pack('>B', 0)
	# print('Frame started at ', datetime.datetime.now())
	# print('framesWidth: ', framesWidth)
	for y in range(0,framesWidth): ### FOR EACH PIXEL IN CURRENT FRAME
		## OPENCV USES BGR FORMAT FOR COLORS
		b = currentImage[thisFrame, y, 0]
		g = currentImage[thisFrame, y, 1]
		r = currentImage[thisFrame, y, 2]

		if(r==0 and g==0 and b==0):
			pass
		else:
			r = struct.pack('>B', r)
			g = struct.pack('>B', g)
			b = struct.pack('>B', b)
			sN = struct.pack('>B', stripNum)
			lC = struct.pack('>B', ledCount)

			sendPacket += s + r + g + b + sN + lC

		ledCount = ledCount + 1
		if(ledCount == 256):
			ledCount = 0
			stripNum = stripNum + 1

	ser.write(sendPacket) 	#### SEND ONE ENTIRE FRAME OF BYTES
	ser.write(f) 		  	#### SHOW LEDS
	ser.write(c)		  	#### CLEAR LEDS


def runCube():
	for i in range(0, len(imageList)):				### IMAGE NUMBER < imageList LENGTH
		# print('Viz number', i , 'started at', datetime.datetime.now())
		sys.stdout.write('\rViz number ' + str(i) + ' started at ' + str(datetime.datetime.now()))

		for j in range(0, (imageList[i].shape[0])):	### FRAME NUMBER < imageList[i] HEIGHT
			sendFrame(j, imageList[i])


#### LOOP ####
while True:
	try:
		runCube()

	except ValueError as e:
		print('Tell my debugger: ', e)
