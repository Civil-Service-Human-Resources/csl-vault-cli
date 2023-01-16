from AppServiceProperties import AppServiceProperties
from AzureProfile import AzureProfile
from EnvironmentService import EnvironmentService
from VarFile import VarFile
from AzureKeyVault import AzureKeyVault

def load(environment, module, name):
    environment_service = EnvironmentService()
    azure_profile = AzureProfile()

    environment_data = environment_service.get_environment(environment)

    subscription_id = azure_profile.get_subscription_id(environment)
    resource_group = environment_data["resourceGroup"]
    app_service_name = environment_data["modules"][module]

    app_service_properties = AppServiceProperties(subscription_id, resource_group, app_service_name)
    
    var_file = VarFile(environment, module)

    key_vault = AzureKeyVault(environment_data["vault"])

    variable_from_file = var_file.get_variable(name)

    var_value = variable_from_file["value"]

    property_value = key_vault.get_secret_key_vault_reference(var_value) if variable_from_file["sensitive"] else var_value

    app_service_properties.update_property(name, property_value)
    app_service_properties.push_updates_to_app_service()
    