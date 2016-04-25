/*
Arduino sketch to control a set of stepper motors to particular positions over serial.
It responds to pairs of bytes received over serial which represent the servo ID and the
position it is to move to.
*/

#include <Servo.h> 

// ------ Configuration settings

byte servoPins[] = {10};              // output pins used for each of the servos
byte positionAngles[] = {0, 200};     // angles to be used for each position of the servos

// ------


const byte numServos = sizeof(servoPins)/sizeof(byte);
Servo servos[numServos];  
const byte numPositions = sizeof(positionAngles)/sizeof(byte);
byte ledPin = 13;                     // use the onboard LED pin for debugging purposes

// This function is run when the arduino turns on (only once)
void setup() 
{ 
    pinMode(ledPin, OUTPUT);          // set the LED's pin as an 'output' pin
    Serial.begin(9600);               // initialise the serial connection at 9600 baud
    while (!Serial) {
        ;                             // wait for the connection to initalise 
    }
    for (byte i = 0; i < numServos; i++) {
        servos[i].attach(servoPins[i]);
    }
} 

// This function is run continuously
void loop() 
{
    if (Serial.available() >= 2) {                     // listen for a command over serial
          digitalWrite(ledPin, !digitalRead(ledPin));  // toggle LED to show something received
          // get incoming data:
          byte servo = Serial.read();
          byte posn = Serial.read();
          setServoPosition(servo, posn);               // move the servo to the requested position
    }
} 

// Send a command to servo `servo` to move to position `posn`
void setServoPosition(byte servo, byte posn) {
    if (servo >= 0 && servo < numServos && posn >= 0 && posn <= numPositions) {
        servos[servo].write(positionAngles[posn]);       
    }
}

