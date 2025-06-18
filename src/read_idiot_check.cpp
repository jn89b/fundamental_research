#include <Arduino.h>
#include <CAN.h>

// If your MCP2515 module uses non-default CS/INT pins,
// call CAN.begin(500E3, /*CSpin=*/9, /*INTpin=*/3) instead of CAN.begin(500E3).

void setup() {
  Serial.begin(9600);
  while (!Serial);

  // initialize CAN at 500 kbps
  if (!CAN.begin(1000E3)) {
    Serial.println("Error: CAN init failed");
    while (1);
  }
  Serial.println("CAN bus reader @500 kbps");
}

void loop() {
  // parsePacket() returns the number of data bytes (0–8) if a frame has arrived
  int dlc = CAN.parsePacket();
  if (dlc > 0) {
    // print arbitration ID in hex
    Serial.print("ID=0x");
    Serial.print(CAN.packetId(), HEX);
    // print Data Length Code
    Serial.print("  DLC=");
    Serial.print(dlc);
    // print each data byte
    Serial.print("  DATA=");
    while (CAN.available()) {
      uint8_t b = CAN.read();
      if (b < 0x10) Serial.print('0');  // leading zero
      Serial.print(b, HEX);
      Serial.print(' ');
    }
    Serial.println();
  }
}
