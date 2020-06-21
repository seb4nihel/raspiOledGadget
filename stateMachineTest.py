#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import time
import asyncio
from signal import *

def clean(*args):
    print("clean me")
    sys.exit(0)

for sig in (SIGABRT, SIGILL, SIGINT, SIGSEGV, SIGTERM):
    signal(sig, clean)

# State Machine using a Switch Case Workaround in Python
# Implement Python Switch Case Statement using Class
class StateMachine:

    async def switchState(self, state):
        default = "Not a valid State"
        return await getattr(self, 'state_' + state, lambda: default)()

    async def state_Init(self):
        print("State Machine now in State 'Init'")
        await asyncio.sleep(2)
        await self.switchState("1")
        print("State Machine automatically switching to State '1'")
 
    async def state_1(self):
        print("State Machine now in State '1'")
        await asyncio.sleep(2)
        await self.switchState("Init")
        print("State Machine automatically switching to State 'Init'")
 
s = StateMachine()
loop = asyncio.get_event_loop()
loop.run_until_complete(s.switchState("Init"))
