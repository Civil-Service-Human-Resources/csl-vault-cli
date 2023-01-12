from VarFile import VarFile
from AzureKeyVault import AzureKeyVault
import json
from EnvironmentService import EnvironmentService

def update_var(args):
    print(f"Updating variable '{args.name}' to {args.module} in {args.environment}...")

    environment_service = EnvironmentService()
    key_vault = AzureKeyVault(environment_service.get_environment(args.environment)["vault"])

    file = VarFile(args.environment, args.module)
    variable = file.get_variable(args.name)

    key_vault_secret_id = key_vault.get_key_vault_secret_id(args.module, args.name)

    if variable["sensitive"]:
        print(f"'{args.name}' is a secret variable. Updating in KeyVault as '{key_vault_secret_id}'...")
        
        key_vault.insert_secret(key_vault_secret_id, args.value)
        print(f"'{key_vault_secret_id}' successfully updating in KeyVault")

    file.update_variable(args.name, key_vault_secret_id if variable["sensitive"] else args.value)
    print(f"✅ '{args.name}' updated.")

    

