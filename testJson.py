__author__ = 'Cagatay'

import json
from dynamic import Dynamic
from pprint import pprint

txt='''
{
  "maps":[
    {"id": "blabla", "iscategorical": 0},
    {"id": "blabla", "iscategorical": 0.7}
    ],
  "masks": {"id": "valore"},
  "om_points": "value",
  "parameters": {"id": "valore"}
}
'''

obj=json.loads(txt, object_hook=Dynamic.dict_to_dynamic)
pprint(obj)
