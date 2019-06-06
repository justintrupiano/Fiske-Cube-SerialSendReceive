import serial
# import serial.tools.list_ports
# import glob ## TODO This is for autodetecting serial ports, but i'll work on that later
# from PIL import Image
import cv2
import struct
import datetime
import sys, os

dirname = os.path.dirname(__file__)
# filename = os.path.join(dirname, './data/')
#####INITIALIZATION

imageList = []

## LOAD ALL THE IMAGES INTO AN ARRAY OF IMAGES
# imageList.append(Image.open("data/fiskeCube_SOLAR_MAG.bmp"))
# imageList.append(Image.open("data/fiskeCube_CME.bmp"))
# imageList.append(Image.open("data/fiskeCube_EARTH_MAG_CLOSE.bmp"))
# imageList.append(Image.open("data/fiskeCube_AURORA.bmp"))
imageList.append(cv2.imread(dirname + "data/fiskeCube_SOLAR_MAG.bmp"))
imageList.append(cv2.imread(dirname + "data/fiskeCube_CME.bmp"))
imageList.append(cv2.imread(dirname + "data/fiskeCube_EARTH_MAG_CLOSE.bmp"))
imageList.append(cv2.imread(dirname + "data/fiskeCube_AURORA.bmp"))

# ser = serial.Serial()
# ser.port = serial.tools.list_ports.comports()[0]
# ser.open()

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

	# print('Frame started at ', datetime.datetime.now())
	# print('framesWidth: ', framesWidth)
	for y in range(0,framesWidth): ### FOR EACH PIXEL IN CURRENT FRAME
		## OPENCV USES BGR FORMAT FOR COLORS
		b = currentImage[thisFrame, y, 0]
		g = currentImage[thisFrame, y, 1]
		r = currentImage[thisFrame, y, 2]

		if(r==0 & g==0 & b==0):
			pass
		else:
			r = struct.pack('>B', r)
			g = struct.pack('>B', g)
			b = struct.pack('>B', b)
			sN = struct.pack('>B', stripNum)
			lC = struct.pack('>B', ledCount)

			send = s + r + g + b + sN + lC
			ser.write(send)

		ledCount = ledCount + 1
		if(ledCount == 256):
			ledCount = 0
			stripNum = stripNum + 1

	# print('Frame completed at ', datetime.datetime.now())
	ser.write(f)
	ser.write(c)


def runCube():
	for i in range(0, len(imageList)):				### IMAGE NUMBER < imageList LENGTH
		# print('Viz number', i , 'started at', datetime.datetime.now())
		sys.stdout.write('\rViz number ' + str(i) + ' started at ' + str(datetime.datetime.now()))

		for j in range(0, (imageList[i].shape[0])):	### FRAME NUMBER < imageList[i] HEIGHT
			sendFrame(j, imageList[i])
			# print('i: ', i)
			# print('j: ', j)



#### LOOP ####
while True:
	try:
		runCube()

	except ValueError as e:
		print('Tell my debugger this context-relevant information: ', e)
