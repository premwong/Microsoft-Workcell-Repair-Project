#include <ros.h>
#include <std_msgs/String.h>
// ROS Master needs to have a topic "ready" and must send it either "F" or "R"

# define STARTBUTTON 13
# define DIRECTION 5
# define SPEEDCONTROL 3

//using factory max rpm: 500, since speed control : 0-5V, 1V ~ 500rpm

void moveForward() {
  analogWrite(SPEEDCONTROL, 30);
  digitalWrite(DIRECTION, LOW);
  digitalWrite(STARTBUTTON,LOW);
}
void moveReverse() {
  analogWrite(SPEEDCONTROL, 30);
  digitalWrite(DIRECTION, HIGH);
  digitalWrite(STARTBUTTON,LOW);
}

void stop() {
  digitalWrite(STARTBUTTON, HIGH);
}

void setup() {
  pinMode(STARTBUTTON, OUTPUT);
  pinMode(DIRECTION, OUTPUT);
  pinMode(SPEEDCONTROL, OUTPUT);
  pinMode(7,OUTPUT); // testing

  Serial.begin(9600);
  digitalWrite(STARTBUTTON, HIGH);
}

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readString();
    switch(data) {
      case "F": moveForward();
      case "R": moveReverse();
      case "S": stop();
    }
    Serial.flush();
  }
}
