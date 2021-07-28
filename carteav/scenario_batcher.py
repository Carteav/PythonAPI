from environs import Env
import lgsvl
import os
from scenario import *
from pyplugin import PluginLoader
from pluginbase import PluginBase


class Batcher:
    def __init__(self, json_dir, python_dir):
        self.plugin_base = PluginBase(package='carteav.scenarios')
        self.json_dir = json_dir
        self.python_dir = python_dir
        self.plugin_source = self.plugin_base.make_plugin_source(searchpath=[python_dir])
        self.env = Env()
        self.sim = lgsvl.Simulator(self.env.str("LGSVL__SIMULATOR_HOST", lgsvl.wise.SimulatorSettings.simulator_host),
                                   self.env.int("LGSVL__SIMULATOR_PORT", lgsvl.wise.SimulatorSettings.simulator_port))

        self.json_scenarios = []
        self.python_scenarios = []

    def load_json_scenarios(self, directory):
        for file in os.listdir(directory):
            if file.endswith(".json"):
                file_path = os.path.join(directory, file)
                file_path = os.path.join(os.path.dirname(__file__), file_path)
                print("Loading json scenario: " + file_path)
                self.json_scenarios.append(JsonScenario(self.sim, file_path))

    def load_python_scenarios(self, directory):
        for plugin_name in self.plugin_source.list_plugins():
            #if file.endswith(".py"):
            #file_path = os.path.join(directory, file)
            #file_path = os.path.join(os.path.dirname(__file__), file_path)
            print("Loading python scenario: " + plugin_name)
            python_scenario = self.plugin_source.load_plugin(plugin_name)
            #python_scenarios_in_file = PluginLoader("carteav.scenario.CarteavScenario", file_path)
            #loaded_python_scenarios = [python_scenario(self.sim, file_path) for python_scenario in
             #                          python_scenarios_in_file]
            #self.python_scenarios.Append(python_scenario)
            python_scenario.setup(self)

    def load(self):
        self.load_json_scenarios(self.json_dir)
        self.load_python_scenarios(self.python_dir)

    def run_json_scenarios(self):
        for json_scenario in self.json_scenarios:
            json_scenario.run()

    def run_python_scenarios(self):
        for python_scenario in self.python_scenarios:
            python_scenario.run()

    def run(self):
        scenarios = [*self.json_scenarios, *self.python_scenarios]
        for scenario in scenarios:
            scenario.run()



batcher = Batcher("json_scenarios", "python_scenarios")
batcher.load()
batcher.run()
