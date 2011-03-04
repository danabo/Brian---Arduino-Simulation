from brian import *

## uses equations from http://books.nips.cc/papers/files/nips23/NIPS2010_0425.pdf

mF = mfarad
Cm = 1*mF
tau = 10 * ms
A = 1
taue = 5 * ms
taui = 10 * ms
eqs = '''
dv/dt = ((ge+gi)*v+w*(1*mF))/(-Cm)/(1*ms) : volt
dw/dt = (w-A*v)/(-tau) : volt
dge/dt = -ge/taue : farad
dgi/dt = -gi/taui : farad
'''

vInit = 0*mV
B = 3*mV
reset = '''
v=vInit
w+=B
'''

IF = NeuronGroup(1, model=eqs, reset=reset, threshold='v>w')
IF.rest()
##PG = PoissonGroup(1, 100 * Hz)
E = 5*mV
sign = 1
#PG = NeuronGroup(1, model='dv/dt=(E-v)/(10*ms) : volt')
#PG.v = -B

#C = Connection(PG, IF, 'v', weight=B)

Mv = StateMonitor(IF, 'v', record=True)
Mvt = StateMonitor(IF, 'w', record=True)
#PGv = StateMonitor(PG, 'v', record=True)

run(10 * ms)
IF.v = B
#IF.gi = -5 * mF
run(100 * ms)
IF.v = 0 *mV
run(100 * ms)

plot(Mv.times / ms, Mv[0] / mV)
plot(Mvt.times / ms, Mvt[0] / mV)
#plot(Mvt.times / ms, PGv[0] / mV)

show()