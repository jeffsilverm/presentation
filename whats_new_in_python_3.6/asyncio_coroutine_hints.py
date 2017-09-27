#! /usr/bin/python3.6
# -*- coding: utf-8 -*-
#
# asyncio_coroutine_hints.py
# From https://pymotw.com/3/asyncio/coroutines.html by Doug Hellmann
# but also showing how type annotations would work.

from typing import Coroutine
import asyncio


async def coroutine() -> Coroutine:
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
