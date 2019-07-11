#include <SPI.h>
#include <MFRC522.h>

#define RST_PIN         9          // Configurable, see typical pin layout above
#define SS_PIN          10         // Configurable, see typical pin layout above
#define buzz            8
#define led             7
MFRC522 mfrc522(SS_PIN, RST_PIN);  // Create MFRC522 instance
String CardID="";
void setup() {
  pinMode(buzz,OUTPUT);
  Serial.begin(9600);   // Initialize serial communications with the PC
  SPI.begin();      // Init SPI bus
  mfrc522.PCD_Init();   // Init MFRC522
}

void loop() {
  digitalWrite(led,LOW);
  while(Serial.available()==0){
  // Reset the loop if no new card present on the sensor/reader. This saves the entire process when idle.
  if ( ! mfrc522.PICC_IsNewCardPresent()) {
    return;
  }

  // Select one of the cards
  if ( ! mfrc522.PICC_ReadCardSerial()) {
    return;
  }
  
  for (byte i = 0; i < mfrc522.uid.size; i++) {
     CardID += mfrc522.uid.uidByte[i];
     }
  digitalWrite(led,HIGH);
  Serial.println(CardID);
  delay(1000);
  CardID = "";
}
//Serial.println(Serial.readString());
if (Serial.readString() == "m"){
  digitalWrite(buzz,HIGH);
  delay(1000);
  digitalWrite(led,LOW);
  digitalWrite(buzz,LOW);}
}
