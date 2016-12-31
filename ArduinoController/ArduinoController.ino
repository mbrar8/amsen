#include "dht11.h"
#include <Wire.h>




/*************************
* Gas sensor globals, these are circular buffers to store instant values
* We report the average of these circular buffers on the serial port
*************************/
// Circular buffer for Sensors so that we can take a moving average
#define PIN_MQ2 A0
#define PIN_MQ4 A1

#define SV_SIZE 100
int svMQ4[SV_SIZE];
int svMQ2[SV_SIZE];
// index into the circular buffers
int index=0;

/*************************
* Humiture globals
*************************/
#define DHT11PIN 22
dht11 DHT11;

/*************************
* Compass globals
**************************/
// Compass I2C Address
int HMC6352Address = 0x42;
//calculated in setup()
int compassSlaveAddress;
String compassValue;


// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 115200 bits per second:
  Serial.begin(115200);
  
  // Compute the compass slave address
  // Shift the device's documented slave address (0x42) 1 bit right
  // This compensates for how the TWI library only wants the
  // 7 most significant bits (with the high bit padded with 0)
  compassSlaveAddress = HMC6352Address >> 1;
  Wire.begin();
}


int average(int array[SV_SIZE]) {
  long sum = 0;
  int x = 0;  
  for(x; x < SV_SIZE; x++) {
    sum = sum + array[x];
  }  
  int avg = sum/SV_SIZE;
  return avg;
}

void readHumiture() {
    // Humiture sensor is time sensitive and cannot be read too often and may give timeout error
    // just ignore the failed attempts as long as some attempts succeed. The humidity & temp this way is sampled
    // as fast the sensor suports
    int chk = DHT11.read(DHT11PIN);
    /* 
    switch (chk)
    {
      case DHTLIB_OK: 
  		Serial.println("OK"); 
  		break;
      case DHTLIB_ERROR_CHECKSUM: 
  		Serial.println("Checksum error"); 
  		break;
      case DHTLIB_ERROR_TIMEOUT: 
  		Serial.println("Time out error"); 
  		break;
      default: 
  		Serial.println("Unknown error"); 
  		break;
    }
    */
}

void readGasSensors() {
   // read the input on analog pin 0:
  svMQ4[index]  = analogRead(PIN_MQ4);
  svMQ2[index] = analogRead(PIN_MQ2);

  // Increment index and wrap around if its end of array
  index = index + 1;
  if (index >= SV_SIZE) {
    index = 0;
  } 
}

void readCompass() {
    Wire.beginTransmission(compassSlaveAddress);
    Wire.write("A");
    Wire.endTransmission();
    delay(10);
    
    
    Wire.requestFrom(compassSlaveAddress, 2);
    int i = 0;
    byte headingData[2];
    while(Wire.available() && i < 2)
    {
      headingData[i] = Wire.read();
      i++;
    }
    int headingValue = headingData[0]*256 + headingData[1];
    compassValue = "";
    compassValue += int(headingValue/10);
    compassValue += ".";
    compassValue += int (headingValue % 10);
}

/*********************************************
* Output sends all the data collected on the serial port
* using the following format
* <sensor_name>=<sensor_value>,<sensor_name>=<sensor_value>, ..... \n
* Example
* MQ4=10,MQ2=5,MQ3=54,HUM=35,TMP=32,CMP=120
**********************************************/
void output() {
    String output= "";
    output += "MQ4=";
    output += average(svMQ4);
    output += ",MQ2=";
    output += average(svMQ2);
    output += ",HUM=";
    output += DHT11.humidity;
    output += ",TMP=";
    output += DHT11.temperature;
    output += ",CMP=";
    output += compassValue;
    Serial.println(output);
}

// the loop routine runs over and over again forever:
void loop() {
  readGasSensors();
 
  // Every 1000th value we send the output on serial port
  if (index == 0) {
    // Read the sensors that take time to read
    readHumiture();
    readCompass();
    output();
  }
 
    
}