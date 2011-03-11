## use half_center5.pde

from arduino import *
ard = HCO(4, 28800)  # com5, baud 512000
##ard = HCO(4, 9600)  # com5, baud 512000

from brian import *
from time import sleep,clock
import sys
clock()


class Timer:
	def __init__(self):
		self.t0=0
		self.runs = 0
		self.avg = 0
	def start(self):
		self.t0=clock()
	# add an externally measured time interal to the average
	def include(self, dt):
		n=self.runs
		self.avg = self.avg*(float(n)/(n+1.0))+dt/(n+1.0)
		self.runs+=1
	def stop(self):
		dt = clock()-self.t0
		self.t0=0
		self.include(dt)
	def results(self):
		return self.avg
			

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

tau = 1*ms
tr = 3*mV
threshold = tr-.5*mV;
v0 = 0*mV
v1 = 2.8*mV
timespan = 100*ms
eqs = '''
dv/dt = (tr-v)/(1*k)/tau : volt
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
IF.v=[v1,v0]
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


##sleep(2)
ard.Light(1)
ard.needs_version(5)
print "init arduino"
##print "junk:  "+ard.read(100)
# init neurons
for neuron in range(2):
	for var in ('v','k'):
		ard.set_value(neuron, var, getattr(proxy[neuron],var))
# init constants
ard.set_const('tau', float(tau))
ard.set_const('tr', float(tr))
ard.set_const('Wi', float(Wi))
ard.set_const('timestep', float(default_clock.dt))
ard.set_threshold(float(threshold))

##print "junk:  "+ard.read(100)
# extra byte not present yet

P = PercentDisplay(timespan, default_clock.dt)
communication_time = Timer()
calculation_time = Timer()    # arduino
step_time = Timer()

arduino_spike_list = [[],[]]

@network_operation(when='before_groups')
def update_arduino():
	##ard.ToggleLight()
	##print "junk:  "+ard.read(100)   # extra byte present now
	step_time.start()
	
	for neuron in range(2):
		for var in ('v','k'):
			communication_time.start()
			value = ard.get_value(neuron, var)
			communication_time.stop()
			setattr(proxy[neuron],var, value*volt)
	spikes = ard.get_spikes()
	arduino_spike_list[0].append(spikes[0])
	arduino_spike_list[1].append(spikes[1])
	# FIX!  for some reason theres an extra 'k' or '?' on the first tick
	##stuff = ard.read(1)  # see if theres extra junk  
	##if stuff: print stuff 
	dt = ard.tick()
	calculation_time.include(dt/1000000.0)  # convert to seconds
	P.update()
	#for neuron in range(2):
	#	for var in ('v','k'):
	#		setattr(proxy[neuron],var, get_value(ard, neuron, var))
	
	step_time.stop()
	
	
	
def IF_spike(spikes):
	for neuron in spikes:
		for prxy in range(2):
			dv = float(Cp[neuron,prxy])    # should be in volts
			if dv!=0:
				#ard.send_spike(prxy)
				ard.inc_value(prxy, 'v', dv)

				
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
run(timespan)
ard.Light(0)
print "simulation complete!"

print "average communication time = "+str(communication_time.results())+" seconds"
print "average arduino calculation time = "+str(calculation_time.results())+" seconds"
print "average simulation step time = "+str(step_time.results())+" seconds"

times = MvIF.times / ms
subplot(611)
plot(times, MvIF[0] / mV)
plot(times, MvIF[1] / mV)
subplot(612)
##raster_plot(spIF, ymargin=.5)
raster_plot(spIF1)
raster_plot(spIF2)
subplot(613)
plot(times, MvP[0] / mV)
plot(times, MvP[1] / mV)
subplot(614)
##raster_plot(spP, ymargin=.5)
raster_plot(spP1)
raster_plot(spP2)
subplot(615)
sc = scatter(times, arduino_spike_list[0], 1)
ax = sc.axes
ax.set_xbound(0, timespan/ms)
subplot(616)
sc = scatter(times, arduino_spike_list[1], 1)
ax = sc.axes
ax.set_xbound(0, timespan/ms)

show()