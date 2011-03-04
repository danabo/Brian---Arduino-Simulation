from arduino import *
from brian import *
from time import sleep

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

IF = NeuronGroup(2, model=eqs, reset=reset, threshold=tr-.05*mV)

proxy_eqs = '''
dv/dt = 0*volt/second : volt
dk/dt = 0/second : volt/volt
'''
proxy = NeuronGroup(2, model=proxy_eqs, reset=reset, threshold=tr-.05*mV)   # proxy neurons for the arduino
IF.v=[2.8*mV,v0]
IF.k=[1,1]
proxy.v = [v0,v0]
proxy.k = [1 ,1 ]


C = Connection(IF, IF, 'v')
Cp = Connection(IF, proxy, 'v')   # proxy connection
Cpr = Connection(proxy, IF, 'v')  # reverse proxy connection
Wi = -100*mV
"""
(N1<->N2)<->(N3<->N4)
"""
C[0,1]=C[1,0]=Wi
Cp[1,0]=Cpr[0,1]=Wi


#sp1 = SpikeMonitor(IF[0])
#sp2 = SpikeMonitor(IF[1])
#sp3 = SpikeMonitor(IF[2])
#sp4 = SpikeMonitor(IF[3])
spIF = SpikeMonitor(IF)
spP = SpikeMonitor(proxy)
MvIF = StateMonitor(IF, 'v', record=True)
MvP = StateMonitor(proxy, 'v', record=True)
#Mk = StateMonitor(IF, 'k', record=True)

"""
get_default_clock().dt = 1*ms

ard = Arduino(3)  # com4
sleep(.5)
print "init arduino"
for neuron in range(2):
	for var in ('v','k'):
		set_value(ard, neuron, var, getattr(proxy[neuron],var))


@network_operation
def update_arduino():
	##ard.ToggleLight()
	for neuron in range(2):
		for var in ('v','k'):
			setattr(proxy[neuron],var, get_value(ard, neuron, var))
	arduino_tick(ard)
	#for neuron in range(2):
	#	for var in ('v','k'):
	#		setattr(proxy[neuron],var, get_value(ard, neuron, var))
"""
'''
clock  = get_default_clock()
clock.set_duration(100*ms)
print clock.get_duration()
clock.dt = .1*ms
for i in xrange(1000):   # 100ms
	clock.tick()
print clock.get_duration()
'''

refresh=10*ms
showlast=100*ms


times = MvIF.times / ms
ion()
subplot(411)
MvIF.plot(refresh=refresh, showlast=showlast)
plot(times, MvIF[0] / mV)
plot(times, MvIF[1] / mV)
subplot(412)
raster_plot(spIF, refresh=refresh, showlast=showlast)
subplot(413)
MvP.plot(refresh=refresh, showlast=showlast)
subplot(414)
raster_plot(spP, refresh=refresh, showlast=showlast)

run(100*ms)
ioff()

show()