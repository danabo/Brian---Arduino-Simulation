from brian import *

# half center oscillator with adaptation

eqs = '''
dv/dt = (w+v)/(10*ms) : volt # the membrane equation
dw/dt = -w/(10*ms) : volt # the adaptation current
'''
# The adaptation variable increases with each spike
IF = NeuronGroup(2, model=eqs, threshold=20 * mV,
                 reset='''v  = 0*mV
                          w += 10*mV ''')

C = Connection(IF, IF, 'v')
C[0,1]=3 * mV
C[1,0]=3 * mV

Mv = StateMonitor(IF, 'v', record=True)
Mw = StateMonitor(IF, 'w', record=True)

IF.v = array([0,20])*mV

run(200 * ms)

plot(Mv.times / ms, Mv[0] / mV)
plot(Mw.times / ms, Mv[1] / mV)

show()