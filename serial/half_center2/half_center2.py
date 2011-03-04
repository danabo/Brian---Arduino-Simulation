# This file was automatically generated by SWIG (http://www.swig.org).
# Version 1.3.40
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.
# This file is compatible with both classic and new-style classes.

from sys import version_info
if version_info >= (2,6,0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_half_center2', [dirname(__file__)])
        except ImportError:
            import _half_center2
            return _half_center2
        if fp is not None:
            try:
                _mod = imp.load_module('_half_center2', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _half_center2 = swig_import_helper()
    del swig_import_helper
else:
    import _half_center2
del version_info
try:
    _swig_property = property
except NameError:
    pass # Python < 2.2 doesn't have 'property'.
def _swig_setattr_nondynamic(self,class_type,name,value,static=1):
    if (name == "thisown"): return self.this.own(value)
    if (name == "this"):
        if type(value).__name__ == 'SwigPyObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name,None)
    if method: return method(self,value)
    if (not static) or hasattr(self,name):
        self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)

def _swig_setattr(self,class_type,name,value):
    return _swig_setattr_nondynamic(self,class_type,name,value,0)

def _swig_getattr(self,class_type,name):
    if (name == "thisown"): return self.this.own()
    method = class_type.__swig_getmethods__.get(name,None)
    if method: return method(self)
    raise AttributeError(name)

def _swig_repr(self):
    try: strthis = "proxy of " + self.this.__repr__()
    except: strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)

try:
    _object = object
    _newclass = 1
except AttributeError:
    class _object : pass
    _newclass = 0


class Neuron(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Neuron, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Neuron, name)
    __repr__ = _swig_repr
    __swig_setmethods__["nvars"] = _half_center2.Neuron_nvars_set
    __swig_getmethods__["nvars"] = _half_center2.Neuron_nvars_get
    if _newclass:nvars = _swig_property(_half_center2.Neuron_nvars_get, _half_center2.Neuron_nvars_set)
    __swig_setmethods__["vars"] = _half_center2.Neuron_vars_set
    __swig_getmethods__["vars"] = _half_center2.Neuron_vars_get
    if _newclass:vars = _swig_property(_half_center2.Neuron_vars_get, _half_center2.Neuron_vars_set)
    __swig_setmethods__["values"] = _half_center2.Neuron_values_set
    __swig_getmethods__["values"] = _half_center2.Neuron_values_get
    if _newclass:values = _swig_property(_half_center2.Neuron_values_get, _half_center2.Neuron_values_set)
    __swig_setmethods__["threshold"] = _half_center2.Neuron_threshold_set
    __swig_getmethods__["threshold"] = _half_center2.Neuron_threshold_get
    if _newclass:threshold = _swig_property(_half_center2.Neuron_threshold_get, _half_center2.Neuron_threshold_set)
    __swig_setmethods__["spiking"] = _half_center2.Neuron_spiking_set
    __swig_getmethods__["spiking"] = _half_center2.Neuron_spiking_get
    if _newclass:spiking = _swig_property(_half_center2.Neuron_spiking_get, _half_center2.Neuron_spiking_set)
    def __init__(self): 
        this = _half_center2.new_Neuron()
        try: self.this.append(this)
        except: self.this = this
    def onReset(self): return _half_center2.Neuron_onReset(self)
    def tick(self, *args): return _half_center2.Neuron_tick(self, *args)
    def get_index(self, *args): return _half_center2.Neuron_get_index(self, *args)
    def set(self, *args): return _half_center2.Neuron_set(self, *args)
    def get(self, *args): return _half_center2.Neuron_get(self, *args)
    __swig_destroy__ = _half_center2.delete_Neuron
    __del__ = lambda self : None;
Neuron_swigregister = _half_center2.Neuron_swigregister
Neuron_swigregister(Neuron)
cvar = _half_center2.cvar

class NeuronGroup(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, NeuronGroup, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, NeuronGroup, name)
    __repr__ = _swig_repr
    __swig_setmethods__["neurons"] = _half_center2.NeuronGroup_neurons_set
    __swig_getmethods__["neurons"] = _half_center2.NeuronGroup_neurons_get
    if _newclass:neurons = _swig_property(_half_center2.NeuronGroup_neurons_get, _half_center2.NeuronGroup_neurons_set)
    __swig_setmethods__["nsize"] = _half_center2.NeuronGroup_nsize_set
    __swig_getmethods__["nsize"] = _half_center2.NeuronGroup_nsize_get
    if _newclass:nsize = _swig_property(_half_center2.NeuronGroup_nsize_get, _half_center2.NeuronGroup_nsize_set)
    __swig_setmethods__["current"] = _half_center2.NeuronGroup_current_set
    __swig_getmethods__["current"] = _half_center2.NeuronGroup_current_get
    if _newclass:current = _swig_property(_half_center2.NeuronGroup_current_get, _half_center2.NeuronGroup_current_set)
    __swig_setmethods__["matrix"] = _half_center2.NeuronGroup_matrix_set
    __swig_getmethods__["matrix"] = _half_center2.NeuronGroup_matrix_get
    if _newclass:matrix = _swig_property(_half_center2.NeuronGroup_matrix_get, _half_center2.NeuronGroup_matrix_set)
    def __init__(self, *args): 
        this = _half_center2.new_NeuronGroup(*args)
        try: self.this.append(this)
        except: self.this = this
    def tick(self, *args): return _half_center2.NeuronGroup_tick(self, *args)
    def getCurrent(self): return _half_center2.NeuronGroup_getCurrent(self)
    def setCurrent(self, *args): return _half_center2.NeuronGroup_setCurrent(self, *args)
    def getNeuron(self, *args): return _half_center2.NeuronGroup_getNeuron(self, *args)
    def set(self, *args): return _half_center2.NeuronGroup_set(self, *args)
    def get(self, *args): return _half_center2.NeuronGroup_get(self, *args)
    __swig_destroy__ = _half_center2.delete_NeuronGroup
    __del__ = lambda self : None;
NeuronGroup_swigregister = _half_center2.NeuronGroup_swigregister
NeuronGroup_swigregister(NeuronGroup)


def setup():
  return _half_center2.setup()
setup = _half_center2.setup

