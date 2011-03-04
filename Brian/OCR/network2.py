from brian import *
from random import random,seed
seed()

tau = 20 * msecond        # membrane time constant
Vt = -50 * mvolt          # spike threshold
Vr = -60 * mvolt          # reset value
El = -50 * mvolt          # resting potential (same as the reset)   # each neuron will spike once

N = 100+50+26

G = NeuronGroup(N=N, model='dV/dt = -(V-El)/tau : volt', threshold=Vt, reset=Vr)

Gin  = G.subgroup(100) # input neurons form 10x10 image
Gh   = G.subgroup(50)  # hidden layer
Gout = G.subgroup(26)  # output layer (one for each letter)

C1 = Connection(Gin, Gh)   # input layer to hidden layer  
C2 = Connection(Gh, Gout)  # hidden layer to output layer 

C1.connect_full(weight=lambda i,j:random()*mV) 
C2.connect_full(weight=lambda i,j:random()*mV) 

#G.V = Vr + rand(N) * (Vt - Vr)
input = [
0,0,0,0,1,1,0,0,0,0,
0,0,0,1,1,1,1,0,0,0,
0,0,1,1,0,0,1,1,0,0,
0,0,1,0,0,0,0,1,0,0,
0,0,1,0,0,0,0,1,0,0,
0,1,1,1,1,1,1,1,1,0,
0,1,0,0,0,0,0,0,1,0,
1,1,0,0,0,0,0,0,1,1,
1,0,0,0,0,0,0,0,0,1,
1,0,0,0,0,0,0,0,0,1
]
Gin.V  = Vr + array(input) * (Vt - Vr)
Gh.V   = array([Vr]*50)
Gout.V = array([Vr]*26)


class Tracker:
	def __init__(self):
		self.spiked = set([])
	# spikes is an array of neuron numbers
	def __call__(self,spikes):
		for neuron in spikes:
			self.spiked.add(neuron)
	def getSpiked(self):
		return list(self.spiked)
output_record = Tracker()

M = SpikeMonitor(G)
Min  = SpikeMonitor(Gin)
Mh   = SpikeMonitor(Gh)
Mout = SpikeMonitor(Gout,function = output_record)

run(30 * ms)

#print M.nspikes
print "output spike count: ",Mout.nspikes
print "output spiked neurons:  ",output_record.getSpiked()

#raster_plot(Min)
#raster_plot(Mh)
#raster_plot(Mout)
raster_plot(M)
show()
