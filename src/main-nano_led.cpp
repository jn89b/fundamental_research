#include <Arduino.h>
#include <CAN.h>

#define LED_PIN    3    // On-board LED on most Arduinos
#define DIST_ID    0x12  // Must match sendDistanceCAN’s ID
#define THRESH_CM  10    // turn LED on if distance < 20 cm

void setup() {
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);

  Serial.begin(9600);
  while (!Serial);

  // Start CAN at 500 kbps (match your sender)
  if (!CAN.begin(1000E3)) {
    Serial.println("ERROR: CAN init failed");
    while (1);
  }
  // Only accept the sonar ID
  CAN.filter(DIST_ID);

  Serial.println("CAN sonar-reader up @500 kbps");
}

void loop() {
  int dlc = CAN.parsePacket();
  if (dlc > 0 && CAN.packetId() == DIST_ID) {
    // We expect exactly 1 byte (mm/10)
    uint8_t dist10mm = CAN.read();
    // (If dlc>1, you could read extra bytes or flush them)
    
    float dist_cm = dist10mm / 10.0f;
    Serial.print("Sonar: ");
    Serial.print(dist_cm, 1);
    Serial.println(" cm");

    // LED logic
    if (dist_cm < THRESH_CM) {
      digitalWrite(LED_PIN, HIGH);
    } else {
      digitalWrite(LED_PIN, LOW);
    }
  }
}
