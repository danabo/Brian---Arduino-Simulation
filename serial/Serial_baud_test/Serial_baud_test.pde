#define BUFF_SIZE 256

/*
bauds that work
9600
14400
19200
28800
*/
int baud = 9600;
unsigned long t = 0;
unsigned long dt = 0;
byte buffer[BUFF_SIZE];

void setup() {
  Serial.begin(baud);
  Serial.print("baud rate ");
  Serial.println(baud);
  
  for(int i = 0; i < BUFF_SIZE; ++i) {
    buffer[i] = (byte)i;    // assume overflow, so really buffer[i] = i%256;
  }
}



void loop() {
  if(Serial.available() > 0) {
    Serial.read();
    t = micros();
    Serial.write(buffer,BUFF_SIZE);
    dt = micros()-t;
    Serial.println("");
    Serial.print(dt);
    Serial.println(" us");
  }
}
