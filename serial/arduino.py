import serial
from struct import pack,unpack
##from time import clock
##clock()   # windows needs an initial call

class Arduino(serial.Serial):
	def __init__(self, *args):
		serial.Serial.__init__(self, *args)
		self.timeout = 0   # no timeout
		
		self.lightstate = 0
	def Light(self, on=1):
		self.write(chr(on))
		self.lightstate = on
	def ToggleLight(self):
		self.lightstate = 1-self.lightstate
		self.write(chr(self.lightstate))
			
class HCO(Arduino):
	def __init__(self, *args):
		Arduino.__init__(self, *args)
		self.neuron = -1
		self.var = ''
		##self.time = clock()
		##self.dtime = 0
		##self.last_dtime = 0
	def select(self, neuron, var):
		if neuron!=self.neuron:
			self.set_neuron(neuron)
			self.neuron=neuron
		if var!=self.var:
			self.set_var(var)
			self.var=var
	def set_var(self, var):
		self.write('\x10'+var)
	def set_neuron(self,neuron_i):
		self.write('\x11'+chr(neuron_i))
	def read_float(self):
		data = self.read_bytes(4)
		return unpack('f',data)[0]
	def write_float(self, f):
		data = pack('f',f)
		self.write(data)
	# sends a floating point f to the arduino which converts it to a system float and then converts and sends the data back
	def test_float(self, f):
		self.write('\x03')    # test float mode
		self.write_float(f)
		ff = self.read_float()
		print self.read_until('\n')
		return ff
	def read_num(self):
		return eval(self.read_until('\x00'))
	def read_until(self, char='\x00'):
		s = ""
		c = ""
		while c!=char:
			c=self.read(1)
			s+=c
		return s[:-1]   # remove the terminating byte
	def read_bytes(self, n_bytes):
		s = ""
		c = ""
		n=0
		while n<n_bytes:
			c=self.read(1)
			if c!="":
				s+=c
				n+=1
		return s
	def get_value(self, neuron, var):
		self.select(neuron, var)
		self.write('\x21')
		## return self.read_num()
		return self.read_float()

	def set_value(self, neuron, var, value):
		self.select(neuron, var)
		##self.write('\x20'+str(value)+'\x00')
		self.write('\x20')
		self.write_float(value)
		
	def inc_value(self, neuron, var, value):
		self.select(neuron, var)
		## self.write('\x23'+str(value)+'\x00')
		self.write('\x23')
		self.write_float(value)
		
	consts = {'tr' : 0x01,
			  'tau': 0x02,
			  'v0' : 0x03,
			  'v1' : 0x04,
			  'k0' : 0x05,
			  'Wi' : 0x06,
			  'timestep' : 0x07}
	def set_const(self, cvar, value):
		## self.write('\xe0'+chr(consts[cvar])+str(value)+'\x00')
		self.write('\xe0')
		self.write_float(value)
	def set_threshold(self, value):
		## self.write('\xe1'+str(value)+'\x00')
		self.write('\xe1')
		self.write_float(value)
	def send_receive(self, out_bytes, nbytes_in=1):
		self.write(out_bytes)
		s = ""
		for i in xrange(nbytes_in):
			c = ""
			while c=="":
				c = self.read(1)
			s+=c
		return s
		
	def needs_version(self, n, exact=False):
		# if exact is true this function will only accept version numbers equal to n
		# if exact is false this function will accept version numbers greater than or equal to n
		self.write('\x02')   # get version info
		v = self.read_until('\0')
		# the version string looks like this 'arduinoHCO(n)'  where (n) is the version number
		hco = 'arduinoHCO'
		if v[:len(hco)]!=hco:
			raise RuntimeError("The arduino does not have the proper half-centered oscillator sketch loaded!")
		version_num = eval(v[len(hco):])
		if (exact and version_num!=n) or (not(exact) and version_num<n):
			raise RuntimeError("This sketch is version "+str(version_num)+" which is an older version than "+str(n))
		
	def get_tick_time(self):
		self.write('\xf5')
		return self.read_num()
		
	def tick(self):
		##self.last_dtime = self.dtime
		t = self.get_tick_time()
		self.write('\xf0')
		return t
		
	
	
# functions for half centered oscillator
def simvar(ard, neuron, var):
	ard.write('\x10'+var+'\x11'+chr(neuron))
def get_value(ard, neuron, var):
	simvar(ard, neuron, var)
	ard.write('\x21')
	s = ""
	c = ""
	while c!='\x00':
		c=ard.read(1)
		s+=c
	return float(s[:-1])

def set_value(ard, neuron, var, value):
	simvar(ard, neuron, var)
	ard.write('\x20'+str(value)+'\x00')
	
def inc_value(ard, neuron, var, value):
	simvar(ard, neuron, var)
	ard.write('\x23'+str(value)+'\x00')
	
consts = {'tr' : 0x01,
		  'tau': 0x02,
		  'v0' : 0x03,
		  'v1' : 0x04,
		  'k0' : 0x05,
		  'Wi' : 0x06,
		  'timestep' : 0x07}
def set_const(ard, cvar, value):
	ard.write('\xe0'+chr(consts[cvar])+str(value)+'\x00')
def set_threshold(ard, value):
	ard.write('\xe1'+str(value)+'\x00')
	
def send_receive(ard, out_bytes, nbytes_in=1):
	ard.write(out_bytes)
	s = ""
	for i in xrange(nbytes_in):
		c = ""
		while c=="":
			c = ard.read(1)
		s+=c
	return s
	
def arduino_tick(ard):
	ard.write('\xf0')