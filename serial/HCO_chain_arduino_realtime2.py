## use half_center4.pde

from arduino import *
from brian import *
from time import sleep
import sys

class PercentDisplay:
	def __init__(self, timespan, dt):
		self.percent = 0
		self.current_time = 0.0
		self.dt = float(dt)
		self.timespan = float(timespan)
	def update(self):
		self.current_time+=self.dt
		p = int(self.current_time*100.0/self.timespan)
		if p-self.percent>=1 or p>=100:
			self.display(p)
			self.percent=p
	def display(self, p):
		if p==100:
			sys.stdout.write("\b"*5)
		else:
			sys.stdout.write("\b"*5+str(p)[:4]+"%")

tau = .8*ms
tr = 3*mV
threshold = tr-.5*mV;
v0 = 0*mV
timespan = 250*ms
eqs = '''
dv/dt = (tr-v)/(0.2*k)/tau : volt
dk/dt = -10*k/(1*second) : volt/volt
'''

reset = '''
k+=2
v=v0
'''

IF = NeuronGroup(2, model=eqs, reset=reset, threshold=threshold)

proxy_eqs = '''
dv/dt = 0*volt/second : volt
dk/dt = 0/second : volt/volt
'''
proxy = NeuronGroup(2, model=proxy_eqs, reset=reset, threshold=threshold)   # proxy neurons for the arduino
IF.v=[2.8*mV,v0]
IF.k=[1,1]
proxy.v = [v0,v0]
proxy.k = [1 ,1 ]


C = Connection(IF, IF, 'v')
Cp = Connection(IF, proxy, 'v')   # proxy connection
Cpr = Connection(proxy, IF, 'v')  # reverse proxy connection
Wi = -250*mV
"""
(N1<->N2)<->(N3<->N4)
"""
C[0,1]=C[1,0]=Wi
Cp[1,0]=Cpr[0,1]=Wi


default_clock = get_default_clock()
## get_default_clock().dt = 1*ms

ard = Arduino(3)  # com4
sleep(.5)
print "init arduino"
# init neurons
for neuron in range(2):
	for var in ('v','k'):
		set_value(ard, neuron, var, getattr(proxy[neuron],var))
# init constants
set_const(ard, 'tau', float(tau))
set_const(ard, 'tr', float(tr))
set_const(ard, 'Wi', float(Wi))
set_const(ard, 'timestep', float(default_clock.dt))
set_threshold(ard, float(threshold))

P = PercentDisplay(timespan, default_clock.dt)

@network_operation(when='before_groups')
def update_arduino():
	##ard.ToggleLight()
	for neuron in range(2):
		for var in ('v','k'):
			setattr(proxy[neuron],var, get_value(ard, neuron, var)*volt)
	arduino_tick(ard)
	P.update()
	#for neuron in range(2):
	#	for var in ('v','k'):
	#		setattr(proxy[neuron],var, get_value(ard, neuron, var))
	
	
	
def IF_spike(spikes):
	for neuron in spikes:
		for prxy in range(2):
			dv = float(Cp[neuron,prxy])    # should be in volts
			if dv!=0:
				inc_value(ard, prxy, 'v', dv)

				
SpikeMonitor(IF, function = IF_spike)
spIF1 = SpikeMonitor(IF[0]) #, function = IF_spike)
spIF2 = SpikeMonitor(IF[1]) #, function = IF_spike)
## spIF = SpikeMonitor(IF, function = IF_spike)
spP1 = SpikeMonitor(proxy[0])
spP2 = SpikeMonitor(proxy[1])
## spP = SpikeMonitor(proxy)
MvIF = StateMonitor(IF, 'v', record=True)
MvP = StateMonitor(proxy, 'v', record=True)
#Mk = StateMonitor(IF, 'k', record=True)

'''
clock  = get_default_clock()
clock.set_duration(100*ms)
print clock.get_duration()
clock.dt = .1*ms
for i in xrange(1000):   # 100ms
	clock.tick()
print clock.get_duration()
'''

refresh=1*ms
showlast=200*ms
##showlast=timespan

times = MvIF.times / ms
ion()
subplot(411)
MvIF.plot(refresh=refresh, showlast=showlast)
subplot(412)
##raster_plot(spIF, ymargin=.5)
raster_plot(spIF1, refresh=refresh, showlast=showlast)
raster_plot(spIF2, refresh=refresh, showlast=showlast)
subplot(413)
MvP.plot(refresh=refresh, showlast=showlast)
subplot(414)
##raster_plot(spP, ymargin=.5)
raster_plot(spP1, refresh=refresh, showlast=showlast)
raster_plot(spP2, refresh=refresh, showlast=showlast)




run(timespan)
print "simulation complete!"
ioff()

show()