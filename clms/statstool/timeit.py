"""timeit decorator"""
# -*- coding: utf-8 -*-
import time
from logging import getLogger


def timeit(method):
    """ decorator to print the time that takes a method to execute"""
    def timed(*args, **kw):
        """ modified function"""
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        log = getLogger(__name__)
        log.info(
            "%r (%r, %r) %2.2f sec", method.__name__, args, kw, te - ts
        )
        return result

    return timed
