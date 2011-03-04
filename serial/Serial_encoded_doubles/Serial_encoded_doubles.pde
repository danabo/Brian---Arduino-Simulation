// send/recieve doubles as raw binary data
/*
on the python end:  (assume functions read(),write() goto arduino)
  from struct import pack,unpack
  f = SOME_FLOAT
  data = pack('f',f)
  arduino.write(data)
  data = arduino.read(4);   # size of float is 4
  f_times_10 = unpack('f',data)
*/

void setup() {
  Serial.begin(9600);
  Serial.print("size of double is ");
  Serial.println(sizeof(double));
  Serial.print("size of float is ");
  Serial.println(sizeof(float));
}

int double_size = sizeof(double);
byte* data = (byte*)malloc(double_size);
void loop() {
  if(Serial.available()>=double_size) {
    for(int i=0; i<double_size; ++i) {
      data[i] = Serial.read();
    }
    double* d = (double*)data;
    //Serial.println(*d);
    (*d)*=10;
    data = (byte*)d;
    for(int i=0; i<double_size; ++i) {
      Serial.write(data[i]);
    }
  }
}





