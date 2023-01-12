import json
class EnvironmentService:
    def __init__(self):
        environments = open("data/environments.json", "r", encoding="utf-8-sig").read()
        environments = json.loads(environments)
        self.environments = environments

    def environment_exists(self, environment_name):
        return environment_name in self.environments.keys()

    def get_environment(self, environment_name):
        return self.environments[environment_name]