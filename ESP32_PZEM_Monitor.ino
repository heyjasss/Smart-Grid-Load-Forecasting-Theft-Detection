#include <PZEM004Tv30.h>

// ================= PZEM 1 =================
PZEM004Tv30 pzem1(Serial2, 16, 17);

// ================= PZEM 2 =================
HardwareSerial SerialPZEM2(1);
PZEM004Tv30 pzem2(SerialPZEM2, 32, 33);

// ================= RELAY + BUZZER =================
#define RELAY_PIN 26
#define BUZZER_PIN 27

// Theft threshold
const float THEFT_THRESHOLD = 0.439;

// Theft must continue for 3 readings
const int REQUIRED_ABNORMAL_READINGS = 3;

int abnormalCount = 0;

void setup() {

  Serial.begin(9600);

  Serial2.begin(9600, SERIAL_8N1, 16, 17);
  SerialPZEM2.begin(9600, SERIAL_8N1, 32, 33);

  pinMode(RELAY_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);

  // Active LOW relay = HIGH means OFF
  digitalWrite(RELAY_PIN, HIGH);

  // Buzzer OFF
  digitalWrite(BUZZER_PIN, LOW);

  delay(1000);

  Serial.println();
  Serial.println("======================================");
  Serial.println(" SMART GRID THEFT DETECTION SYSTEM");
  Serial.println("======================================");
  Serial.println("PZEM1 RX/TX : 16/17");
  Serial.println("PZEM2 RX/TX : 32/33");
  Serial.println("Relay GPIO  : 26");
  Serial.println("Buzzer GPIO : 27");
  Serial.println("Threshold   : 0.439 W");
  Serial.println("System Ready");
  Serial.println();
}

void loop() {

  // -------- PZEM 1 --------
  float v1 = pzem1.voltage();
  float c1 = pzem1.current();
  float p1 = pzem1.power();

  // -------- PZEM 2 --------
  float v2 = pzem2.voltage();
  float c2 = pzem2.current();
  float p2 = pzem2.power();

  // -------- Invalid readings --------
  if (isnan(v1)) v1 = 0;
  if (isnan(c1)) c1 = 0;
  if (isnan(p1)) p1 = 0;

  if (isnan(v2)) v2 = 0;
  if (isnan(c2)) c2 = 0;
  if (isnan(p2)) p2 = 0;

  // -------- Invalid PZEM data --------
  if (p1 <= 0 || p2 <= 0) {

    abnormalCount = 0;

    digitalWrite(RELAY_PIN, HIGH);
    digitalWrite(BUZZER_PIN, LOW);

    Serial.println("INVALID PZEM READING");

    delay(2000);
    return;
  }

  // -------- Power difference --------
  float difference = abs(p1 - p2);

  // -------- Abnormal counter --------
  if (difference > THEFT_THRESHOLD) {
    abnormalCount++;
  }
  else {
    abnormalCount = 0;
  }

  // -------- THEFT / NORMAL --------
  if (abnormalCount >= REQUIRED_ABNORMAL_READINGS) {

    digitalWrite(RELAY_PIN, LOW);
    digitalWrite(BUZZER_PIN, HIGH);

    Serial.println("!!! THEFT SUSPECTED !!!");

  }
  else {

    digitalWrite(RELAY_PIN, HIGH);
    digitalWrite(BUZZER_PIN, LOW);

    Serial.println("NORMAL");
  }

  // -------- Detailed output --------
  Serial.print("PZEM1: ");
  Serial.print(v1, 2);
  Serial.print(" V, ");

  Serial.print(c1, 3);
  Serial.print(" A, ");

  Serial.print(p1, 2);
  Serial.print(" W");

  Serial.print("     |     PZEM2: ");

  Serial.print(v2, 2);
  Serial.print(" V, ");

  Serial.print(c2, 3);
  Serial.print(" A, ");

  Serial.print(p2, 2);
  Serial.print(" W");

  Serial.print("     |     Difference: ");

  Serial.print(difference, 3);
  Serial.print(" W");

  Serial.print("     |     Status: ");

  if (abnormalCount >= REQUIRED_ABNORMAL_READINGS) {
    Serial.println("THEFT SUSPECTED");
  }
  else {
    Serial.println("NORMAL");
  }

  // -------- CSV output --------
  Serial.print(v1, 2);
  Serial.print(",");

  Serial.print(c1, 4);
  Serial.print(",");

  Serial.print(p1, 2);
  Serial.print(",");

  Serial.print(v2, 2);
  Serial.print(",");

  Serial.print(c2, 4);
  Serial.print(",");

  Serial.print(p2, 2);
  Serial.print(",");

  Serial.print(difference, 3);
  Serial.print(",");

  if (abnormalCount >= REQUIRED_ABNORMAL_READINGS) {
    Serial.println("THEFT SUSPECTED");
  }
  else {
    Serial.println("NORMAL");
  }

  delay(2000);
}