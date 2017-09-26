#! /usr/bin/python3.6
# -*- coding: utf-8 -*-
#
# asyncio_coroutine_hints.py
# From https://pymotw.com/3/asyncio/coroutines.html by Doug Hellmann
# but also showing how type annotations would work.

from typing import Coroutine
# from typing import Awaitable
import typing.Awaitable
import asyncio


async def coroutine() -> Coroutine :
    for i in [1,2,3,4]:
        print('in coroutine, i is {:d}'.format(i))


event_loop = asyncio.get_event_loop()   # type: asyncio.events.AbstractEventLoop
# According to type(event_loop), event_loop is of type
# <class 'asyncio.unix_events._UnixSelectorEventLoop'>
# TYPE: class asyncio.unix_events._UnixSelectorEventLoop
# The following is from http://mypy.readthedocs.io/en/latest/cheat_sheet_py3.html
# To find out what type mypy infers for an expression anywhere in
# your program, wrap it in reveal_type.  Mypy will print an error
# message with the type; remove it again before running or compiling the code.
# reveal_type(event_loop) # -> error: Revealed type is 'builtins.int'

try:
    print('starting coroutine')
    coro = coroutine()  # type: typing.Awaitable[typing.Coroutine[Any, Any, Any]]
# type(coro) says coro is of type <class 'coroutine'>
#    reveal_type(coro)
# When I run mypy, it throws the following messages:
# asyncio_coroutine_hints.py:10: error: No library stub file for standard library module 'typing.Awaitable'
# asyncio_coroutine_hints.py:10: note: (Stub files are from https://github.com/python/typeshed)
# asyncio_coroutine_hints.py:31: error: Name 'Any' is not defined
# The problem is that the appropriate stub file for the asyncio module hasn't been written yet.

    print('entering event loop')
    event_loop.run_until_complete(coro)
finally:
    print('closing event loop')
    event_loop.close()
