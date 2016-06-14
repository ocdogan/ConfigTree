__author__ = 'Cagatay'

import json
import types
from configNode import ConfigNode
from configRoot import ConfigRoot


def __get_object_id(d):
    object_id = None
    if d and isinstance(d, dict):
        object_id = d.get('object_id', None)
        if object_id:
            try:
                object_id = int(object_id)
            except Exception:
                try:
                    object_id = float(object_id)
                except Exception:
                    pass
    return object_id

def from_dict(d):
    if d and isinstance(d, dict):
        type_name = d.get('__type__', 'confignode').lower()
        object_id = __get_object_id(d)
        name = d.get('name', '') # d['name'] if 'name' in d else ''
        try:
            if type_name == 'configroot':
                inst = ConfigRoot(name=name, object_id=object_id)
            else:
                inst = ConfigNode(name=name, object_id=object_id)
        except Exception:
            pass
        for k, v in d.iteritems():
            if k == 'nodes':
                for node in [from_dict(n) for n in v]:
                    if node:
                        inst.nodes.append(node)
            elif k == 'attributes' and isinstance(inst, ConfigNode):
                for a in v:
                    name = a.get('name', None)
                    value = a.get('value', None)
                    application = a.get('application', '')
                    channel = a.get('channel', '')
                    client = a.get('client', '')
                    inst.attributes.set_attr(name=name, value=value, application=application, channel=channel, client=client)
            elif k not in ('object_id', '__type__') and hasattr(inst, k):
                try:
                    setattr(inst, k, v)
                except Exception:
                    pass
        return inst
    return None

def from_json(text_data):
    if text_data and isinstance(text_data, types.StringTypes):
        d = json.loads(text_data)
        return from_dict(d)
    return None
