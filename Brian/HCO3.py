from brian import *

tau = .8*ms
tr = 3*mV
v0 = 0*mV
eqs = '''
dv/dt = (tr-v)/(.2*k)/tau : volt
dk/dt = -10*k/(1*second) : volt/volt
'''

reset = '''
k+=1
v=v0
'''

IF = NeuronGroup(2, model=eqs, reset=reset, threshold=tr-.1*mV)
IF.v=[v0,2.8*mV]
IF.k=[1,1]

C = Connection(IF, IF, 'v')
C[0,1]=C[1,0]=-250*mV
##Ck = Connection(IF, IF, 'k')
##Ck[0,1]=Ck[1,0]=-.6

sp1 = SpikeMonitor(IF[0])
sp2 = SpikeMonitor(IF[1])
Mv = StateMonitor(IF, 'v', record=True)
Mk = StateMonitor(IF, 'k', record=True)

## get_default_clock().dt = .1*ms
run(40 * ms)

subplot(411)
plot(Mv.times / ms, Mv[0] / mV)
plot(Mv.times / ms, Mk[0])
subplot(412)
raster_plot(sp1)
subplot(413)
plot(Mv.times / ms, Mv[1] / mV)
plot(Mv.times / ms, Mk[1])
subplot(414)
raster_plot(sp2)

show()