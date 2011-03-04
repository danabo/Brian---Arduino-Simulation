from brian import *

tau = 1*ms
tr = 3*mV
v0 = 0*mV
eqs = '''
dv/dt = (tr-v)/(1*k)/tau : volt
dk/dt = -10*k/(1*second) : volt/volt
'''

reset = '''
k+=2
v=v0
'''

IF = NeuronGroup(4, model=eqs, reset=reset, threshold=tr-.05*mV)
IF.v=[v0,v0,v0,2.8*mV]
IF.k=[1,1,1,1]

C = Connection(IF, IF, 'v')
C[0,1]=C[1,0]=C[1,2]=C[2,1]=C[2,3]=C[3,2]=-100*mV
##Ck = Connection(IF, IF, 'k')
##Ck[0,1]=Ck[1,0]=-.6

sp1 = SpikeMonitor(IF[0])
sp2 = SpikeMonitor(IF[1])
sp3 = SpikeMonitor(IF[2])
sp4 = SpikeMonitor(IF[3])
#sp = SpikeMonitor(IF)
Mv = StateMonitor(IF, 'v', record=True)
#Mk = StateMonitor(IF, 'k', record=True)

run(250 * ms)


times = Mv.times / ms
subplot(411)
plot(times, Mv[0] / mV)
plot(times, Mv[1] / mV)
subplot(412)
##raster_plot(spIF, ymargin=.5)
raster_plot(sp1)
raster_plot(sp2)
subplot(413)
plot(times, Mv[2] / mV)
plot(times, Mv[3] / mV)
subplot(414)
##raster_plot(spP, ymargin=.5)
raster_plot(sp3)
raster_plot(sp4)

"""
subplot(211)
plot(Mv.times / ms, Mv[0] / mV)
plot(Mv.times / ms, Mv[1] / mV)
plot(Mv.times / ms, Mv[2] / mV)
plot(Mv.times / ms, Mv[3] / mV)
subplot(212)
raster_plot(sp)
"""


show()