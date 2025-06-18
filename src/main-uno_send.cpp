#include <Arduino.h>
#include <CAN.h>

// put function declarations here:
int myFunction(int, int);
void setup();
void loop();


void setup() {
  Serial.begin(9600);
  while (!Serial);

  Serial.println("CAN Sender");
  bool ok = CAN.begin(1000E3);
  Serial.print("CAN.begin(1000E3) returned ");
  Serial.println(ok ? "OK" : "FAIL");

  if (!ok) {
    while (1) {
      Serial.println("ERROR: CAN bus init failed!");
      delay(1000);
    }
  }
}

void loop() {
    // send packet: id is 11 bits, packet can contain up to 8 bytes of data
    Serial.print("Sending packet ... ");

    CAN.beginPacket(0x12);
    CAN.write('F');
    CAN.write('U');
    CAN.write('C');
    CAN.write('K');
    CAN.endPacket();

    Serial.println("done");

    delay(50);

    // send extended packet: id is 29 bits, packet can contain up to 8 bytes of data
    Serial.print("Sending extended packet ... ");

    // CAN.beginExtendedPacket(0xabcdef);
    // CAN.write('T');
    // CAN.write('R');
    // CAN.write('U');
    // CAN.write('M');
    // CAN.write('S');
    // CAN.endPacket();

    // Serial.println("done");
    // delay(1000);
}

// put function definitions here:
int myFunction(int x, int y) {
  return x + y;
}