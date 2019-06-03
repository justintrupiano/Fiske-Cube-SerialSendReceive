import serial
# import serial.tools.list_ports
# import glob ## TODO This is for autodetecting serial ports, but i'll work on that later
# from PIL import Image
import cv2
import struct
import datetime


#####INITIALIZATION

imageList = []

## LOAD ALL THE IMAGES INTO AN ARRAY OF IMAGES
# imageList.append(Image.open("data/fiskeCube_SOLAR_MAG.bmp"))
# imageList.append(Image.open("data/fiskeCube_CME.bmp"))
# imageList.append(Image.open("data/fiskeCube_EARTH_MAG_CLOSE.bmp"))
# imageList.append(Image.open("data/fiskeCube_AURORA.bmp"))
imageList.append(cv2.imread("data/fiskeCube_SOLAR_MAG.bmp"))
imageList.append(cv2.imread("data/fiskeCube_CME.bmp"))
imageList.append(cv2.imread("data/fiskeCube_EARTH_MAG_CLOSE.bmp"))
imageList.append(cv2.imread("data/fiskeCube_AURORA.bmp"))


# ser = serial.Serial()
# ser.port = serial.tools.list_ports.comports()[0]
# ser.open()

ser = serial.Serial('/dev/ttyACM0'); ## CHANGE TO WHATEVER PORT IS BEING USED
ser.baudrate = 2000000



#####Functions
def sendFrame(thisFrame, currentImage):
	# framesHeight = currentImage.height #NOT NEEDED --- EACH FRAME IS ONLY 1 PIXEL HIGH
	# framesWidth = currentImage.width
	framesWidth = currentImage.shape[1]
	ledCount = 0
	stripNum = 0

	print('Frame started at ', datetime.datetime.now())

	for y in range(0,framesWidth): ### FOR EACH PIXEL IN CURRENT FRAME
		## OPENCV USES BGR FORMAT FOR COLORS
		b = currentImage[thisFrame, y, 0]
		g = currentImage[thisFrame, y, 1]
		r = currentImage[thisFrame, y, 2]

		if(r==0 & g==0 & b==0):
			pass
		else:
			ser.write(str.encode('s'))
			ser.write(struct.pack('>B', r))
			ser.write(struct.pack('>B', g))
			ser.write(struct.pack('>B', b))
			ser.write(struct.pack('>B', stripNum))
			ser.write(struct.pack('>B', ledCount))

		ledCount = ledCount + 1
		if(ledCount == 256):
			ledCount = 0
			stripNum = stripNum + 1


	print('Frame completed at ', datetime.datetime.now())

	ser.write(str.encode('f'))
	ser.write(str.encode('c'))


def runCube():
	for i in range(0, len(imageList)):	### IMAGE NUMBER < imageList LENGTH
		for j in range(0, imageList[i].shape[1]):	### FRAME NUMBER < imageList[i] HEIGHT
			sendFrame(j, imageList[i])




#### LOOP ####
while True:
	try:
		runCube()

	except ValueError as e:
		print('Tell my debugger this context-relevant information: ', e)
