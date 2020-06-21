#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import time
from signal import *

def clean(*args):
    print("clean me")
    sys.exit(0)

for sig in (SIGABRT, SIGILL, SIGINT, SIGSEGV, SIGTERM):
    signal(sig, clean)

# State Machine using a Switch Case Workaround in Python
# Implement Python Switch Case Statement using Class
class StateMachine:

    def switchState(self, state):
        default = "Not a valid State"
        return getattr(self, 'state_' + state, lambda: default)()

    def state_Init(self):
        print("State Machine now in State 'Init'")
        time.sleep(2)
        self.switchState("1")
        print("State Machine automatically switching to State '1'")
 
    def state_1(self):
        print("State Machine now in State '1'")
        time.sleep(2)
        self.switchState("Init")
        print("State Machine automatically switching to State 'Init'")
 

s = StateMachine()
s.switchState("Init")