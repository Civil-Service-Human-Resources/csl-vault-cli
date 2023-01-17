from VarFile import VarFile
from AzureKeyVault import AzureKeyVault
from EnvironmentService import EnvironmentService
from AppServiceProperties import AppServiceProperties
from AzureProfile import AzureProfile

def delete_var(args):
    print(f"Deleting variable '{args.name}' from {args.module} in {args.environment}...")

    environment = EnvironmentService()
    
    app_services_property_exists = get_list_of_app_services_a_property_exists(args.environment, args.name)

    variable_can_be_deleted = True
    if len(app_services_property_exists) > 0:
        print("This variable is currently being used in these app services: " + ", ".join(app_services_property_exists))
        user_answer = input("Are you sure you'd like to delete this variable? (Can only accept 'yes') ")
        variable_can_be_deleted = user_answer == "yes"

    if variable_can_be_deleted:

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
    else:
        print("Deletion of variable has been cancelled")

def get_list_of_app_services_a_property_exists(environment, property_name):
    azure_profile = AzureProfile()
    environment_data = EnvironmentService()

    environment_data = environment_data.get_environment(environment)
    modules = environment_data["modules"]

    apps_property_exists = []

    for module_name in modules.keys():
        app_service_name = modules[module_name]
        app_service_properties = AppServiceProperties(azure_profile.get_subscription_id(environment), environment_data["resourceGroup"], app_service_name)

        if app_service_properties.property_exists_in_app_service(property_name):
            apps_property_exists.append(app_service_name)

    return apps_property_exists
    