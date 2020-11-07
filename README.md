# AzureWebAppReporting
Report on webapps in Azure and pushes the data to a log aggregator.

## To get started 

Fill in your client_id, secret and tenant in main.py and your log aggregator customer_id and shared_key in aggregation.py

**NOTE that this script can take a while if you have a large amount of app services, it is best run in a pipeline on Azure DevOps. Please be patient!**

```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
python main.py
```

## Harley, why not Azure Identity?

Some eager Azure users will notice that this resource does not use the latest version of some packages - notably using the azure.common.credentials package over azure.identity. This is because Azure Identity does not have updated documentation on Azure's site (yet) and does not support all resources! This script will move over to the azure identity package in the future.
