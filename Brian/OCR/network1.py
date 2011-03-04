from brian import *
from random import random,seed
seed()

tau = 20 * msecond        # membrane time constant
Vt = -50 * mvolt          # spike threshold
Vr = -60 * mvolt          # reset value
El = -49 * mvolt          # resting potential (same as the reset)

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
arr = array([1,0,0,0,0,0,0,0,0,0]*10)
Gin.V  = Vr + arr * (Vt - Vr)
Gh.V   = array([Vr]*50)
Gout.V = array([Vr]*26)


M = SpikeMonitor(G)
Min  = SpikeMonitor(Gin)
Mh   = SpikeMonitor(Gh)
Mout = SpikeMonitor(Gout)

run(50 * ms)

#print M.nspikes
print "output spike count: ",Mout.nspikes

#raster_plot(Min)
#raster_plot(Mh)
#raster_plot(Mout)
raster_plot(M)
show()
