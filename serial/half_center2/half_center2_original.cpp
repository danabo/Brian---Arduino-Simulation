/*
 now handles spiking
*/
//%module half_center2

#include <stdlib.h>
//#include "half_center2.h"

double tr = .003;
double tau = .0008;
double v0 = .000; 
double k0 = 1.0;
double Wi = -250.0;
double timestep = .0001;
class Neuron { public:
  int nvars;
  int vars[2];
  double values[2];
  double threshold;
  bool spiking;
  Neuron() {
     nvars = 2;
     vars[0]=(int)'v';
     vars[1]=(int)'k'; 
     values[0]=v0;
     values[1]=k0;
     threshold = tr-.0001;
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
    values[0]+= t*(tr-values[0])/(.2*values[1])/tau;
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
      matrix = (double**)malloc(n*n*sizeof(double));
      for(int i=0; i<n; ++i) {
        neurons[i]=Neuron();
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
  double get(int var) {
    return neurons[current].get(var);
  }
};







NeuronGroup setup() {
 NeuronGroup G = NeuronGroup(2);
 G.matrix[0][1] = Wi;
 G.matrix[1][0] = Wi;
 G.neurons[0].values[0] = .0028;   //  neuron0.v = 2.8 mV 
 return G;
}
