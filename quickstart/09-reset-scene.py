#!/usr/bin/env python3
#
# Copyright (c) 2019 LG Electronics, Inc.
#
# This software contains code licensed as described in LICENSE.
#

import os
import lgsvl
import random
import time
import math

random.seed(0)

sim = lgsvl.Simulator(os.environ.get("SIMULATOR_HOST", "127.0.0.1"), 8181)
if sim.current_scene == "BorregasAve":
  sim.reset()
else:
  sim.load("BorregasAve")

spawns = sim.get_spawn()

state = lgsvl.AgentState()
state.transform = spawns[0]
a = sim.add_agent("Lincoln2017MKZ (Apollo 5.0)", lgsvl.AgentType.EGO, state)

# 10 meters ahead
sx = state.transform.position.x
sz = state.transform.position.z + 10.0

for i, name in enumerate(["Sedan", "SUV", "Jeep", "Hatchback"]):
  state = lgsvl.AgentState()
  state.transform = spawns[0]

  state.transform.position.x = sx - 4.0 * i
  state.transform.position.z = sz
  sim.add_agent(name, lgsvl.AgentType.NPC, state)

input("Press Enter to reset")

# Reset will remove any spawned vehicles and set the weather back to default, but will keep the scene loaded
sim.reset()
