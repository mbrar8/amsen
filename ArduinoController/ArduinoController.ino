#include <NewPing.h>
#include "dht11.h"
#include <Wire.h>



/*************************
* PIN DEFINITIONS
* GAS SENSORS
**************************/
#define PIN_MQ2 A0
#define PIN_MQ4 A1

/*************************
* Gas sensor globals, these are circular buffers to store instant values
* We report the average of these circular buffers on the serial port
* Circular buffer for Sensors so that we can take a moving average
*************************/
#define SV_SIZE 100
int svMQ4[SV_SIZE];
int svMQ2[SV_SIZE];
// index into the circular buffers
int index = 0;

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

/**************************
*  SONAR GLOBALS
**************************/


#define trigPin_fwd 3
#define echoPin_fwd 2
#define trigPin_right 4
#define echoPin_right 5
#define trigPin_left 6
#define echoPin_left 7

#define SONAR_NUM 3 //Number of sonar sensors
#define MAX_DISTANCE 150 //Max distance cm
#define PING_INTERVAL 33 // Milliseconds between pings.

unsigned long pingTimer[SONAR_NUM]; // When each pings.
unsigned int cm[SONAR_NUM]; // Store ping distances.
uint8_t currentSensor = 0; // Which sensor is active.


NewPing sonar[SONAR_NUM] = {
  NewPing(trigPin_left, echoPin_left, MAX_DISTANCE),
  NewPing(trigPin_fwd, echoPin_fwd, MAX_DISTANCE),
  NewPing(trigPin_right, echoPin_right, MAX_DISTANCE)
};
/**
//Fwd Sonar
NewPing sonar_fwd(trigPin_fwd,echoPin_fwd);

//Right Sonar
NewPing sonar_right(trigPin_right, echoPin_right);

//Left Sonar
NewPing sonar_left(trigPin_left, echoPin_left);
**/

long sonarValue_fwd;
long sonarValue_right;
long sonarValue_left;

// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 115200 bits per second:
  Serial.begin(115200);
  //initSonar();
  pingTimer[0] = millis() + 75; //First ping start in ms
  for (uint8_t i = 1; i < SONAR_NUM; i++) {
    pingTimer[i] = pingTimer[i - 1] + PING_INTERVAL;
  }


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
  for (x; x < SV_SIZE; x++) {
    sum = sum + array[x];
  }
  int avg = sum / SV_SIZE;
  return avg;
}

void readHumiture() {
  // Humiture sensor is time sensitive and cannot be read too often and may give timeout error
  // just ignore the failed attempts as long as some attempts succeed. The humidity & temp this way is sampled
  // as fast the sensor suports
  int chk = DHT11.read(DHT11PIN);
  /*
  uncomment this code to do status check on hurmiture value being properly measured
  actual values are inside DHT11.humidity and DHT11.temperature, see output below
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

/***********
* read compass value
************/
void readCompass() {
  Wire.beginTransmission(compassSlaveAddress);
  Wire.write("A");
  Wire.endTransmission();
  delay(10);


  Wire.requestFrom(compassSlaveAddress, 2);
  int i = 0;
  byte headingData[2];
  while (Wire.available() && i < 2)
  {
    headingData[i] = Wire.read();
    i++;
  }
  int headingValue = headingData[0] * 256 + headingData[1];
  compassValue = "";
  compassValue += int(headingValue / 10);
  compassValue += ".";
  compassValue += int (headingValue % 10);
}

void initSonar() {
  //pinMode(trigPin_fwd, OUTPUT);
  //pinMode(echoPin_fwd, INPUT);
  pinMode(trigPin_right, OUTPUT);
  pinMode(echoPin_right, INPUT);
  //pinMode(trigPin_left, OUTPUT);
  //pinMode(echoPin_left, INPUT);
}

int count = 0;

long readSonar(int trigPin, int echoPin) {
  long duration;
  long sonarValue;

  // Send the Trigger pulse
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Wait for the echo
  duration = pulseIn(echoPin, HIGH, 50000);

  // compute the distance
  sonarValue = (duration / 2) / 29.1;
  Serial.print("SonarValue: ");
  Serial.print(count);
  Serial.print("   ");
  Serial.println(sonarValue);
  count = count + 1;
  return sonarValue;

  
}

//void readAllSonar() {
  //sonarValue_fwd = readSonar(trigPin_fwd, echoPin_fwd);
  //sonarValue_right = readSonar(trigPin_right, echoPin_right);
  //sonarValue_left = readSonar(trigPin_left, echoPin_left);
  //sonarValue_right = sonar_right.ping_in();
  //sonarValue_fwd = sonar_fwd.ping_in();
  //sonarValue_left = sonar_left.ping_in();
  /**
   if (sonarValue_right == 2) {
    return;
  }
  if (sonarValue_fwd == 2) {
    return;
  }
  if (sonarValue_left == 2) {
    return;
  }
  Serial.println("SNR F: ");
  Serial.println(sonarValue_fwd);
  Serial.println("SNR R: ");
  Serial.println(sonarValue_right);
  Serial.println("SNR L: ");
  Serial.println(sonarValue_left);
  **/
//}
void echoCheck() { // If ping echo, set distance to array. Calculating distance
  if (sonar[currentSensor].check_timer())
    cm[currentSensor] = sonar[currentSensor].ping_result / US_ROUNDTRIP_CM;
}
 
void oneSensorCycle() { // Printing sonar results.
  for (uint8_t i = 0; i < SONAR_NUM; i++) {
    Serial.print(i);
    Serial.print("=");
    Serial.print(cm[i]);
    Serial.print("cm ");
  }
  Serial.println();
}

void readAllSonar() {
  for (uint8_t i = 0; i < SONAR_NUM; i++) {
    if (millis() >= pingTimer[i]) {
      pingTimer[i] += PING_INTERVAL * SONAR_NUM;
      if (i == 0 && currentSensor == SONAR_NUM - 1)
        oneSensorCycle(); // Do something with results.
      sonar[currentSensor].timer_stop();
      currentSensor = i;
      cm[currentSensor] = 0;
      sonar[currentSensor].ping_timer(echoCheck);
    }
  }
}



/*********************************************
* Output sends all the data collected on the serial port
* using the following format
* <sensor_name>=<sensor_value>,<sensor_name>=<sensor_value>, ..... \n
* Example
* MQ4=10,MQ2=5,MQ3=54,HUM=35,TMP=32,CMP=120
**********************************************/
void output() {
  String output = "";
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
  //output += ",SNR_FWD=";
  //output += sonarValue_fwd;
  output += ",SNR_RHGT=";
  output += sonarValue_right;
  //output += ",SNR_LFT=";
  //output += sonarValue_left;
  Serial.println(output);
}

// the loop routine runs over and over again forever:
void loop() {  
  readAllSonar();
  //delay(100);
  return;
  readGasSensors();
 

  // Every 1000th value we send the output on serial port
  if (index == 0) {
    // Read the sensors that take time to read
    readHumiture();
    readCompass();
    readAllSonar();
    output();
  }


}

