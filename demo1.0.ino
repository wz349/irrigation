#include <SPI.h>
#include <math.h>
const int chipSelectPin = 3; //now used for pdown
const int dataReadyPin = 6;
const int ampLvlPin = 4;
const int chanSelPin = 2;
const int rsEnablePin = 9;
long byte1;
long byte2;
byte byte3;
long value;
// These specific option are tested to give the 23 bit (one bit missing) of the adc reading
#define speedMaximum 14000000
#define dataOrder MSBFIRST
#define dataMode SPI_MODE2


SPISettings mySettting(speedMaximum, dataOrder, dataMode);



#define ADDRESS 3
byte sbufferA [1];
byte sbufferD [1];
  int more = false;
  int last = true;
  int i = 0;
  int buffer = 0;
  int role = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(rsEnablePin, OUTPUT);
  delay(10);
  digitalWrite(rsEnablePin, LOW);

    pinMode(chipSelectPin,OUTPUT);
  pinMode(dataReadyPin,INPUT);
  pinMode(ampLvlPin,OUTPUT);
  pinMode(chanSelPin,OUTPUT);
    digitalWrite(chipSelectPin,LOW);
  digitalWrite(ampLvlPin,LOW);   //default amplification level = 1
  digitalWrite(chanSelPin,HIGH); //default channel = ain3&4 (for test)

  
  SPI.begin();


  }

void loop() {
  // put your main code here, to run repeatedly:
  if(role == 0) {
    listen();
    blink(1);
    role = 1;
  }
  else {
    
    digitalWrite(rsEnablePin, HIGH);
    int x = (int)( getAdcReading(0) >> 8);
    sendAddress(4);
    sendData(x);
    //sendData(400);
    //sendData(32767);
    delay(2000);
  }
  
  //delay(2000);
}


// send address (0-127)
void sendAddress(int a) {
   Serial.print(char(a | 0x80));
}

// send data (0-32767)
void sendData(int d) {
  int first = 0;
  int current = 0;
  int rest = 0;
  if(d > 0x3F) {                            // if data is greater than 6 bits and need extended mode
      rest = d;
      first = 1;
      while(rest != 0) {
        current = rest & 0x3F;              // gets rid of everthing but last 6 bits
        rest = rest >> 6;
        if(first || (rest == 0)) {
          current = current | 0x40;         // places 1 in 6th bit to indicate start or end of "extended" transmission
          first = !first;
        }
        Serial.print(char(current));
      }
    }
    else Serial.print(char(d));
}


int listen() {
  digitalWrite(rsEnablePin, LOW);
  while(1) {
  while(Serial.available()){
       Serial.readBytes(sbufferA,1);
        int address = sbufferA[0];
        if( address >> 7 ) {                      //If byte is an address byte (MSB == 1)
          address = address & 0x7F;               //Get rid of last bit to compare with ADDRESS
          if(address == ADDRESS)  {               //If transmission was meant for this Arduino
            while(1) {                            //Keep reading until another address comes
              if(Serial.available()) {
                Serial.readBytes(sbufferD,1);
                int data = sbufferD[0];
                if(data >> 7) {              //If next byte is another address, break
                  break;
                }
                // if tranmission is start or end of extended mode
                if(data >> 6){
                  // get rid of 6th bit (extended bit)
                  data = data & 0x3F;
                  // if this is the start of extended mode
                  if(more == false){
                    buffer = data;
                    //print "* ", bin(buffer);
                    last = more;
                    more = true;
                  // else this is the end of extended mode
                  }else{
                    i = i+1;
                    buffer = (data << (6*i)) | buffer;
                    //print "! ", bin(buffer);
                    data = buffer;
                    last = more;
                    more = false;
                  }
                // else this is either a normal transmission or in the middle of extended mode
                }else{
                  last = more;
                }
                // if transmission is done, whether normal or extended mode
                if (more == false){
                  if(data == 2) return 0;
                   blink(data);
                  buffer = 0;
                  more = false;
                  last = false;
                  i=0;
                // else if this is the middle of extended mode
                } else if((more == true) and (last == true)){
                  i= i+1;
                  buffer = (data << (6*i)) | buffer;
                }
              }
            }
          }
        }
  }
  
  }
    
}



void blink(int t){
  if (t>4) t =1;
  while(t>0) {
    digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
    delay(500);                       // wait for a second
    digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
    delay(500);                       // wait for a second
    t--;
  }
}


long getAdcReading(int channel) {

  long value = 0 ;
  SPI.beginTransaction(mySettting);
  //digitalWrite(chipSelectPin,LOW);

  // a little delay for ad7191 to be ready (from datasheet)
  __asm__("nop\n\t");
  __asm__("nop\n\t");
  __asm__("nop\n\t");
  __asm__("nop\n\t");
  while(digitalRead(dataReadyPin)==HIGH){}
  delayMicroseconds(10);
  while(digitalRead(dataReadyPin)==HIGH){}
   
  byte1 = SPI.transfer16(0);
  byte2 = SPI.transfer(0);

  //digitalWrite(chipSelectPin,HIGH);
  SPI.endTransaction();

  
  value = byte1*256+byte2;  
  return value;
  
}
