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

IF = NeuronGroup(4, model=eqs, reset=reset, threshold=tr-.1*mV)
IF.v=[v0,v0,v0,2.8*mV]
IF.k=[1,1,1,1]

C = Connection(IF, IF, 'v')
cm =   [[0,2,1,1],
		[1,0,2,1],
		[1,1,0,2],
		[2,1,1,0]]
Wi = -50*mV
for i in range(4):
	for j in range(4):
		C[i,j] = cm[i][j]*Wi


#sp = SpikeMonitor(IF)
sp = [SpikeMonitor(IF[0]),
	SpikeMonitor(IF[1]),
	SpikeMonitor(IF[2]),
	SpikeMonitor(IF[3]) ]
Mv = StateMonitor(IF, 'v', record=True)
#Mk = StateMonitor(IF, 'k', record=True)

run(500 * ms)

times = Mv.times / ms
subplot(411)
plot(times, Mv[0] / mV)
plot(times, Mv[1] / mV)
subplot(412)
##raster_plot(spIF, ymargin=.5)
raster_plot(sp[0])
raster_plot(sp[1])
subplot(413)
plot(times, Mv[2] / mV)
plot(times, Mv[3] / mV)
subplot(414)
##raster_plot(spP, ymargin=.5)
raster_plot(sp[2])
raster_plot(sp[3])
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