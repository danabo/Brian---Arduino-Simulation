from brian import *

tau = 1*ms
tr = 5*mV
v0 = 0*mV
eqs = '''
dv/dt = (tr-v)/tau : volt
'''

reset = '''
v0-=3*mV
v=v0
'''

IF = NeuronGroup(1, model=eqs, reset=reset, threshold=tr-.1*mV)
IF.v=v0

Mv = StateMonitor(IF, 'v', record=True)

run(800 * ms)

plot(Mv.times / ms, Mv[0] / mV)

show()