#include <Wire.h>
#include <MPU6050.h>

MPU6050 mpu;
const int trigPin = 9;
const int echoPin = 10;

void setup() {
  Serial.begin(9600);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  Wire.begin();
  mpu.initialize();
  // (Optional) check connection silently
  // if (!mpu.testConnection()) { /* handle error */ }
}

void loop() {
  // ——— Ultrasonic distance measurement ———
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

  // ——— MPU6050 accelerometer & gyro ———
  int16_t ax, ay, az, gx, gy, gz;
  mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);

  // ——— CSV Output: distance,ax,ay,az,gx,gy,gz ———
  if (distance < 0) {
    Serial.print(-1);            // use –1 for out-of-range
  } else {
    Serial.print(distance, 2);   // two decimal places
  }
  Serial.print(",");
  Serial.print(ax); Serial.print(",");
  Serial.print(ay); Serial.print(",");
  Serial.print(az); Serial.print(",");
  Serial.print(gx); Serial.print(",");
  Serial.print(gy); Serial.print(",");
  Serial.println(gz);

  delay(500);
}
