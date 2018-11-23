#include <NewPing.h>


#define MAX_DISTANCE 100
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
  Serial.print(d1);
  Serial.print("\t");
  Serial.print(d2);
  Serial.print("\t");
  Serial.print(d3);
  Serial.print("\t");
  Serial.print(d4);
  Serial.print("\t");
  Serial.print(d5);
  Serial.print("\t");
  Serial.print(d6);
  Serial.print("\t");
  Serial.print(d7);
  Serial.println("\tcm");
}
