int fsr = A0;
int col = 7;

void setup() {
  Serial.begin(9600);
  pinMode(fsr, INPUT);
  pinMode(col, INPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (digitalRead(col) == 0) {
    Serial.println(analogRead(fsr));
    delay(1000);
  }
delay(500);
}
