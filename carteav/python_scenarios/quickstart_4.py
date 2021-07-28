import lgsvl
from carteav.scenario import PythonScenario

class Scenario4(PythonScenario):
    def run(self):
        print("Python API Quickstart #4: Ego vehicle driving straight")
        super().run()



        if self.simulator.current_scene == lgsvl.wise.DefaultAssets.map_borregasave:
            self.simulator.reset()
        else:
            self.simulator.load(lgsvl.wise.DefaultAssets.map_borregasave)

        spawns = self.simulator.get_spawn()

        state = lgsvl.AgentState()
        state.transform = spawns[0]

        forward = lgsvl.utils.transform_to_forward(spawns[0])

        # Agents can be spawned with a velocity. Default is to spawn with 0 velocity
        state.velocity = 20 * forward
        ego = self.simulator.add_agent(self.env.str("LGSVL__VEHICLE_0", lgsvl.wise.DefaultAssets.ego_lincoln2017mkz_apollo5),
                            lgsvl.AgentType.EGO, state)

        # The bounding box of an agent are 2 points (min and max) such that the box formed from those 2 points completely encases the agent
        print("Vehicle bounding box =", ego.bounding_box)

        print("Current time = ", self.simulator.current_time)
        print("Current frame = ", self.simulator.current_frame)

        input("Press Enter to drive forward for 2 seconds")

        # The simulator can be run for a set amount of time. time_limit is optional and if omitted or set to 0, then the simulator will run indefinitely
        self.simulator.run(time_limit=2.0)

        print("Current time = ", self.simulator.current_time)
        print("Current frame = ", self.simulator.current_frame)

        self.simulator.reset()

        state = lgsvl.AgentState()
        state.transform = spawns[0]

        forward = lgsvl.utils.transform_to_forward(spawns[0])

        # Agents can be spawned with a velocity. Default is to spawn with 0 velocity
        state.velocity = 20 * forward

        ego = self.simulator.add_agent(self.env.str("LGSVL__VEHICLE_0", lgsvl.wise.DefaultAssets.ego_lincoln2017mkz_apollo5),
                            lgsvl.AgentType.EGO, state)

        input("Press Enter to continue driving for 2 seconds")

        self.simulator.run(time_limit=2.0)

        print("Current time = ", self.simulator.current_time)
        print("Current frame = ", self.simulator.current_frame)

def setup(batcher):
    Scenario4(batcher.sim, __file__).setup(batcher)