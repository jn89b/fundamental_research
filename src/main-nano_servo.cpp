#include <Arduino.h>
#include <CAN.h>
#include <Servo.h>

Servo myservo;  // create servo object to control a servo
int pos = 0;    // variable to store the servo position
const uint32_t PIXHAWK_RPY_ID = 0x2;
const float    INT16_MAX_RAD = 32767.0f;

// -----------------------------------------------------------------------------
// Attempts to read one roll-pitch-yaw frame from CAN.
// If a valid frame arrives, decodes it into radians and returns true.
// Otherwise returns false immediately.
// -----------------------------------------------------------------------------
bool readRPY(float &roll, float &pitch, float &yaw) {
  int packetSize = CAN.parsePacket();
  if (packetSize == 0 || CAN.packetId() != PIXHAWK_RPY_ID) {
    // no packet or not the ID we want
    return false;
  }



  // we expect at least 6 bytes: R_hi,R_lo,P_hi,P_lo,Y_hi,Y_lo
  if (packetSize < 8) {
    // malformed—flush and skip
    while (CAN.available()) CAN.read();
    return false;
  }

  // read high/low bytes for each axis
  int16_t r_i = (int16_t)((CAN.read() << 8) | CAN.read());
  int16_t p_i = (int16_t)((CAN.read() << 8) | CAN.read());
  int16_t y_i = (int16_t)((CAN.read() << 8) | CAN.read());
  // drop any padding
  while (CAN.available()) CAN.read();

  // convert back to radians: (int16/32767) * π
  roll  = (float)r_i / INT16_MAX_RAD * PI;
  pitch = (float)p_i / INT16_MAX_RAD * PI;
  yaw   = (float)y_i / INT16_MAX_RAD * PI;

  // Convert to degrees
  roll  = roll * 180.0f / PI;
  pitch = pitch * 180.0f / PI;
  yaw   = yaw * 180.0f / PI;

  return true;
}

void moveServo(int position)
{
  myservo.write(position); // tell servo to go to position in variable 'pos'
  delay(15);               // waits 15ms for the servo to reach the position
}

void setup() {
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object

  Serial.begin(9600);
  while (!Serial);

  if (!CAN.begin(1000E3)) {
    Serial.println("Error starting CAN");
    while (1);
  }
  CAN.filter(PIXHAWK_RPY_ID);
  Serial.println("CAN listener up @ 500 kbps, waiting for RPY frames…");
}

void loop() {
    // send packet: id is 11 bits, packet can contain up to 8 bytes of data
    // Serial.print("Sending packet ... ");

    // Serial.println("done");
    float roll, pitch, yaw;

    if (readRPY(roll, pitch, yaw)) {
      Serial.print("RPY [rad]: ");
      Serial.print(roll,  3);
      Serial.print(" , ");
      Serial.print(pitch, 3);
      Serial.print(" , ");
      Serial.println(yaw, 3);
    }
    // else{
    //   Serial.println("No packet or not the ID we want");
    // }
    // send extended packet: id is 29 bits, packet can contain up to 8 bytes of data
    moveServo(roll);

    // for (int pos = 0; pos <= 100; pos += 1)
    // { // goes from 0 degrees to 180 degrees
    //   moveServo(pos);              // tell servo to go to position in variable 'pos'
    // }
    // for (int pos = 100; pos >= 0; pos -= 1) 
    // { // goes from 180 degrees to 0 degrees
    //   moveServo(pos);              // tell servo to go to position in variable 'pos'
    // }
}
