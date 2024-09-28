#include <Servo.h>

// Create a servo object for controlling one servo
Servo myServo;

// Variables to store LED pin numbers
int ledPins[] = {2, 3, 4, 5, 6};  // LEDs representing 1 to 5 fingers

// Angle for each finger count (0-indexed, 0 fingers = 0 degrees, 1 finger = 30, etc.)
int angles[] = {0, 30, 60, 90, 120, 150};  // Adjusted for up to 5 fingers

void setup() {
  // Attach the servo to its corresponding pin
  myServo.attach(9);  // Attach the servo to pin 9 (or any other pin you want)

  // Set the pins as OUTPUT for LEDs
  for (int i = 0; i < 5; i++) {
    pinMode(ledPins[i], OUTPUT);
  }

  // Initialize the servo to 0 degrees
  myServo.write(0);

  // Start serial communication at 9600 baud
  Serial.begin(9600);
  Serial.println("Arduino is ready to receive finger count data...");
}

void loop() {
  // Check if there is data available from the serial port
  if (Serial.available() > 0) {
    // Read the number of fingers detected as an integer
    int fingersUp = Serial.readString().toInt(); 

    // Print the number of fingers received
    Serial.print("Received fingers up: ");
    Serial.println(fingersUp);

    // Ensure the value is between 0 and 5 (inclusive)
    if (fingersUp >= 0 && fingersUp <= 5) {
      // Rotate the servo to the appropriate angle
      int angle = angles[fingersUp];
      myServo.write(angle);
      
      // Print the angle the servo is rotating to
      Serial.print("Rotating servo to ");
      Serial.print(angle);
      Serial.println(" degrees");

      // Control the LEDs based on the number of fingers up
      for (int i = 0; i < 5; i++) {
        if (i < fingersUp) {
          digitalWrite(ledPins[i], HIGH);  // Turn on the LED for this finger count
          Serial.print("Turning on LED on pin ");
          Serial.println(ledPins[i]);
        } else {
          digitalWrite(ledPins[i], LOW);   // Turn off the LEDs for counts above the finger count
          Serial.print("Turning off LED on pin ");
          Serial.println(ledPins[i]);
        }
      }
    } else {
      // Print an error if the number of fingers is outside the valid range
      Serial.println("Error: Invalid finger count. Expected a value between 0 and 5.");
    }
  }
}
