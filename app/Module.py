import os

class Module:
    def get_list_of_modules(self):
        return os.listdir("data/modules")

    def moduleExists(self, module_name):
        modules = self.get_list_of_modules()
        return module_name in modules