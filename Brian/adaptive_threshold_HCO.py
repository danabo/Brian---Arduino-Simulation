from brian import *

eqs = '''
dv/dt = (10*mV)/(1*ms) : volt
dvt/dt = (10*mV-vt)/(15*ms) : volt
'''

reset = '''
v=0*mV
vt+=3*mV
'''

IF = NeuronGroup(2, model=eqs, reset=reset, threshold='v>vt')
##IF.rest()
#PG = PoissonGroup(1, 500 * Hz)
#C = Connection(PG, IF, 'v', weight=-.05 * mV)
#C = Connection(PG, IF, 've', weight=1 * mV)


C = Connection(IF, IF, 'v')
weight = -.9*mV
C[0,1]=weight
C[1,0]=weight


IF.v = array([0,10])*mV
#IF.v = 0*mV
IF.vt = 10*mV
##IF.ve = 0*mV

Mv = StateMonitor(IF, 'v', record=True)
Mvt = StateMonitor(IF, 'vt', record=True)

run(100 * ms)
##Mv.plot()
##Mvt.plot()
plot(Mv.times / ms, Mv[0] / mV)
plot(Mv.times / ms, Mv[1] / mV)
#plot(Mvt.times / ms, Mvt[0] / mV)

show()