from brian import *

tau = 20 * msecond        # membrane time constant
Vt = -50 * mvolt          # spike threshold
Vr = -60 * mvolt          # reset value
El = -49 * mvolt          # resting potential (same as the reset)
psp = 0.5 * mvolt         # postsynaptic potential size

G = NeuronGroup(N=176, model='dV/dt = -(V-El)/tau : volt',
              threshold=Vt, reset=Vr)
			  
Gin  = G.subgroup(100) # input neurons form 10x10 image
Gh   = G.subgroup(50)  # hidden layer
Gout = G.subgroup(26)  # output layer (one for each letter)

C1 = Connection(Gin, Gh)
C2 = Connection(Gh, Gout)
#C1.connect_random(sparseness=0.1, weight=psp)
#C2.connect_random(sparseness=0.1, weight=psp)
C1.connect_full(weight=.5*mV) 
C2.connect_full(weight=.5*mV)

M = SpikeMonitor(G)

G.V = Vr + rand(176) * (Vt - Vr)

run(100*ms)

print M.nspikes

raster_plot()
show()