import json

class VarFile:
    def __init__(self, environment, module):
        self.environment = environment
        self.module = module

    def variable_exists(self, variable_name):
        file = open(f"data/modules/{self.module}/{self.environment}-vars.json")
        variables = json.loads(file.read())
        return variable_name in [v["name"] for v in variables]

    def insert_variable(self, variable_name, variable_value, is_secret):
        file = open(f"data/modules/{self.module}/{self.environment}-vars.json")
        variables = json.loads(file.read())
        variables.append({
            "name": variable_name,
            "sensitive": is_secret,
            "value": variable_value
        })
        file_to_write = open(f"data/modules/{self.module}/{self.environment}-vars.json", "w")
        file_to_write.write(json.dumps(variables, indent=4))
        file_to_write.close()

    def get_variable(self, variable_name):
        file = open(f"data/modules/{self.module}/{self.environment}-vars.json")
        variables = json.loads(file.read())
        return next((var for var in variables if var["name"] == variable_name), None)

    def get_all_variables(self):
        file = open(f"data/modules/{self.module}/{self.environment}-vars.json")
        return json.loads(file.read())

    def update_variable(self, variable_name, new_value):
        file = open(f"data/modules/{self.module}/{self.environment}-vars.json")
        variables = json.loads(file.read())
        next(var for var in variables if var["name"] == variable_name)["value"] = new_value
        file_to_write = open(f"data/modules/{self.module}/{self.environment}-vars.json", "w")
        file_to_write.write(json.dumps(variables, indent=4))
        file_to_write.close()

    def delete_variable(self, variable_name):
        file = open(f"data/modules/{self.module}/{self.environment}-vars.json")
        variables = json.loads(file.read())
        variables = [var for var in variables if var["name"] != variable_name]
        file_to_write = open(f"data/modules/{self.module}/{self.environment}-vars.json", "w")
        file_to_write.write(json.dumps(variables, indent=4))
        file_to_write.close()
