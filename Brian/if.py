from brian import *

tau = 10 * ms
Vr = -70 * mV
Vt = -55 * mV

G = NeuronGroup(1, model='V:volt', threshold=Vt, reset=Vr)

input = SpikeGeneratorGroup(1, [(0, t * ms) for t in linspace(10, 100, 25)])

C = Connection(input, G)
C[0, 0] = 2 * mV

M = StateMonitor(G, 'V', record=True)

G.V = Vr
run(100 * ms)
plot(M.times / ms, M[0] / mV)
show()