__author__ = 'Cagatay'

from copy import copy, deepcopy

class A(object):
	def __init__(self, obj_id, *args, **kwargs):
		self.__obj_id = obj_id
	
	def __repr__(self):
		return type(self).__name__ + ':' + str(self.__obj_id)

	@property
	def obj_id(self):
		return self.__obj_id

	@obj_id.setter
	def obj_id(self, value):
		self.__obj_id = value

class B(A):
	def __init__(self, obj_id, name, *args, **kwargs):
		super(B, self).__init__(obj_id, *args, **kwargs)
		self.__name = name

	@property
	def name(self):
		return self.__name

	@name.setter
	def name(self, value):
		self.__name = value

	def __repr__(self):
		result = super(B, self).__repr__()
		return result + ', name:' + str(self.__name)

class C(A):
	def __init__(self, obj_id, color, *args, **kwargs):
		super(C, self).__init__(obj_id=obj_id, *args, **kwargs)
		self.__color = color

	@property
	def color(self):
		return self.__color

	@color.setter
	def color(self, value):
		self.__color = value

	def __repr__(self):
		result = super(C, self).__repr__()
		return result + ', color:' + str(self.__color)

class D(B, C):
	def __init__(self, obj_id, name, color, status, *args, **kwargs):
		super(D, self).__init__(obj_id=obj_id, name=name, color=color, *args, **kwargs)
		self.__status = status

	@property
	def status(self):
		return self.__status

	@status.setter
	def status(self, value):
		self.__status = value

	def __repr__(self):
		result = super(D, self).__repr__()
		return result + ', status:' + str(self.__status)
		
	def __copy__(self):
		print 'copy'
		return type(self)(self.__obj_id, self.__name, self.__color, self.__status)
		
	def __deepcopy__(self, memo):
		cls = self.__class__
		result = cls.__new__(cls)
		memo[id(self)] = result
		for k, v in self.__dict__.items():
			setattr(result, k, deepcopy(v, memo))
		setattr(result, 'obj_id', -self.obj_id)
		return result

a1 = A(1)
print a1

b = B(2, 'b1')
print b

c = C(3, 'red')
print c

d1 = D(4, 'd1', 'blue', 'dirty')
print d1

d2 = type(d1)(-4, 'd1', 'blue', 'dirty')
print d2

d2 = deepcopy(d1)
#d2.obj_id=5
print d2
print d1
