#!/usr/bin/env python
# -*- coding:utf-8 -*-

# db.py
'''
Database operation module.
'''

# note
# 1.__a 不允许外部访问变量(但还是有办法)
# 2._a  不推荐外部访问
# 3.__a__ 系统特殊变量 不在上面1.2.范围内 均可访问

import threading, uuid
import functools, logging, time

class Dict(dict):
    def __init__(self, names=(), values=(), **kw):
        super(Dict, self).__init__(**kw)
        for k, v in zip(names, values):
            self[k] = v

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'") % key

    def __setattr__(self, key, value):
        self[key] = value

def next_id(t=None):
    '''
    Return next id as 50-char string.

    Args:
        t: unix timestamp, default to None and using time.time().
    '''
    if t is None:
        t = time.time()
    return '%015d%s000' % (int(t * 1000), uuid.uuid4().hex)

def _profiling(start, sql=''):
    t = time.time() - start
    if t > 0.1:
        logging.warning('[PROFILING] [DB] %s: %s' % (t, sql))
    else:
        logging.info('[PROFILING] [DB] %s: %s' % (t, sql))

class DBError(Exception):
    pass

class MultiColumnsError(DBError):
    pass

# global engine object
engine = None

# 数据库引擎对象:
class _Engine(object):
    def __init__(self, connect):
        self._connect = connect
    def connect(self):
        return self._connect

# 持有数据库连接的上下文对象:
class _DbCtx(threading.local):
    """docstring for _DbCtx"""
    def __init__(self):
        self.connection = None
        self.transactions = 0

    def is_init(self):
        return not self.connection is None

    def init(self):
        logging.info('open lazy connection...')
        self.connection = _LasyConnection()
        self.transactions = 0

    def cleanup(self):
        self.connection.cleanup()
        self.connection = None

    def cursor(self):
        return self.connection.cursor()

_db_ctx = _DbCtx()

# 上下文管理器(先执行enter,然后程序,最后exit) 优化版try finally
# 自动获取和释放连接

class _ConnectionCtx(object):
    def __enter__(self):
        global _db_ctx
        self.should_cleanup = False
        if not _db_ctx.is_init():
            _db_ctx.is_init()
            self.should_cleanup = True
        return self

    def __exit__(self, exctype, excvalue, traceback):
        global _db_ctx
        if self.should_cleanup:
            _db_ctx.cleanup()

# API
def connection():
    '''
    Return _ConnectionCtx object that can be used by 'with' statement:

    with connection():
        pass
    '''
    return _ConnectionCtx()

def with_connection(func):
    '''
    Decorator for reuse connection.

    @with_connection
    def foo(*args, **kw):
        f1()
        f2()
        f3()
    '''
    @functools.wraps(func)
    def _wrapper(*args, **kw):
        # with 后面函数加()
        with _ConnectionCtx():
            return func(*args, **kw)
    return _wrapper

