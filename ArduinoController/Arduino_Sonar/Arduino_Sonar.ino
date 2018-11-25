#include <NewPing.h>


#define MAX_DISTANCE 20
#define SONAR_NUM 7

NewPing sonar[SONAR_NUM] = {
  NewPing(22, 23, MAX_DISTANCE),
  NewPing(24, 25, MAX_DISTANCE),
  NewPing(26, 27, MAX_DISTANCE),
  NewPing(28, 29, MAX_DISTANCE),
  NewPing(30, 31, MAX_DISTANCE),
  NewPing(32, 33, MAX_DISTANCE),
  NewPing(34, 35, MAX_DISTANCE)
};


void setup() {
 Serial.begin(115200);
 Serial.println("Setup done");
}

void loop() {
  delay(100);
  //sonar count starts at far left when facing front
  //d1 is left side
  int d1 = sonar[0].ping_cm();
  int d2 = sonar[1].ping_cm();
  int d3 = sonar[2].ping_cm();
  //d4 is center
  int d4 = sonar[3].ping_cm();
  int d5 = sonar[4].ping_cm();
  int d6 = sonar[5].ping_cm();
  //d7 is right side
  int d7 = sonar[6].ping_cm();
  String output = "";
  output += ",SNR_1=";
  //Left most sonar (robot's front)
  output += d1;
  output += ",SNR_2=";
  output += d2;
  output += ",SNR_3=";
  output += d3;
  output += ",SNR_4=";
  //Center Sonar
  output += d4;
  output += ",SNR_5=";
  output += d5;
  output += ",SNR_6=";
  output += d6;
  output += ",SNR_7=";
  //Rightmost sonar (robot's front)
  output += d7;
  Serial.println(output);
}
