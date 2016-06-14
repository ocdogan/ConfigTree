__author__ = 'Cagatay'

class Dynamic(dict):
	__setattr__= dict.__setitem__
	__delattr__= dict.__delitem__

	def __getattr__(self, key): 
		return self[key] if self.has_key(key) else None
		
	@staticmethod
	def dict_to_dynamic(d):
		return Dynamic(d)

