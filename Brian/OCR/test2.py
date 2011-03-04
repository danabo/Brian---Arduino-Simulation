from brian import *

# decreasing the time constant increases the rate of fire
tau = 10 * msecond        # membrane time constant
Vt = -50 * mvolt          # spike threshold
# voltage that the neuron is reset to
Vr = -60 * mvolt          # reset value

# if resting potential is lower than spike threshold, the neuron will never spike
El = -50 * mvolt          # resting potential (same as the reset)

G = NeuronGroup(N=1, model='dV/dt = -(V-El)/tau : volt',
              threshold=Vt, reset=Vr)

Mspike = SpikeMonitor(G)
M = StateMonitor(G, 'V', record=0)   # record 0th neuron's voltage

run(1 * second)

print Mspike.nspikes

##raster_plot(Mspike)
plot(M.times / ms, M[0] / mV)
xlabel('Time (in ms)')
ylabel('Membrane potential (in mV)')
title('Membrane potential for neuron 0')
show()