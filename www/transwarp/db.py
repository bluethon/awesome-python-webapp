#!/usr/bin/env python
# -*- coding:utf8 -*-
# db.py

# note
# 1.__a 不允许外部访问变量(但还是有办法)
# 2._a  不推荐外部访问
# 3.__a__ 系统特殊变量 不在上面1.2.范围内 均可访问
import threading

# 数据库引擎对象:
class _Engine(object):
    def __init__(self, connect):
        self._connect = connect
    def connect(self):
        return self._connect

engine = None

# 持有数据库连接的上下文对象:
class _DbCtx(threading.local):
    """docstring for _DbCtx"""
    def __init__(self):
        self.connection = None
        self.transactions = 0

    def is_init(self):
        return not self.connection is None

    def init(self):
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
    return _ConnectionCtx()
