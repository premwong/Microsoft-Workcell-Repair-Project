#include <ros.h>
// ROS Master needs to have a topic "ready" and must send it either "F" or "R"

# define STARTBUTTON 13
# define DIRECTION 5
# define SPEEDCONTROL 3
# define SPEED 43

//using factory max rpm: 500, since speed control : 0-5V, 1V ~ 500rpm


void setup() {
  pinMode(STARTBUTTON, OUTPUT);
  pinMode(DIRECTION, OUTPUT);
  pinMode(SPEEDCONTROL, OUTPUT);

  Serial.begin(9600);
  digitalWrite(STARTBUTTON, HIGH);
  analogWrite(SPEEDCONTROL, SPEED);
}

int global_direction = 0;

void loop() {
  if (Serial.available() > 0) {
    char data = Serial.readString().charAt(0);
    switch(data) {
      case 'F': global_direction = 1;
                break;
      case 'R': global_direction = -1;
                break;
      case 'S': global_direction = 0;
                break;
    }
    if (global_direction == 1) {
      digitalWrite(DIRECTION, LOW);
    } else if (global_direction == -1) {
      digitalWrite(DIRECTION, HIGH);
    }
    int32_t state = ((global_direction == 1) || (global_direction == -1)) ? LOW : HIGH;
    digitalWrite(STARTBUTTON, state);
    Serial.flush();
  }
}
