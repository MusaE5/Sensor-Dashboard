// Phase 1 - Distance Sensor Test (HC-SR04)

#define trigPin 9
#define echoPin 10

void setup() {
  Serial.begin(9600);          // Start serial communication
  pinMode(trigPin, OUTPUT);    // Trig pin will send the pulse
  pinMode(echoPin, INPUT);     // Echo pin will receive the pulse
}

void loop() {
  // Send a 10 microsecond pulse to trigger measurement
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Read the time for echo to return
  long duration = pulseIn(echoPin, HIGH);

  // Calculate distance in cm
  float distance = duration * 0.034 / 2;

  // Output distance
  Serial.print("Dist:");
  Serial.println(distance);

  delay(200);  // Wait a little before next measurement
}
