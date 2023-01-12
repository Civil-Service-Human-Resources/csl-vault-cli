from VarFile import VarFile
from AzureKeyVault import AzureKeyVault
import json
from EnvironmentService import EnvironmentService

def delete_var(args):
    print(f"Deleting variable '{args.name}' from {args.module} in {args.environment}...")

    environment = EnvironmentService()

    file = VarFile(args.environment, args.module)
    variable = file.get_variable(args.name)
    
    if variable["sensitive"]:
        key_vault = AzureKeyVault(environment.get_environment(args.environment)["vault"])
        
        key_vault_secret_id = key_vault.get_key_vault_secret_id(args.module, args.name)
        print(f"'{args.name}' is a secret variable. Deleting from KeyVault as '{key_vault_secret_id}'...")
        
        key_vault.delete_secret(key_vault_secret_id)
        print(f"'{key_vault_secret_id}' successfully deleted from KeyVault.")
        print("ℹ️ This variable has been soft-deleted. Use the Azure CLI's `az keyvault secret purge` command to permanently delete it. Learn more here: https://learn.microsoft.com/en-us/cli/azure/keyvault/secret?view=azure-cli-latest#az-keyvault-secret-purge")

    file.delete_variable(args.name)
    print(f"✅ '{args.name}' deleted.")

    