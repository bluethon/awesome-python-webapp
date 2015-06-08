#!/usr/bin/env python
# coding=utf-8

import logging; logging.basicConfig(level=logging.INFO)

import asyncore, os, json, time
from datetime import datetime

from aiohttp import web

def index(request):
    return web.Respon(body=b'<h1>Awesome</h1>')
