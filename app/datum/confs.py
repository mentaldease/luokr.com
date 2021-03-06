# -*- coding: UTF-8 -*-

import time
from lib.datum import Datum

class ConfsDatum(Datum):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.reload()

    def reload(self, datum = None):
        self._cache = {}
        if datum is not None:
            ret = datum.result('select conf_name, conf_vals from confs')
            if ret:
                for row in ret:
                    self._cache[row['conf_name']] = row['conf_vals']

    def obtain(self, name):
        if name not in self._cache:
            ret = self.record('select conf_vals from confs where conf_name = ?', (name, ))
            if ret:
                self._cache[name] = ret['conf_vals']
            else:
                self._cache[name] = None
        return self._cache[name]

    def exists(self, name):
        ret = self.record('select 1 from confs where conf_name = ?', (name, ))
        return bool(ret)

    def upsert(self, name, vals):
        self.submit('replace into confs (conf_name, conf_vals, conf_ctms) values (?, ?, ?)', (name, vals, int(time.time()),))
        self._cache[name] = vals

    def delete(self, name):
        self.submit('delete from confs where conf_name = ?', (name, ))
        self._cache[name] = None
