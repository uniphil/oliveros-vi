void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  byte state;
  if (Serial.available()) {
    state = Serial.read();
    digitalWrite(LED_BUILTIN, state != '0');
  }
}
