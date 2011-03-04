from brian import *

tau = 1*ms
tr = 3*mV
v0 = 0*mV
eqs = '''
dv/dt = (tr-v)/(2*k)/tau : volt
dk/dt = -8*k/(1*second) : volt/volt
'''

reset = '''
k+=1
v=v0
'''

IF = NeuronGroup(2, model=eqs, reset=reset, threshold=tr-.1*mV)
IF.v=[v0,2*mV]
IF.k=[1,5]

C = Connection(IF, IF, 'k')
C[0,1]=C[1,0]=2
##C[0,0]=C[1,1]=0

Mv = StateMonitor(IF, 'v', record=True)
Mk = StateMonitor(IF, 'k', record=True)

run(1000 * ms)

subplot(211)
plot(Mv.times / ms, Mv[0] / mV)
plot(Mv.times / ms, Mk[0])
subplot(212)
plot(Mv.times / ms, Mv[1] / mV)
plot(Mv.times / ms, Mk[1])

show()