#! /usr/bin/python3.6
# -*- coding: utf-8 -*-
#
# This demonstrates how to have a method get called when an I/O operation completes.
#
import asyncio
import sys


@asyncio.coroutine
def my_coroutine(future, task_name, seconds_to_sleep=3):
    print('{0} sleeping for: {1} seconds'.format(task_name, seconds_to_sleep))
    yield from asyncio.sleep(seconds_to_sleep)
    future.set_result('{0} is finished'.format(task_name))


@asyncio.coroutine
def terminal_reader(future):
    print("Waiting for terminal I/O")
    a_char = sys.stdin.read(1)
    yield from asyncio.


def got_result(future):
    print(future.result())


def got_a_char(future):
    print("Got a char: " + future.result())


loop = asyncio.get_event_loop()
future1 = asyncio.Future()
future2 = asyncio.Future()
future3 = asyncio.Future()

tasks = [
    my_coroutine(future1, 'task1', 3),
    my_coroutine(future2, 'task2', 1),
    terminal_reader(future=future3)]

future1.add_done_callback(got_result)
future2.add_done_callback(got_result)
future3.add_done_callback(got_a_char)

loop.run_until_complete(asyncio.wait(tasks))
loop.close()
