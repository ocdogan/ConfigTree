__author__ = 'Cagatay'

import types
from StringIO import StringIO as StrIO
from configNodeBase import ConfigNodeBase
from configAttrList import ConfigAttrList


class ConfigNode(ConfigNodeBase):
    def __init__(self, name='', object_id=None, *args, **kwargs):
        super(ConfigNode, self).__init__(name=name, object_id=object_id, *args, **kwargs)
        self._attributes = ConfigAttrList()

    @property
    def attributes(self):
        return self._attributes

    def to_dict(self):
        result = super(ConfigNode, self).to_dict()
        if self._attributes.has_attr():
            attrs = [attr.to_dict() for attr in self._attributes]
            result['attributes'] = attrs
        return result

    def _write_repr(self, stringio):
        if self._attributes.has_attr():
            stringio.write(', \r\n"attributes": ')
            stringio.write(str(self._attributes))
        super(ConfigNode, self)._write_repr(stringio)

    def _find_part(self, part):
        result = self._nodes.get_node(part)
        if not result and isinstance(part, types.StringTypes) \
                and part.startswith('[') and part.endswith(']') \
                and len(part) > 2:
            attr = part[1:len(part) - 1]
            attr = attr.strip() if attr else None
            if attr:
                attr_parts = attr.split(',')
                attr_len = len(attr_parts)
                name = attr_parts[0] if attr_len > 0 else None
                application = attr_parts[1] if attr_len > 1 else None
                channel = attr_parts[2] if attr_len > 2 else None
                client = attr_parts[3] if attr_len > 3 else None
                result = self._attributes.get_attr(name, application, channel, client)
        return result

