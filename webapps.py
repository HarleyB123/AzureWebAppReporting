import json

from azure.mgmt.monitor import MonitorManagementClient
from azure.mgmt.web import WebSiteManagementClient
from msrest.exceptions import ClientException


def get_all_webapps(credentials, rgs):
    all_webapps = []
    for sub, groups in rgs.items():
        web_client = WebSiteManagementClient(credentials, sub)
        monitor_client = MonitorManagementClient(credentials, sub)
        for rg in groups:
            for site in web_client.web_apps.list_by_resource_group(rg):
                get_config = web_client.web_apps.get_configuration(rg, site.name)
                resource_id = f"/subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.Web/sites/{site.name}"
                AuditLogs = "No Audit Logs"
                try:
                    monitor_client.diagnostic_settings.get(
                        resource_id,
                        "diagnostic-log-name",  # Place the name of your diagnostic log here!
                    )
                    AuditLogs = True
                except ClientException as ex:
                    pass

                webapp_data = dict(
                    {
                        "Subscription": sub,
                        "Resource Group": rg,
                        "App Service Name": site.name,
                        "HTTPS_ONLY": site.https_only,
                        "FTPS": get_config.ftps_state,
                        "TLS": get_config.min_tls_version,
                        "Always-On": get_config.always_on,
                        "Audit Logs": AuditLogs,
                        "Kind": site.kind,
                        "Location": site.location,
                    }
                )
                all_webapps.append(webapp_data)
    return json.dumps(all_webapps)
