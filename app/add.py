import json
import os
from VarFile import VarFile
from AzureKeyVault import AzureKeyVault
from EnvironmentService import EnvironmentService

def add_var(environment, module, name, value, is_secret):
    _insert_variable(environment, module, name, value, is_secret)

def _insert_variable(environment, module, var_name, var_value, is_secret):
    print(f"Adding variable '{var_name}' to {module} in {environment}...")

    environment_service = EnvironmentService()

    key_vault_uri = environment_service.get_environment(environment)["vault"]
    key_vault = AzureKeyVault(key_vault_uri)

    if is_secret:
        key_vault_secret_id = key_vault.get_key_vault_secret_id(module, var_name)
        print(f"'{var_name}' is a secret variable. Adding to KeyVault as '{key_vault_secret_id}'...")
        
        key_vault.insert_secret(key_vault_secret_id, var_value)
        print(f"'{key_vault_secret_id}' successfully added to KeyVault")

    var_file = VarFile(environment, module)
    var_file.insert_variable(var_name, key_vault_secret_id if is_secret else var_value, is_secret)
    print(f"✅ '{var_name}' added.")

    