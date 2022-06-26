#define stepSize 1.8
#define motor1_dir 2
#define motor1_step 3
#define motor2_dir 4
#define motor2_step 5

void setup() {
  pinMode(motor1_dir, OUTPUT);
  pinMode(motor1_step, OUTPUT);
  pinMode(motor2_dir, OUTPUT);
  pinMode(motor2_step, OUTPUT);
  Serial.begin(9600);
}

int move_angle(String direc, int angle, int motor_num, float vel) {
  int X = (int) 2*PI/((360/stepSize)*0.000002*vel);
  Serial.println(X);
  int dirPin=2; int stepPin = 3;
  if (motor_num == 0) {
    dirPin = 2;
    stepPin = 3;
  }
  else if (motor_num == 1) {
    dirPin = 4;
    stepPin = 5;
  }
  Serial.print(dirPin);
  Serial.println(stepPin);
  if (direc == "CW"){digitalWrite(dirPin, LOW);}
  else if (direc == "CC") {digitalWrite(dirPin, HIGH);}
  int stepsize = round(angle / stepSize);
  for (int i = 0; i < stepsize; i++){
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(X);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(X);
  }
  return 0;
}

void loop() {
  String direc = "";
  int angle = 0;
  int motor_num = 0;
  float vel = 0.0;
  int last_index = 0;
  int argument_num = 0;
  String str_serial = Serial.readString();
  if (str_serial.length() > 0){
    str_serial = str_serial + " ";
    for (int i = 0; i < str_serial.length(); i++) {
      if ((str_serial.charAt(i) == ' ') && (argument_num == 0)){
        direc = str_serial.substring(last_index, i);
        last_index = i;
        argument_num = argument_num + 1;
      }
      else if ((str_serial.charAt(i) == ' ') && (argument_num == 1)){
        angle = str_serial.substring(last_index, i).toInt();
        last_index = i;
        argument_num = argument_num + 1;
      }
      else if ((str_serial.charAt(i) == ' ') && (argument_num == 2)){
        motor_num = str_serial.substring(last_index, i).toInt();
        last_index = i;
        argument_num = argument_num + 1;
      }
      else if ((str_serial.charAt(i) == ' ') && (argument_num == 3)){
        vel = str_serial.substring(last_index, i).toFloat();
        last_index = i;
        argument_num = argument_num + 1;
      }
    }
    move_angle(direc, angle, motor_num, vel);
    Serial.print(direc);
    Serial.print(" ");
    Serial.print(angle);
    Serial.print(" ");
    Serial.print(motor_num);
    Serial.print(" ");
    Serial.println(vel);
    direc = "";
    angle = 0;
    motor_num = 0;
    last_index = 0;
    argument_num = 0;
  }
}
