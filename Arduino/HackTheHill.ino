#include <Servo.h>

// Create a servo object for controlling one servo
Servo myServo;

// Variables to store LED pin numbers
int ledPins[] = {2, 3, 4, 5, 6};  // Red, Blue, White, Green, Yellow LEDs for 1-5 fingers

// Angle for each finger count (1 finger = 30 degrees, 2 fingers = 60, etc.)
int angles[] = {30, 60, 90, 120, 150};  // Servo angles for 1-5 fingers

// Default delay time after a gesture is detected (in milliseconds)
unsigned long gestureTimeout = 3000;  // 3 seconds
unsigned long lastGestureTime = 0;    // To keep track of the last time a gesture was detected

void setup() {
  // Attach the servo to its corresponding pin
  myServo.attach(9);  // Attach the servo to pin 9

  // Set the LED pins as OUTPUT
  for (int i = 0; i < 5; i++) {
    pinMode(ledPins[i], OUTPUT);
  }

  // Initialize the servo to 0 degrees (default position)
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

    // Ensure the value is between 1 and 5 (inclusive)
    if (fingersUp >= 1 && fingersUp <= 5) {
      // Rotate the servo to the appropriate angle based on the number of fingers
      int angle = angles[fingersUp - 1];  // Adjust index (1 finger = 30°, 2 fingers = 60°, etc.)
      myServo.write(angle);
      
      // Print the angle the servo is rotating to
      Serial.print("Rotating servo to ");
      Serial.print(angle);
      Serial.println(" degrees");

      // Control the LEDs
      for (int i = 0; i < 5; i++) {
        if (i == (fingersUp - 1)) {
          digitalWrite(ledPins[i], HIGH);  // Turn on the LED corresponding to the finger count
          Serial.print("Turning on LED on pin ");
          Serial.println(ledPins[i]);
        } else {
          digitalWrite(ledPins[i], LOW);   // Turn off the other LEDs
          Serial.print("Turning off LED on pin ");
          Serial.println(ledPins[i]);
        }
      }

      // Record the current time as the last gesture time
      lastGestureTime = millis();
    } else {
      // Print an error if the number of fingers is outside the valid range
      Serial.println("Error: Invalid finger count. Expected a value between 1 and 5.");
    }
  }

  // Check if the timeout has passed since the last gesture detection
  if (millis() - lastGestureTime > gestureTimeout) {
    // Return the servo to the default (0 degrees) position
    myServo.write(0);

    // Turn off all LEDs
    for (int i = 0; i < 5; i++) {
      digitalWrite(ledPins[i], LOW);
    }

    // Print a message indicating the reset action
    Serial.println("Returning to default position (0 degrees) and turning off LEDs.");

    // Reset lastGestureTime to prevent continuous execution
    lastGestureTime = millis() + gestureTimeout;  // Prevent this code from running again until the next valid gesture
  }
}
