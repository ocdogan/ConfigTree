__author__ = 'Cagatay'

from StringIO import StringIO as StrIO
from copy import deepcopy, _deepcopy_dispatch
from types import ModuleType
from collections import OrderedDict
from configJSONEncoder import ConfigJSONEncoder
import configUtil
import json


class ConfigObject(object):
    __id_by_type = {}

    def __init__(self, object_id=None, *args, **kwargs):
        self.__object_id = abs(object_id) if object_id else configUtil.next_id(type(self))

    @property
    def object_id(self):
        return self.__object_id

    def __set_object_id(self, object_id):
        self.__object_id = object_id

    def reset_id(self):
        new_id = configUtil.next_id(type(self))
        self.__set_object_id(new_id)

    def reset_ids(self):
        self.reset_id()

    def __repr__(self):
        stringio = StrIO()
        stringio.write('{')
        self._write_repr_props(stringio)
        self._write_repr(stringio)
        stringio.write('}')
        return stringio.getvalue()

    def _write_repr_props(self, stringio):
        val = configUtil.to_json_value(type(self).__name__.lower())
        stringio.write('"__type__": {0}'.format(val))
        val = configUtil.to_json_value(self.__object_id)
        stringio.write(', "object_id": {0}'.format(val))
        return True

    def _write_repr(self, stringio):
        pass

    def to_dict(self):
        return {'__type__': type(self).__name__.lower(), 'object_id': self.__object_id} if self.__object_id else {}

    def find(self, path):
        return None

    def _can_copy_attr(self, attr_name):
        return True

    def _deepcopy_attrs_to(self, destination, memo):
        for k, v in self.__dict__.items():
            if self._can_copy_attr(k):
                setattr(destination, k, deepcopy(v, memo))

    def __deepcopy__(self, memo):
        objid = id(self)
        result = None
        if objid in memo:
            result = memo[objid]
        else:
            cls = self.__class__
            result = cls.__new__(cls)
            memo[objid] = result
            self._deepcopy_attrs_to(result, memo)
        return result

    def to_json(self):
        d = self.to_dict()
        od = OrderedDict(sorted(d.items(), key=lambda t: t[0]))
        return json.dumps(od, cls=ConfigJSONEncoder)

