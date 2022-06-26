#include<Wire.h>
const int MPU_addr=0x68;
float AcX,AcY,AcZ;
float Val_X,Val_Y,Val_Z;

#define AcX_offset 5700
#define AcX_min -10700
#define AcX_max 22200

#define AcY_offset 0
#define AcY_min -16200
#define AcY_max 16400

#define AcZ_offset -3000
#define AcZ_min -19700
#define AcZ_max 14100

void setup(){
  Wire.begin();
  Wire.beginTransmission(MPU_addr);
  Wire.write(0x6B);
  Wire.write(0);
  Wire.endTransmission(true);
  Serial.begin(9600);
}
void loop(){
  Wire.beginTransmission(MPU_addr);
  Wire.write(0x3B);
  Wire.endTransmission(false);
  Wire.requestFrom(MPU_addr,14,true);
  AcX=Wire.read()<<8|Wire.read();
  AcY=Wire.read()<<8|Wire.read();
  AcZ=Wire.read()<<8|Wire.read();
  Val_X=(AcX-AcX_offset)*180/(AcX_max-AcX_min);
  Val_Y=(AcY-AcY_offset)*180/(AcY_max-AcY_min);
  Val_Z=(AcZ-AcZ_offset)*180/(AcZ_max-AcZ_min);
  Serial.print("AcX = ");
  Serial.print(Val_X);
  Serial.print(" | AcY = ");
  Serial.print(Val_Y);
  Serial.print(" | AcZ = ");
  Serial.println(Val_Z);
}
