/*
 handles spiking
 constants can be changed
 version number accessable
 timer for speed watching
*/

double tr = .003;
double tau = .0008;
double v0 = .000; 
double v1 = .0028;
double k0 = 1.0;
double Wi = -.2500;
double timestep = .0001;
double spike_threshold = tr-.0005;
class Neuron { public:
  int nvars;
  int vars[2];
  double values[2];
  double threshold;
  boolean spiking;
  Neuron() {
     nvars = 2;
     vars[0]=(int)'v';
     vars[1]=(int)'k'; 
     values[0]=v0;
     values[1]=k0;
     threshold = spike_threshold;
     spiking = false;
  }
  void onReset() {
    // called when the neuron spikes
    values[1]+=1;   // k++
    values[0]=v0;   // v=v0
  }
  // t is timestep in seconds
  void tick(double t) {
    if(spiking) {onReset(); spiking=false;}  // spike only lasts one tick
    // dk/dt = -10*k/(1*second) : volt/volt
    // k
    values[1]+= t*(-10*values[1]);
    // dv/dt = (tr-v)/(.2*k)/tau
    // v
    values[0]+= t*(tr-values[0])/(1*values[1])/tau;
    if(values[0]>=threshold) {
      spiking=true;
    }
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
  void inc(int var, double value) {
    values[get_index(var)]+=value;
  }
  double get(int var) {
     return values[get_index(var)]; 
  }
};
class NeuronGroup { public:
  Neuron * neurons;
  int nsize;
  int current; // the current neuron
  double** matrix;  // the connection matrix of neurons with in this group
  NeuronGroup(int n) : nsize(0), current(0) {
      neurons = (Neuron*)malloc(n*sizeof(Neuron));
      matrix = (double**)malloc(n*sizeof(double*));
      for(int i=0; i<n; ++i) {
        neurons[i]=Neuron();
        matrix[i] = (double*)malloc(n*sizeof(double));
        for(int j=0; j<n; ++j) {
           matrix[i][j] = 0.0;  // initialize matrix with no connections 
        }
      }
      nsize=n;
  }
  
  void tick(double t) {
     for(int i=0; i<nsize; ++i) {
        neurons[i].tick(t);
        if(neurons[i].spiking) {
          for(int j=0; j<nsize; ++j) {
            neurons[j].values[0] += matrix[i][j];   // V_j += W_ij
          }
        }
     } 
  }
  Neuron& getCurrent() {
    return neurons[current];
  }
  void set(int var, double value) {
    neurons[current].set(var,value);
  }
  void inc(int var, double value) {
    neurons[current].inc(var,value);
  }
  double get(int var) {
    return neurons[current].get(var);
  }
};

/*
// reads float as a string
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
*/

// returns next serial byte 
// waits untill there is one
int next() {
  int b = -1;
  while(b<0) {
    b=Serial.read();
  }
  return b;
}

// reads binary float data
int float_size=sizeof(float);  // this should be 4
byte* data = (byte*)malloc(float_size);
float get_float() {
  for(int i=0; i<float_size; ++i) {
    data[i] = (byte)next();   // read bytes
  }
  return *((float*)data);  // cast to float pointer and then de-reference
}

void send_float(float f) {
  byte* data = (byte*)(&f);  // convert reference to f into a byte array
  for(int i=0; i<float_size; ++i) {
    Serial.write(data[i]);  // write bytes
  }
}


// doubles are the same size as floats
double get_double() {
  return (double)get_float();
}


int b=0;
int digits = 8;  // number of decimal digits in a float 
int var = 'v';
NeuronGroup G = NeuronGroup(2);

unsigned long time;
unsigned long dtime;   // change in time for the last simulation tick


void setup() {
  Serial.begin(28800);
  pinMode(13, OUTPUT); 
 G.matrix[0][1] = Wi;
 G.matrix[1][0] = Wi;
 G.neurons[0].values[0] = v1;   //  G[0].v = v1 volts
 time=micros();
 dtime=0;
}



void loop() {
  if(Serial.available() > 0) {
    b = Serial.read();
      if(b==0x00) {
        // light off
        digitalWrite(13,LOW);
      }
      else if(b==0x01) {
        // light on
        digitalWrite(13,HIGH);
      }
      else if(b==0x02) {
        // ask for version number
        // send string: "arduinoHCO5\0"  (version 5)
        Serial.print("arduinoHCO5");
        Serial.print('\0');
      }
      else if(b==0x03) {
        // test floating point transfer over serial
        // read 4 byte float, write the same 4 byte float
        // print string version of float with newline
        float f = get_float();
        send_float(f);
        Serial.println(f,10);
      }
      else if(b==0x05) {
        // get # decimal digits in a double
        // write 1 byte
        Serial.print(digits, BYTE);
      }
      else if(b==0x10) {
        // set current variable
        // read 1 byte 
        var = next();
      }
      else if(b==0x11) {
        // set current neuron
        // read 1 byte
        G.current = next();
      }
      else if(b==0x12) {
        // get current var
        // write 1 byte
        Serial.print(var, BYTE); 
      }
      else if(b==0x13) {
        // get current neuron
        // write 1 byte
        Serial.print(G.current, BYTE); 
      }
      else if(b==0x20) {
        // set value
        // read 4 byte float
        G.set(var, get_float());
      }
      else if(b==0x21) {
        // get value
        // write 4 byte float
        send_float(G.get(var));
        // Serial.print(G.get(var),digits);
        // Serial.print('\0');
      }
      else if(b==0x22) {
        // get spike status
        // write 255 or 0
        Serial.print(G.getCurrent().spiking,BYTE);
      }
      else if(b==0x23) {
        // incriment value
        // read 4 byte float
        G.inc(var, get_float());
      }
      else if(b==0xe0) {
        // set constant
        // read ID (1 byte) then read untill '\0'
        b = next();
        /*
        double tr       : 0x01
        double tau      : 0x02
        double v0       : 0x03 
        double v1       : 0x04
        double k0       : 0x05
        double Wi       : 0x06
        double timestep : 0x07
        */
             if(b==0x01) {tr = get_double();}
        else if(b==0x02) {tau= get_double();}
        else if(b==0x03) {v0 = get_double();}
        else if(b==0x04) {v1 = get_double();}
        else if(b==0x05) {k0 = get_double();}
        else if(b==0x06) {Wi = get_double();}
        else if(b==0x07) {timestep = get_double();}
      }
      else if(b==0xe1) {
        // update neuron spike thresholds
        // read 4 byte float
        double newthreshold = get_double();
        for(int  i=0; i<G.nsize; ++i) {
          G.neurons[i].threshold = newthreshold;
        }
      }
      else if(b==0xf0) {
        // simulation tick
        time = micros();
        G.tick(timestep);
        dtime = micros()-time;
      }
      else if(b==0xf5) {
        // get run time for last simulation tick in microseconds
        // write string int untill '\0'
        Serial.print(dtime);
        Serial.print('\0');
      }
    
  }
}
