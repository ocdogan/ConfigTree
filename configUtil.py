__author__ = 'Cagatay'

import datetime
import time
from dateutil import tz
from decimal import *
import types


def gettype(type_name):
    try:
        t = getattr(__builtins__, type_name)
        if isinstance(t, type):
            return t
    except Exception:
        pass
    glb = globals()
    print glb
    result = glb[type_name] if type_name in glb else None
    if result and isinstance(result, types.ClassType):
        return result
    return None

def add_timezone(dt):
    epoch_second = time.mktime(dt.timetuple())
    return datetime.datetime.utcfromtimestamp(epoch_second).replace(microsecond=dt.microsecond, tzinfo=tz.tzlocal())

def json_compatible(value):
    if isinstance(value, datetime.datetime) or isinstance(value, datetime.date):
        if not value.tzinfo:
            value = add_timezone(value)
        return value.isoformat(), True
    if isinstance(value, Decimal):
        return float(value), True
    return value, False

def to_json_value(obj):
    obj, converted = json_compatible(obj)
    if obj is None:
        return 'nil'
    if isinstance(obj, bool):
        return str(obj).lower()
    if isinstance(obj, (int, long, float)):
        return str(obj)
    return '"{0}"'.format(obj)

__id_by_type = {}

def next_id(object_type):
    object_type = object_type if object_type is not None else type(object)
    object_type = object_type if isinstance(object_type, type) else type(object_type)

    global __id_by_type
    current_id = 0
    key = object_type.__name__.lower()

    if key in __id_by_type:
        current_id = __id_by_type[key]
    current_id += 1
    __id_by_type[key] = current_id
    return '{0}@{1}'.format(key, current_id)

