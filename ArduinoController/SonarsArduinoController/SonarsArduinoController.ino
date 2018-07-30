#include <NewPing.h>


#define MAX_DISTANCE 10
#define SONAR_NUM 7

NewPing sonar[SONAR_NUM] = {
  NewPing(23, 22, MAX_DISTANCE),
  NewPing(25, 24, MAX_DISTANCE),
  NewPing(27, 26, MAX_DISTANCE),
  NewPing(29, 28, MAX_DISTANCE),
  NewPing(31, 30, MAX_DISTANCE),
  NewPing(33, 32, MAX_DISTANCE),
  NewPing(35, 34, MAX_DISTANCE)
};


void setup() {
 Serial.begin(115200);
 Serial.println("Setup done");
}

void loop() {
  delay(100);
  int d1 = sonar[0].ping_cm();
  int d2 = sonar[1].ping_cm();
  int d3 = sonar[2].ping_cm();
  int d4 = sonar[3].ping_cm();
  int d5 = sonar[4].ping_cm();
  int d6 = sonar[5].ping_cm();
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
