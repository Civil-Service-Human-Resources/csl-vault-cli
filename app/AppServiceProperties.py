from azure.mgmt.web import WebSiteManagementClient 
from azure.identity import DefaultAzureCredential

class AppServiceProperties:
    def __init__(self, subscription_id, resource_group, app_service_name):
        self.resource_group = resource_group
        self.app_service_name = app_service_name
        credential = DefaultAzureCredential()
        self.web_client = WebSiteManagementClient(credential=credential, subscription_id=subscription_id)
        self.app_settings = self.web_client.web_apps.list_application_settings(resource_group, app_service_name)

    def get_app_properties(self):
        return self.app_settings.properties

    def update_property(self, property_name, property_value):
        self.app_settings.properties.update({ property_name: property_value })

    def push_updates_to_app_service(self):
        self.web_client.web_apps.update_application_settings(
            self.resource_group, 
            self.app_service_name, 
            app_settings=self.app_settings
        )