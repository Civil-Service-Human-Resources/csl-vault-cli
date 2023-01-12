import json
from VarFile import VarFile
from AzureKeyVault import AzureKeyVault
from EnvironmentService import EnvironmentService

def add(file_path):
    environment_service = EnvironmentService()
    secret_variables = []

    bulk_variables = json.loads(open(file_path, "r").read())

    for i in bulk_variables:
            environment = i["environment"]
            module = i["module"]
            values = i["values"]

            var_file = VarFile(environment, module)

            for v in values:
                var_name = v["name"]
                var_value = v["value"]
                is_secret = v["secret"]

                key_vault_uri = environment_service.get_environment(environment)["vault"]
                key_vault = AzureKeyVault(key_vault_uri)
                key_vault_secret_id = key_vault.get_key_vault_secret_id(module, var_name)

                var_file.insert_variable(var_name, key_vault_secret_id if is_secret else var_value, is_secret)
                print(f"Inserted variable in file: {var_name}")

                if is_secret:
                    secret_variables.append({
                        "environment": environment,
                        "name": key_vault_secret_id,
                        "value": var_value
                    })
                    print(f"🔑 Variable '{var_name}' queued to be added to the Key Vault")
            
    for secret_variable in secret_variables:
        key_vault_uri = environment_service.get_environment(secret_variable["environment"])["vault"]
        key_vault = AzureKeyVault(key_vault_uri)
        key_vault.insert_secret(secret_variable["name"], secret_variable["value"])
        print("✅ Inserted secret '" + secret_variable["name"] + "' to the Key Vault")