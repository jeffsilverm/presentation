#! /usr/bin/python3.6
# -*- coding: utf-8 -*-
#
# asyncio_coroutine.py
# From https://pymotw.com/3/asyncio/coroutines.html by Doug Hellmann 
import asyncio


async def coroutine():
    for i in [1,2,3,4]:
        print('in coroutine, i is {:d}'.format(i))


event_loop = asyncio.get_event_loop()
# event_loop is of type <class 'asyncio.unix_events._UnixSelectorEventLoop'>
try:
    print('starting coroutine')
    coro = coroutine()
# coro is of type <class 'coroutine'>
    print('entering event loop')
    event_loop.run_until_complete(coro)
finally:
    print('closing event loop')
    event_loop.close()
