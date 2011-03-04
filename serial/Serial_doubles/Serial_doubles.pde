
void setup() {
  Serial.begin(9600);
}

char term = 'T';
char num[100]; // plenty of room
int i=0;
int last=0;
void loop() {
  if(Serial.available()>0) {
    last=i;
    num[i++] = Serial.read();
    if(i==100) {i=0;}
    
  }
  if(num[last]==term) {
    num[last]='\0';
    double f = atof(num);
    Serial.println(f,16);
    i=0;
    last=0;
  }
}
