

extern double tr;
extern double tau;
extern double v0; 
extern double k0;
extern double Wi;
extern double timestep;


class Neuron { public:
  int nvars;
  int vars[2];
  double values[2];
  double threshold;
  bool spiking;
  Neuron();
  void onReset();
  // t is timestep in seconds
  void tick(double t);
  int get_index(int var);
  void set(int var, double value);
  double get(int var);
};
class NeuronGroup { public:
  Neuron * neurons;
  int nsize;
  int current; // the current neuron
  double** matrix;  // the connection matrix of neurons with in this group
  NeuronGroup(int n);
  void tick(double t);
  Neuron& getCurrent();
  void setCurrent(int index);
  Neuron getNeuron(int index);
  void set(int var, double value);
  double get(int var);
};




extern NeuronGroup setup();
