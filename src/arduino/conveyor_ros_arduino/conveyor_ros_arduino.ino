#include <ros.h>
#include <std_msgs/String.h>
// ROS Master needs to have a topic "ready" and must send it either "F" or "R"

# define STARTBUTTON 13
# define DIRECTION 5
# define SPEEDCONTROL 3
# define TIME_DELAY 5000

void moveForward() {
  analogWrite(SPEEDCONTROL, 50);
  digitalWrite(DIRECTION, LOW);
  digitalWrite(STARTBUTTON,LOW);
  delay(TIME_DELAY);
  digitalWrite(STARTBUTTON, HIGH);
}
void moveReverse() {
  analogWrite(SPEEDCONTROL, 50);
  digitalWrite(DIRECTION, HIGH);
  digitalWrite(STARTBUTTON,LOW);
  delay(TIME_DELAY);
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
    
    if (data.equals("F")) {
      digitalWrite(7, HIGH); // This is just for testing
      delay(3000);
      digitalWrite(7,LOW);
      moveForward();
    } else if (data.equals("R")) {
      moveReverse();
    }
    Serial.flush();
  }
}
