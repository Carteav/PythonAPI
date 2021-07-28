from enum import Enum
import lgsvl
from lgsvl.utils import accepts
import json
import time

class ScenarioType(Enum):
    Python = 1
    Json = 2


class CarteavScenario:
    @accepts(lgsvl.simulator.Simulator, str)
    def __init__(self, simulator, path):
        self.simulator = simulator
        self.path = path


class PythonScenario(CarteavScenario):
    @accepts(lgsvl.simulator.Simulator, str)
    def __init__(self, simulator, path):
        super().__init__(simulator, path)
        self.type = ScenarioType.Python
        self.runtime = 5

    def run(self):
        print("running python scenario: " + self.path)
        time.sleep(self.runtime)

    def setup(self, batcher):
        self.env = batcher.env
        python_scenario_list = batcher.python_scenarios
        python_scenario_list.append(self)


class JsonScenario(CarteavScenario):
    @accepts(lgsvl.simulator.Simulator, str)
    def __init__(self, simulator, path):
        super().__init__(simulator, path)
        self.type = ScenarioType.Json
        self.path = path
        file = open(path)
        self.json_data = json.load(file)
        self.runtime = 5

    def run(self):
        print("running json scenario: " + self.path)

        self.simulator.load(self.json_data["map"]["id"])

        for agent in self.json_data["agents"]:
            agent_state = lgsvl.AgentState()
            agent_transform = lgsvl.Transform.from_json(agent["transform"])
            agent_state.transform = agent_transform
            agent_type = lgsvl.AgentType(agent["type"])
            created_agent = self.simulator.add_agent(agent["variant"], agent_type, agent_state)
            agent_waypoints = []
            for wp in agent["waypoints"]:
                wp_pos = lgsvl.Vector(wp["position"]["x"], wp["position"]["y"], wp["position"]["z"])
                trigger = None if not wp["trigger"]["effectors"] else lgsvl.WaypointTrigger.from_json(wp["trigger"])

                if agent_type == lgsvl.AgentType.PEDESTRIAN:
                    waypoint = lgsvl.WalkWaypoint(wp_pos, wp["waitTime"], speed=wp["speed"], trigger=trigger)
                else:
                    wp_angle = lgsvl.Vector(wp["angle"]["x"], wp["angle"]["y"], wp["angle"]["z"])
                    waypoint = lgsvl.DriveWaypoint(wp_pos, wp["speed"], wp_angle, wp["waitTime"], trigger=trigger)

                agent_waypoints.append(waypoint)

            created_agent.follow(agent_waypoints)
            time.sleep(self.runtime)

