#include <ros.h>
#include <std_msgs/String.h>
// ROS Master needs to have a topic "ready" and must send it either "F" or "R"

# define STARTBUTTON 13
# define DIRECTION 5
# define SPEEDCONTROL 3
# define SPEED 43

//using factory max rpm: 500, since speed control : 0-5V, 1V ~ 500rpm
//conveyor isn't linear though so its a really really rough estimate ):

void moveForward() {
  analogWrite(SPEEDCONTROL, SPEED);
  digitalWrite(DIRECTION, LOW);
  digitalWrite(STARTBUTTON,LOW);
  delay(500);
}
void moveReverse() {
  analogWrite(SPEEDCONTROL, SPEED);
  digitalWrite(DIRECTION, HIGH);
  digitalWrite(STARTBUTTON,LOW);
}

void stop_conveyor() {
  digitalWrite(STARTBUTTON, HIGH);
}

void setup() {
  pinMode(STARTBUTTON, OUTPUT);
  pinMode(DIRECTION, OUTPUT);
  pinMode(SPEEDCONTROL, OUTPUT);

  Serial.begin(9600);
  digitalWrite(STARTBUTTON, HIGH);
}

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readString();
    switch(data.charAt(0)) {
      case 'F': moveForward();
      case 'R': moveReverse();
      case 'S': stop_conveyor();
    }
    Serial.flush();
  }
}
