__author__ = 'Cagatay'

from configNodeBase import ConfigNodeBase


class ConfigRoot(ConfigNodeBase):
    def __init__(self, name='', object_id=None, *args, **kwargs):
        super(ConfigRoot, self).__init__(name=name, object_id=object_id, *args, **kwargs)
        self.__cloned_id = None

    @property
    def cloned_id(self):
        return self.__cloned_id

    def _write_repr(self, stringio):
        if self.__cloned_id:
            stringio.write(', \r\n"cloned_id": ')
            stringio.write('"' + str(self.__cloned_id) + '"')
        super(ConfigRoot, self)._write_repr(stringio)

    def _deepcopy_attrs_to(self, destination, memo):
        super(ConfigRoot, self)._deepcopy_attrs_to(destination, memo)
        destination.__cloned_id = self.object_id
