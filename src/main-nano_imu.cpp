#include <Arduino.h>
#include <CAN.h>

const uint32_t PIXHAWK_RPY_ID = 0x2;
const float    INT16_MAX_RAD = 32767.0f;
float roll, pitch, yaw;
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
  if (packetSize < 6) {
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

  return true;
}

void setup() {
  Serial.begin(115200);
  while (!Serial);

  if (!CAN.begin(1000E3)) {
    Serial.println("Error starting CAN");
    while (1);
  }
  CAN.filter(PIXHAWK_RPY_ID);
  Serial.println("CAN listener up @ 1000 kbps, waiting for RPY frames…");
}

void loop() {

  if (readRPY(roll, pitch, yaw)) {
    Serial.print("RPY [rad]: ");
    Serial.print(roll,  3);
    Serial.print(" , ");
    Serial.print(pitch, 3);
    Serial.print(" , ");
    Serial.println(yaw, 3);
  }
  // you can do other work here, this returns immediately if no new frame
}
