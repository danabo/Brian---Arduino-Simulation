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
		
	def read_loop(self, n_bytes=1):
		s=""
		for byte in xrange(n_bytes):
			c=""
			while c=="":
				c=self.read(1)
			s+=c
		return s
		
	def read_wait(self, n_bytes=1):
		return self.read_loop(n_bytes)
		#self.timeout = None   # infinite timeout
		#data = self.read(n_bytes)
		#self.timeout = 0
		#return data
		
	def read_num(self):
		return eval(self.read_until('\x00'))
		
	def read_until(self, char='\x00'):
		## self.timeout=None   # infinite timeout
		s = ""
		c = ""
		while c!=char:
			c=self.read(1)
			s+=c
		## self.timeout = 0
		return s[:-1]   # remove the terminating byte
		
	def read_float(self):
		data = self.read_wait(4)
		return unpack('f',data)[0]
		
	def write_float(self, f):
		data = pack('f',f)
		self.write(data)
			
class HCO(Arduino):
	def __init__(self, *args):
		Arduino.__init__(self, *args)
		self.neuron = -1
		self.var = ''
		self.data = [{'v':list(), 'k':list()},{'v':list(), 'k':list()}]    # 2 neurons each with variables 'v' and 'k'
		##self.time = clock()
		##self.dtime = 0
		##self.last_dtime = 0
	def select(self, neuron=-1, var=-1):
		if neuron>=0 and neuron!=self.neuron:
			self.set_neuron(neuron)
			self.neuron=neuron
		if var!=-1 and var!=self.var:
			self.set_var(var)
			self.var=var
	def set_var(self, var):
		self.write('\x10'+var)
	def set_neuron(self,neuron_i):
		self.write('\x11'+chr(neuron_i))

	# sends a floating point f to the arduino which converts it to a system float and then converts and sends the data back
	def test_float(self, f):
		self.write('\x03')    # test float mode
		self.write_float(f)
		ff = self.read_float()
		print self.read_until('\n')
		return ff

	def get_value(self, neuron, var):
		self.select(neuron, var)
		self.write('\x21')
		#  uncomment to use older way of transfering floats
		## return self.read_num()
		return self.read_float()
		
	# depricated
	# reads floats assuming they are sent as ascii strings
	def get_value_v4(self, neuron, var):
		self.select(neuron, var)
		self.write('\x21')
		return self.read_num()
		
	def get_single_spike(self, neuron):
		self.select(neuron=neuron)
		self.write('\x22')
		n = ord(self.read_wait(1))
		if n==0:
			return 0
		return 1
	
	# returns a list of 0s and 1s
	def get_spikes(self):
		if self.inWaiting() > 0:
			raise RuntimeException("Extra data in buffer!  '"+ard.read()+"'")
		self.write('\x30')
		n = ord(self.read_wait(1))   # number of neurons
		# n must equal 2
		assert n==2, str(n)+"!=2"
		nbytes = ord(self.read_wait(1))
		assert nbytes==1, str(nbytes)+"!=1"
		bytes = self.read_wait(nbytes)
		"""
		spikes = [0]*n
		for i in range(n):
			if ord(bytes[i/8])&(1<<(i%8)):
				spikes[i] = 1
		"""
		spikes = [0,0]
		data = ord(bytes[0])
		spikes[0] = 1&data
		spikes[1] = 2&data
		return spikes
		
	def send_spike(self, neuron):
		self.write('\x31')
		self.write(chr(neuron))

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
		self.write(chr(self.consts[cvar]))
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
		
	# depricated
	# older version - no time is recorded
	def tick_v4(self):
		self.write('\xf0')
		
	def tick(self):
		##self.last_dtime = self.dtime
		t = self.get_tick_time()
		if self.inWaiting() > 0:
			raise RuntimeException("Extra data in buffer!  '"+self.read()+"'")
		self.write('\xf0')
		for neuron in range(2):
			for var in ('v','k'):
				self.data[neuron][var].append(0)   # add next timeframe to each
		if self.inWaiting() > 0:
			self.store_dump()
		return t
		
	def read_dump(self):
		# assume 2 neurons with the variables 'k' and 'v'
		data = []
		n_ticks = ord(self.read_wait(1))
		for tick in range(n_ticks):
			d = dict()
			data.append(d)
			for neuron in range(2):
				vars = dict()
				neuron_num = ord(self.read_wait(1))
				d[neuron_num]=vars
				for variable in range(2):
					# read 1 char variable name and then 4 byte float
					var = self.read_wait(1)
					f = self.read_float()
					vars[var]=f
		return data
		
	def store_dump(self):
		n_ticks = ord(self.read_wait(1))
		#overwrite the last n_ticks in self.data
		for tick in range(n_ticks):
			for neuron in range(2):
				neuron_num = ord(self.read_wait(1))
				for variable in range(2):
					# read 1 char variable name and then 4 byte float
					var = self.read_wait(1)
					f = self.read_float()
					self.data[neuron_num][var][-n_ticks+tick] = f
		
	
	
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