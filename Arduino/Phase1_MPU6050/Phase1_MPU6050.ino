// Phase 1 - MPU6050 Accelerometer Test

#include <Wire.h>
#include <MPU6050.h>

MPU6050 mpu;

void setup() {
  Serial.begin(9600);      // Start serial communication
  Wire.begin();            // Start I2C communication
  mpu.initialize();        // Initialize MPU6050
}

void loop() {
  int16_t ax, ay, az;
  
  // Read raw acceleration values
  mpu.getAcceleration(&ax, &ay, &az);

  // Convert raw z-axis value to "g" (gravity units)
  float z_g = az / 16384.0;

  // Output Z-axis acceleration
  Serial.print("Z:");
  Serial.println(z_g, 2);  // 2 decimal places

  delay(200);  // Wait a little before next read
}
