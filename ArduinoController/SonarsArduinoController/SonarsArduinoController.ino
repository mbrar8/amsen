#include <NewPing.h>


#define MAX_DISTANCE 8
#define SONAR_NUM 7

NewPing sonar[SONAR_NUM] = {
  NewPing(35, 34, MAX_DISTANCE),
  NewPing(37, 36, MAX_DISTANCE),
  NewPing(25, 24, MAX_DISTANCE),
  NewPing(26, 27, MAX_DISTANCE),
  NewPing(29, 28, MAX_DISTANCE),
  NewPing(31, 30, MAX_DISTANCE),
  NewPing(33, 32, MAX_DISTANCE)
};


void setup() {
 Serial.begin(115200);
 Serial.println("Setup done");
}

void output() {
  int d1 = sonar[0].ping_cm();
  int d2 = sonar[1].ping_cm();
  int d3 = sonar[2].ping_cm();
  int d4 = sonar[3].ping_cm();
  int d5 = sonar[4].ping_cm();
  int d6 = sonar[5].ping_cm();
  int d7 = sonar[6].ping_cm();
  String output = "";
  output += "Sonar1=";
  output += d1;
  output += ",Sonar2=";
  output += d2;
  output += ",Sonar3=";
  output += d3;
  output += ",Sonar4=";
  output += d4;
  output += ",Sonar5=";
  output += d5;
  output += ",Sonar6=";
  output += d6;
  output += ",Sonar7=";
  output += d7;
  Serial.println(output);
  
}

void loop() {
  delay(500);
  output();
}
