from environs import Env
import lgsvl
import json
import os

print("Python API Quickstart #4: Ego vehicle driving straight")
env = Env()

sim = lgsvl.Simulator(env.str("LGSVL__SIMULATOR_HOST", lgsvl.wise.SimulatorSettings.simulator_host),
                      env.int("LGSVL__SIMULATOR_PORT", lgsvl.wise.SimulatorSettings.simulator_port))


def batch_run_json_scenarios():
    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    rel_path = "json_scenarios/simple_pedestrian.json"
    abs_file_path = os.path.join(script_dir, rel_path)

    json_file = open(abs_file_path)
    json_scenario = json.load(json_file)
    sim.load(json_scenario["map"]["id"])

    for agent in json_scenario["agents"]:
        agent_state = lgsvl.AgentState()
        agent_transform = lgsvl.Transform.from_json(agent["transform"])
        agent_state.transform = agent_transform
        agent_type = lgsvl.AgentType(agent["type"])
        created_agent = sim.add_agent(agent["variant"], agent_type, agent_state)
        if agent_type == lgsvl.AgentType.PEDESTRIAN:
            agent_waypoints = [lgsvl.WalkWaypoint(wp["position"], wp["waitTime"], speed=wp["speed"],
                                                  trigger=lgsvl.WaypointTrigger.from_json(wp["trigger"])) for wp in
                               agent["waypoints"]]
        else:
            agent_waypoints = [lgsvl.DriveWaypoint(wp["position"], wp["speed"], wp["angle"], wp["waitTime"],
                                                   trigger=lgsvl.WaypointTrigger.from_json(wp["trigger"])) for wp in
                               agent["waypoints"]]
        created_agent.follow(agent_waypoints)



def batch_run_python_scenarios():
    return