# test the arduino half-centre oscillator code
# simulates half center oscillator on the arduino and graphs it with matlibplot
# use half_center5.pde

from arduino import *
from matplotlib.pyplot import *
import numpy as np
import sys
from time import sleep


VERSION = 5
COM = 5

if VERSION<5:
	ard = HCO(COM-1, 9600)
else:
	ard = HCO(COM-1, 28800)
sleep(2)
print "init arduino"
ard.Light(1)    # turn light on
if VERSION>=5:
	ard.needs_version(VERSION)
vars = [{'v':[], 'k':[], 'spike':[]},{'v':[], 'k':[], 'spike':[]}]
timestep = .0001
dt = .0001
timespan = .03
times = np.arange(0., timespan, dt)
#sleep(5)
print "simulation start.."

percent = 0;
current_time = 0.0;
def display_percent(p):
	if p==100:
		sys.stdout.write("\b"*5)
	else:
		sys.stdout.write("\b"*5+str(p)[:4]+"%")

def update_arduino():
	global vars,percent,current_time
	for neuron in range(2):
		for var in ('v','k'):
			if VERSION<5:
				vars[neuron][var].append(ard.get_value_v4(neuron, var))
			else:
				vars[neuron][var].append(ard.get_value(neuron, var))
		vars[neuron]['spike'].append(ard.get_single_spike(neuron))
	#s1,s2 = ard.get_spikes()
	#vars[0]['spike'].append(s1)
	#vars[1]['spike'].append(s2)
		
	for i in xrange(int(dt/timestep)):
		if VERSION<5:
			ard.tick_v4()
		else:
			ard.tick()
		current_time+=timestep
	perc = int(current_time*100/timespan)
	if perc-percent>=1:
		display_percent(perc)
		percent=perc

def frange(start, stop, step):
    r = start
    while r < stop:
            yield r
            r += step

def run(timespan):
	##for i in frange(0,timespan, dt):
	for i in times:
		update_arduino()
	display_percent(100)
		
def dump(fname):
	f = open(fname, 'w')
	f.write('times:\n')
	for i in xrange(len(times)):
		f.write(str(i)+":\t"+str(times[i])+"\n")
	for neuron in range(2):
		f.write("\nneuron #"+str(neuron)+"\n")
		for var in ('v','k'):
			f.write("\nvar '"+var+"'\n")
			for i in xrange(len(vars[neuron][var])):
				f.write(str(i)+':\t'+str(vars[neuron][var][i])+'\n')
	f.close()

run(timespan)

print "simulation complete!"
ard.Light(0)

try:
	subplot(411)
	plot(times, vars[0]['v'])
	plot(times, vars[0]['k'])
	subplot(412)
	sc = scatter(times, vars[0]['spike'], 1)
	ax = sc.axes
	ax.set_xbound(0, timespan)
	subplot(413)
	plot(times, vars[1]['v'])
	plot(times, vars[1]['k'])
	subplot(414)
	sc = scatter(times, vars[1]['spike'], 1)
	ax = sc.axes
	ax.set_xbound(0, timespan)
	show()
except:
	dump("could_not_plot.log")
	raise

'''
times = MvIF.times / ms
subplot(411)
plot(times, MvIF[0] / mV)
plot(times, MvIF[1] / mV)
subplot(412)
raster_plot(spIF)
subplot(413)
plot(times, MvP[0] / mV)
plot(times, MvP[1] / mV)
subplot(414)
raster_plot(spP)
'''

