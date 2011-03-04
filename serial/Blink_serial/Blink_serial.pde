int b = 0;  // incomming byte
 
 

void setup() {                
  // initialize the digital pin as an output.
  // Pin 13 has an LED connected on most Arduino boards:
  pinMode(13, OUTPUT);  
  Serial.begin(9600);  
}

void loop() {
  if(Serial.available() > 0) {
    b = Serial.read();
    if(b>0) {digitalWrite(13,HIGH);}
    else {digitalWrite(13,LOW);}
  }
}
