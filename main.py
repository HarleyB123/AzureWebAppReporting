from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.subscription import SubscriptionClient

from aggregation import post_to_log_aggregator
from webapps import get_all_webapps

client_id = ""
secret = ""
TENANT = ""

CREDENTIALS = ServicePrincipalCredentials(
    client_id=client_id, secret=secret, tenant=TENANT,
)


def list_subscriptions():
    client = SubscriptionClient(CREDENTIALS)
    # ignore disabled subscriptions
    subs = [
        sub.subscription_id
        for sub in client.subscriptions.list()
        if sub.state.value == "Enabled"
    ]

    return subs


def list_resource_groups():
    subs = list_subscriptions()
    resource_groups = {}

    for sub in subs:
        resource_group_client = ResourceManagementClient(CREDENTIALS, sub)
        rgs = resource_group_client.resource_groups.list()

        # generate a list of resource groups
        groups = [rg.name for rg in rgs]

        # create a nested dictionary -- {"sub_id": {[rg1, rg2, rg3]}, "sub_id2": {[rg1, rg2, rg3]}}
        resource_groups[sub] = groups
    return resource_groups


def main():
    rgs = list_resource_groups()
    webapps = get_all_webapps(CREDENTIALS, rgs)
    post_to_log_aggregator(webapps, "WebAppData")


if __name__ == "__main__":
    main()
