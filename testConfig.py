application = None
print str(application).strip().lower() if application else ''

def lentern(text):
	l = len(text) if text else -1
	print l

lentern(application)

#from configObjects import *
#from configRoot import ConfigRoot
#from configNode import ConfigNode
from config import *
from datetime import datetime, date, time, tzinfo
from dateutil import tz

root = ConfigRoot('root', 1)
node1 = ConfigNode('node 1', 2) 
root.nodes.append(node1)
node1.attributes.set_attr('attr 1', 1, None)
node1.attributes.set_attr('attr 2', True, None)
node1.attributes.set_attr('attr 3', 1L, None)
node1.attributes.set_attr('attr 4', 1.3, None)
node1.attributes.set_attr('attr 5', datetime.now(), '', 'channel')

d = root.to_dict()

def printattrs(node):
	print '\n'
	print node.attributes.get_attr('attr 5')
	print node.attributes.get_attr('attr 5', 'application')
	print node.attributes.get_attr('attr 5', 'application', 'channel')
	print node.attributes.get_attr('attr 5', 'application', 'channel', 'client')
	print node.attributes.get_attr('attr 5', 'application', '', 'client')
	print node.attributes.get_attr('attr 5', '', 'channel', 'client')
	print node.attributes.get_attr('attr 5', '', '', 'client')
	print '\n'

#printattrs(node1)

#print d
#print '\n'
#print str(root) + '\n'

#n1 = root.find('/node 1')
#print n1

import json
from pprint import pprint
from dynamic import Dynamic

class ConfigJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime) or isinstance(obj, date):
            obj = str(obj)
        elif isinstance(obj, Decimal):
            obj = float(obj)
        else:
            obj = super(ConfigJSONEncoder, self).default(obj)
        print obj
        return obj

#j = json.dumps(d, cls=ConfigJSONEncoder)
print '\n'
print 'root.to_json()'
pprint(root.to_json())

print '\n'
print 'str(root)'
print str(root)

#obj=json.loads(str(root), object_hook=Dynamic.dict_to_dynamic)
#pprint(obj)

def copynode(node):
	import copy

	node_clone = copy.deepcopy(node)
	node_clone.reset_ids()
	print '\n'
	print 'str(node_clone)'
	print str(node_clone)
	print '\n'
	print 'str(node)'
	print str(node)
	
copynode(root)

from configConverter import from_dict, from_json

print '\n'
s = str(root)
r = from_json(s)
print 'from_json(s)'
print r
