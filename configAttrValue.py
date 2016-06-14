__author__ = 'Cagatay'

from StringIO import StringIO as StrIO
import datetime
import time
from decimal import *
from dateutil import tz
import configUtil


class ConfigAttrValue(object):
    def __init__(self, name, value, application='', channel='', client=''):
        self.__name = str(name).strip() if name else None
        self.__value = value
        self.__application = str(application).strip().lower() if application else ''
        self.__channel = str(channel).strip().lower() if channel else ''
        self.__client = str(client).strip().lower() if client else ''

    @property
    def name(self):
        return self.__name

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, data):
        self.__value = data

    @property
    def application(self):
        return self.__application

    @property
    def channel(self):
        return self.__channel

    @property
    def client(self):
        return self.__client

    def to_dict(self):
        kv_list = [(x.strip('_'), getattr(self, x)) for x in dir(self) if not x.startswith('_')]
        d = {}
        for k, v in kv_list:
            if v and v != '' and not hasattr(v, '__call__'):
                d[k] = v  # skip methods
        return d

    def __repr__(self):
        d = self.to_dict()
        if d and len(d) > 0:
            stringio = StrIO()
            stringio.write('{')
            is_first_attr = True
            items = sorted(d.iterkeys())
            for k in items:
                v = d[k]
                if v is not None:
                    text = '"{0}": {1}' if is_first_attr else ', "{0}": {1}'
                    is_first_attr = False
                    v = configUtil.to_json_value(v)
                    stringio.write(text.format(k, v))
            stringio.write('}')
            return stringio.getvalue()
        return ''

    def get_key(self):
        return '{0}.{1}.{2}.{3}'.format(self.__name,
                                        str(self.__application).strip().lower() if self.__application else '',
                                        str(self.__channel).strip().lower() if self.__channel else '',
                                        str(self.__client).strip().lower() if self.__client else '')


