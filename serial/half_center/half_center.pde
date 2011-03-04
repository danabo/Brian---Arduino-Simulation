// double e = 2.718281828459045235360287471352662497757;

double tr = .003;
double tau = .001;
class Neuron { public:
  int nvars;
  int vars[2];
  double values[2];
  Neuron() {
     nvars = 2;
     vars[0]=(int)'v';
     vars[1]=(int)'k'; 
     values[0]=0;
     values[1]=0;
  }
  // t is timestep in seconds
  void tick(double t) {
    // dk/dt = -10*k/(1*second) : volt/volt
    // k
    values[1]+= t*(-10*values[1]);
    // dv/dt = (tr-v)/(1*k)/tau
    // v
    values[0]+= t*(tr-values[0])/values[1];
  }
  int get_index(int var) {
    for(int i=0; i<nvars; ++i) {
      if(vars[i]==var) {return i;} 
    }
    return -1;  // var does not exist
  }
  void set(int var, double value) {
     values[get_index(var)]=value;
  }
  double get(int var) {
     return values[get_index(var)]; 
  }
};
class NeuronGroup { public:
  Neuron * neurons;
  int nsize;
  int current; // the current neuron
  NeuronGroup(int n) : nsize(0), current(0) {
      neurons = (Neuron*)malloc(n*sizeof(Neuron));
      for(int i=0; i<n; ++i) {
        neurons[i]=Neuron();
      }
      nsize=n;
  }
  
  void tick(double t) {
     for(int i=0; i<nsize; ++i) {
        neurons[i].tick(t);
     } 
  }
  
  void set(int var, double value) {
    neurons[current].set(var,value);
  }
  double get(int var) {
    return neurons[current].get(var);
  }
};


float get_float() {
  int c=-1;
  char num[50]; // plenty of room
  int i=0;
  while(c!=0) {   // reads untill null char
    if(Serial.available() > 0) {
      c=Serial.read();
      num[i++]=(char)c;
    }
  }
  return atof(num);
}

// returns next serial byte 
// waits untill there is one
int next() {
  int b = -1;
  while(b<0) {
    b=Serial.read();
  }
  return b;
}

double timestep = .001;  // .1ms
int b=0;
int digits = 8;  // number of decimal digits in a float 
int var = 'v';
NeuronGroup G = NeuronGroup(2);



void setup() {
  Serial.begin(9600);
  pinMode(13, OUTPUT);  
  //Serial.println(G.get(118),8);
  // Serial.print(G.get(var),digits);
  // Serial.print('\0');
}



void loop() {
  if(Serial.available() > 0) {
    b = Serial.read();
      if(b==0x00) {
        // light off
        digitalWrite(13,LOW);
      }
      if(b==0x01) {
        // light on
        digitalWrite(13,HIGH);
      }
      if(b==0x05) {
        // get # decimal digits in a double
        // write 1 byte
        Serial.print(digits, BYTE);
      }
      if(b==0x10) {
        // set current variable
        // read 1 byte 
        var = next();
      }
      if(b==0x11) {
        // set current neuron
        // read 1 byte
        G.current = next();
      }
      if(b==0x12) {
        // get current var
        // write 1 byte
        Serial.print(var, BYTE); 
      }
      if(b==0x13) {
        // get current neuron
        // write 1 byte
        Serial.print(G.current, BYTE); 
      }
      if(b==0x20) {
        // set value
        // read untill '\0'
        G.set(var, get_float());
      }
      if(b==0x21) {
        // get value
        // write untill '\0'
        Serial.print(G.get(var),digits);
        Serial.print('\0');
      }
      if(b==0xf0) {
        // simulation tick
        G.tick(timestep);
      }
    
  }
}
