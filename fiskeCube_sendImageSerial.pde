import processing.serial.*;

Serial port;

int framesHeight;
int framesWidth;
int frameNum = 0;

int portRead;
int numImages = 4; //// THIS VALUE SHOULD COME FROM THE NUMBER OF BMPs IN A SPECIFIED DIRECTORY

PImage frames;
PImage cme;
PImage aurora;

PImage[] images;
int currentImage = 0;


void setup() {
  images = new PImage[numImages]; //// LOAD ALL THE IMAGES INTO AN ARRAY OF IMAGES
  images[0] = loadImage("fiskeCube_SOLAR_MAG_FLIP.bmp");
  images[1] = loadImage("fiskeCube_CME.bmp");
  images[2] = loadImage("fiskeCube_EARTH_MAG_CLOSE.bmp");
  images[3] = loadImage("fiskeCube_AURORA.bmp");


	port = new Serial(this, Serial.list()[0], 2000000); //// OPEN SERIAL PORT
  //// Serial.list[0] IS THE USB PORT CONNECTED
  //// 2000000 IS THE BAUDRATE --- EXCESSIVE I KNOW, BUT I WAS JUST TRYING CRAZY-HIGH BAUDRATES --- FYI, THE BAUDRATE IS NOT THE SPEED ISSUE.

}


void draw() {
	surface.setTitle(str(frameRate));
  sendFrame(frameNum, images[currentImage]);
  frameNum++;

  if (frameNum == framesHeight){ //// RESET FRAME COUNTER TO 0
    frameNum = 0;
    currentImage++;
    if (currentImage == numImages){
       currentImage = 0;
    }
  }
}



void sendFrame(int thisFrame, PImage frames){
  framesHeight = frames.height; ///// EACH IMAGE HAS A DIFFERENT HEIGHT ////
  framesWidth = frames.width;   ///// ALL IMAGES HAVE THE SAME WIDTH, SO THIS IS REDUNDENT BUT IT MIGHT BE HANDY IN THE FUTURE ////
  int ledCount = 0;
	int stripNum = 0;
  int r;
  int g;
  int b;
	for (int x = 0; x < framesWidth; x++){ //// READ EVERY ENTRY IN FRAMES[]

				color c = frames.get(x, thisFrame);
        //// THE ABOVE READS THE COLOR VALUE AT THE CURRENT PIXEL
        //// x == WIDTH == LED
        //// thisFrame == HEIGHT == FRAME NUMBER



				r = (c>>16)&255; 	////// BITSHIFT TO GET EACH VALUE
				g = (c>>8)&255;
				b = c&255;

				if(r == 0 && g == 0 && b == 0){
					//// SKIP PIXELS THAT ARE OFF ////
				}

				else{
					port.write('s'); /// SEND START COMMAND
					port.write(r); 	/// SEND COLOR INDIVIDUALLY
					port.write(g);
					port.write(b);
					port.write(stripNum); // SEND STRIP NUMBER 0 --> 15
					port.write(ledCount); // SEND LED NUMBER  0 --> 255
				}
    ledCount++;
    if (ledCount == 256){
      ledCount = 0;
      stripNum++;
    }
		}
		port.write('f'); /// SHOW FRAMES
		port.write('c'); /// CLEAR FRAMES
		// port.stop();
		// delay(100);

}
