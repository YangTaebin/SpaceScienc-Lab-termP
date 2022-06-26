void setup() {
  Serial.begin(9600);
}

void loop() {
  int vol_in = analogRead(A0);
  float voltage = vol_in * (5.0 / 1023);
  Serial.print(voltage);
  Serial.println("V");
}
