from brian import *

tau = 10 * ms
taue = 5 * ms
Vr = -70 * mV
Vt = -55 * mV

#leaky (exponential) IF model
##G = NeuronGroup(2, model='dV/dt = -(V-Vr)/tau : volt', threshold=Vt, reset=Vr)

#linear IF model
eqs = Equations('''
	dV/dt = -(Vr)/tau-ge/taue : volt
	dge/dt = -ge/tau  : volt
	''')
G = NeuronGroup(2, model=eqs, threshold=Vt, reset=Vr)

##spikes = linspace(10 * ms, 100 * ms, 25)
##input = MultipleSpikeGeneratorGroup([spikes])

# bi connect 1 to 2
C = Connection(G, G, 'ge')
C[0, 1] = 5 * mV
C[1, 0] = 5 * mV

M = StateMonitor(G, 'V', record=True)

G.V = array([Vr, Vt])
run(100 * ms)
plot(M.times / ms, M[0] / mV)
plot(M.times / ms, M[1] / mV)
show()