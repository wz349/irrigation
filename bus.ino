#include "Seeed_BME280.h"
#include <Wire.h>

BME280 bme280;


// You have to change the ADDRESS for each ARDUINO
  #define ADDRESS 7
byte sbufferA [1];
byte sbufferD [1];
  int more = false;
  int last = true;
  int i = 0;
  int buffer = 0;
  int role = 0;
  unsigned long timeout = 5;
long prt = 32766;
long bridge = 600;
int readCMD = 0;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(2, OUTPUT);
  delay(10);
  digitalWrite(2, LOW);


  while(!bme280.init());
  
  }

void loop() {
  if(role == 0) {
    readCMD = listen();
    while(readCMD == 0) readCMD = listen();
    blink(1);
    role = 1;
  }
  else {
    digitalWrite(2, HIGH);
    delay(100);   //DONT TOUCH THIS
    sendAddress(4);
    if(readCMD ==3) {
      //sendData(prt);
      //prt += 1;
      sendData(bme280.getTemperature());
    } else{
      sendData(bme280.getHumidity());
      //sendData(bridge);
      //bridge += 1;
    }
    role = 0;
    delay(1000);
  }
  
  //delay(2000);
}


// send address (0-127)
void sendAddress(int a) {
   Serial.print(char(a | 0x80));
}

// send data (0-32767)
void sendData(long d) {
  int first = 0;
  long current = 0;
  long rest = 0;
  if(d > 0x3F) {                            // if data is greater than 6 bits and need extended mode
      rest = d;
      first = 1;
      while(rest != 0) {
        current = rest & 0x3F;              // gets rid of everthing but last 6 bits
        rest = rest >> 6;
        if(first || (rest == 0)) {
          current = current | 0x40;         // places 1 in 7th bit to indicate start or end of "extended" transmission
          first = !first;
        }
        Serial.print(char(current));
      }
    }
    else Serial.print(char(d));
}


int listen() {
  unsigned long start = 0;
  unsigned long now = 0;
  digitalWrite(2, LOW);
  while(1) {
  while(Serial.available()){
       Serial.readBytes(sbufferA,1);
        int address = sbufferA[0];
        if( address >> 7 ) {                      //If byte is an address byte (MSB == 1)
          address = address & 0x7F;               //Get rid of last bit to compare with ADDRESS
          if(address == ADDRESS)  {               //If transmission was meant for this Arduino
            start = millis();
            while(1) {                            //Keep reading until another address comes
              now = millis();
              if(now - start > timeout*1000) return 0;
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
                  if(data == 2) return 2;
                  if(data == 3) return 3;
                   //blink(data);
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
