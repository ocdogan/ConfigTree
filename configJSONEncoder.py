__author__ = 'Cagatay'

import json
import configUtil
from datetime import datetime, date, time, tzinfo


class ConfigJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        obj, converted = configUtil.json_compatible(obj)
        if not converted:
            obj = super(ConfigJSONEncoder, self).default(obj)
        return obj
