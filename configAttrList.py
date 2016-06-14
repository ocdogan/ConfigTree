__author__ = 'Cagatay'

import types
from StringIO import StringIO as StrIO
from configAttrValue import ConfigAttrValue
from collections import OrderedDict


class ConfigAttrList(object):
    def __init__(self):
        self.__items = {}

    @staticmethod
    def __get_attr_id(name, application='', channel='', client=''):
        return '{0}.{1}.{2}.{3}'.format(name,
                                        str(application).strip().lower() if application else '',
                                        str(channel).strip().lower() if channel else '',
                                        str(client).strip().lower() if client else '')

    def __get_attr_ids(self, name, application='', channel='', client=''):
        ids = OrderedDict()
        
        attr_id = ConfigAttrList.__get_attr_id(name, application, channel, client)
        ids[attr_id] = attr_id in self.__items
        
        attr_id = ConfigAttrList.__get_attr_id(name, application, channel, '')
        ids[attr_id] = attr_id in self.__items
        
        attr_id = ConfigAttrList.__get_attr_id(name, application, '', client)
        ids[attr_id] = attr_id in self.__items
        
        attr_id = ConfigAttrList.__get_attr_id(name, application, '', '')
        ids[attr_id] = attr_id in self.__items
        
        attr_id = ConfigAttrList.__get_attr_id(name, '', channel, client)
        ids[attr_id] = attr_id in self.__items
        
        attr_id = ConfigAttrList.__get_attr_id(name, '', channel, '')
        ids[attr_id] = attr_id in self.__items
        
        attr_id = ConfigAttrList.__get_attr_id(name, '', '', client)
        ids[attr_id] = attr_id in self.__items
        
        attr_id = ConfigAttrList.__get_attr_id(name, '', '', '')
        ids[attr_id] = attr_id in self.__items
        
        return ids

    def get_attr(self, name, application='', channel='', client=''):
        ids = self.__get_attr_ids(name, application, channel, client)
        for attr_id, exists in ids.iteritems():
            if exists:
                return True, self.__items[attr_id]
        return False, None

    def get_attr_value(self, name, application='', channel='', client=''):
        found, value = self.get_attr(name, application='', channel='', client='')
        return value.value if found and value else None

    def set_attr(self, name, value, application='', channel='', client=''):
        found, attr = self.get_attr(name, application, channel, client)
        if found and attr:
            attr.value = value
        else:
            attr = ConfigAttrValue(name, value, application, channel, client)
            self.__items[attr.get_key()] = attr

    def has_attr(self):
        return len(self.__items) > 0

    @property
    def count(self):
        return len(self.__items)

    def __iter__(self):
        return self.__items.values().__iter__()

    def __reversed__(self):
        return self.__items.values().__reversed__()

    def __len__(self):
        return len(self.__items)

    def remove(self, name, application='', channel='', client=''):
        attr_id = ConfigAttrList.__get_attr_id(name, application, channel, client)
        if attr_id in self.__items:
            self.__items.pop(attr_id, None)
            return True
        return False

    def removeall(self, name, application='', channel='', client=''):
        ids = self.__get_attr_ids(name, application, channel, client)
        for attr_id, exists in ids:
            if exists:
                self.__items.pop(attr_id)

    def clear(self):
        self.__items.clear()

    def __repr__(self):
        if self.has_attr():
            stringio = StrIO()
            index = 0
            count = len(self.__items)
            attr_names = sorted(self.__items.iterkeys())
            stringio.write('[')
            for k in attr_names:
                v = self.__items[k]
                index += 1
                stringio.write(str(v))
                if index < count:
                   stringio.write(', \r\n')
            stringio.write(']')
            return stringio.getvalue()
        return ''

    def to_list(self):
        return self.__items.values()

