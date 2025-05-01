#include <Wire.h>
#include <MPU6050.h>

MPU6050 mpu;
const int trigPin = 9;
const int echoPin = 10;
const int ledPin = 7;
const int buttonPin = 6;

bool lastState = HIGH;

void setup() {
  Serial.begin(9600);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(ledPin, OUTPUT);
  pinMode(buttonPin, INPUT_PULLUP);

  Wire.begin();
  mpu.initialize();
}

void loop() {
  // ——— Ultrasonic distance ———
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  long duration = pulseIn(echoPin, HIGH, 30000);
  float distance = -1;
  if (duration > 0) {
    float d = duration * 0.034 / 2.0;
    if (d <= 200) distance = d;
  }

  // ——— MPU6050 ———
  int16_t ax, ay, az, gx, gy, gz;
  mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);

  // ——— Button + LED ———
  int state = digitalRead(buttonPin);  // LOW = pressed
  digitalWrite(ledPin, state == LOW ? HIGH : LOW);
  int buttonVal = (state == LOW) ? 1 : 0;

  // ——— Output ———
  if (distance < 0) {
    Serial.print(-1);
  } else {
    Serial.print(distance, 2);
  }

  Serial.print(",");
  Serial.print(ax); Serial.print(",");
  Serial.print(ay); Serial.print(",");
  Serial.print(az); Serial.print(",");
  Serial.print(gx); Serial.print(",");
  Serial.print(gy); Serial.print(",");
  Serial.print(gz); Serial.print(",");
  Serial.println(buttonVal);  // button is last column

  delay(200);
}
