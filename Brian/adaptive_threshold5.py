from brian import *

tau = 1*ms
tr = 5*mV
v0 = 0*mV
eqs = '''
dv/dt = (tr-v)/(4*k)/tau : volt
dk/dt = -4*k/(1*second) : volt/volt
'''

reset = '''
k+=1
v=v0
'''

IF = NeuronGroup(1, model=eqs, reset=reset, threshold=tr-.1*mV)
IF.v=v0
IF.k=1

Mv = StateMonitor(IF, 'v', record=True)
Mk = StateMonitor(IF, 'k', record=True)

run(500 * ms)
print IF.k

plot(Mv.times / ms, Mv[0] / mV)
plot(Mv.times / ms, Mk[0])

show()