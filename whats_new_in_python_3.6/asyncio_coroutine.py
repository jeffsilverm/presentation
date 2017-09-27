#! /usr/bin/python3.6
# -*- coding: utf-8 -*-
#
# asyncio_coroutine.py
# From https://pymotw.com/3/asyncio/coroutines.html by Doug Hellmann 
import asyncio
<<<<<<< HEAD
=======
import sys

assert sys.version_info.major==3 and sys.version_info.minor >= 6,\
    "Running python version %s, must run at least 3.6 " % (sys.version_info )
>>>>>>> b4224fda9a436b71b2d8c3dac8e6b3ac00f8f0cb


async def coroutine():
    for i in [1,2,3,4]:
        print('in coroutine, i is {:d}'.format(i))


event_loop = asyncio.get_event_loop()
<<<<<<< HEAD
# event_loop is of type <class 'asyncio.unix_events._UnixSelectorEventLoop'>
try:
    print('starting coroutine')
    coro = coroutine()
# coro is of type <class 'coroutine'>
=======
try:
    print('starting coroutine')
    coro = coroutine()
>>>>>>> b4224fda9a436b71b2d8c3dac8e6b3ac00f8f0cb
    print('entering event loop')
    event_loop.run_until_complete(coro)
finally:
    print('closing event loop')
    event_loop.close()
<<<<<<< HEAD
=======

async def coroutine_y(n):
    for i in [1,2,3,4]:
        print('in coroutine {;d}, i is {:d}'.format(n, i))
        yield (i)

event_loop = asyncio.get_event_loop()
try:
    print('starting coroutine_y # 1')
    coro_1 = coroutine_y(1)
    print('starting coroutine_y # 1')
    coro_2 = coroutine_y(2)
    print('entering event loop')
    event_loop.run_until_complete(coro_1)
finally:
    print('closing event loop')
    event_loop.close()

>>>>>>> b4224fda9a436b71b2d8c3dac8e6b3ac00f8f0cb
