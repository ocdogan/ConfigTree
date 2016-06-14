__author__ = 'Cagatay'

import types
import json
from collections import deque, OrderedDict
from StringIO import StringIO as StrIO
from configObject import ConfigObject


class ConfigNodeBase(ConfigObject):
    class ConfigNodeList(object):
        def __init__(self, parent_node):
            self.__nodes = OrderedDict()
            self.__set_parent(parent_node)

        def __set_parent(self, node):
            self.__parent_node = node if isinstance(node, ConfigNodeBase) else None

        def append(self, node):
            if isinstance(node, ConfigNodeBase) and node.parent != self.__parent_node:
                if node.parent:
                    node.parent.nodes.remove(self)
                key = node.name
                if key in self.__nodes:
                    self.remove(self.__nodes[key])
                self.__nodes[key] = node
                node._set_parent(self.__parent_node)

        def remove(self, node):
            if isinstance(node, ConfigNodeBase) and node.parent == self.__parent_node:
                key = node.name
                if key in self.__nodes:
                    curr = self.__nodes[key]
                    if node == curr:
                        self.__nodes.pop(key, None)
                        node._set_parent(None)
                        return True
            return False

        def has_node(self):
            return len(self.__nodes) > 0

        def get_node(self, name=''):
            name = str(name).strip() if name else None
            if name and name in self.__nodes:
                return self.__nodes[name]
            return None

        @property
        def count(self):
            return len(self.__nodes)

        def __getitem__(self, key):
            return self.get_node(key)

        def __delitem__(self, key):
            if key in self.__nodes:
                node = self.__nodes[key]
                self.__nodes.pop(key, None)
                node._set_parent(None)

        def __contains__(self, item):
            if isinstance(item, ConfigNodeBase):
                if item.name in self.__nodes:
                    node = self.__nodes[item.name]
                    return node == item
            return False

        def __iter__(self):
            return self.__nodes.values().__iter__()

        def __reversed__(self):
            return self.__nodes.values().__reversed__()

        def __len__(self):
            return len(self.__nodes)

        def __repr__(self):
            if self.has_node():
                stringio = StrIO()
                index = 0
                count = len(self.__nodes)
                stringio.write('[')
                node_names = sorted(self.__nodes.iterkeys())
                for k in node_names:
                    v = self.__nodes[k]
                    index += 1
                    stringio.write(str(v))
                    if index < count:
                        stringio.write(', \r\n')
                stringio.write(']')
                return stringio.getvalue()
            return '[]'

        def to_list(self):
            return self.__nodes.values()

    def __init__(self, name='', object_id=None, *args, **kwargs):
        super(ConfigNodeBase, self).__init__(object_id=object_id, *args, **kwargs)
        self.__parent_node = None
        self.__name = str(name).strip() if name else None
        self._nodes = ConfigNodeBase.ConfigNodeList(self)

    @property
    def name(self):
        return self.__name

    def _set_name(self, name):
        self.__name = str(name).strip() if name else None

    def _set_parent(self, parent_node):
        self.__parent_node = parent_node

    def _write_repr_props(self, stringio):
        super(ConfigNodeBase, self)._write_repr_props(stringio)
        if self.__name:
            stringio.write(', "name": "{0}"'.format(self.__name))

    def _write_repr(self, stringio):
        super(ConfigNodeBase, self)._write_repr(stringio)
        if self._nodes.has_node():
            stringio.write(', \r\n"nodes": ')
            stringio.write(str(self._nodes))

    def to_dict(self):
        result = super(ConfigNodeBase, self).to_dict()
        if self.__name:
            result['name'] = self.__name
        if self._nodes.has_node():
            nodes = [node.to_dict() for node in self._nodes]
            result['nodes'] = nodes
        return result
 
    @property
    def parent(self):
        return self.__parent_node

    @property
    def nodes(self):
        return self._nodes

    def reset_ids(self):
        super(ConfigNodeBase, self).reset_ids()
        if self._nodes.has_node():
            for node in self._nodes:
                node.reset_ids()

    def find(self, path):
        result = None
        if path and isinstance(path, types.StringTypes):
            stack = deque()
            stack.append(self)
            parts = path.split('/')
            try:
                index = 0
                count = len(parts)
                for part in parts:
                    que_len = len(stack)
                    if que_len == 0:
                        break
                    index += 1
                    part = part.strip() if part else None
                    print part, index
                    if not part or part == '':
                        if index <= 1 or index == count:
                            continue
                        break
                    if part == '.':
                        pass
                    if part == '..':
                        stack.pop()
                    else:
                        curr = stack[que_len - 1]
                        if not curr:
                            break
                        node_part = curr._find_part(part)
                        if index == count:
                            result = node_part
                            break
                        if not isinstance(node_part, ConfigNodeBase):
                            break
                        stack.append(node_part)
            except Exception:
                pass
        return result

    def _find_part(self, part):
        return self._nodes.get_node(part)

