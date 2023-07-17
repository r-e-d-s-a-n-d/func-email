import os
import logging
import json
import sys
from datetime import datetime, timedelta
from azure.identity import ManagedIdentityCredential, ClientSecretCredential
from azure.monitor.query import LogsQueryClient, MetricsQueryClient, LogsQueryStatus
from azure.core.exceptions import HttpResponseError

sys.path.append('../')

client_id = os.getenv('CLIENT_ID', '00000000-0000-0000-0000-000000000000')
client_secret = os.getenv('CLIENT_SECRET', 'REDACTED')
graph_scopes = os.getenv('GRAPH_SCOPE', 'https://graph.microsoft.com/.default').split(' ')
tenant_id = os.getenv('TENANT_ID', '00000000-0000-0000-0000-000000000000')
workspace = os.getenv('WORKSPACE_ID', 'd9691c06-68f4-477a-af60-a760248ac4c6')

#credential = ManagedIdentityCredential()
credential = ClientSecretCredential(tenant_id, client_id, client_secret)
client = LogsQueryClient(credential)
metrics_client = MetricsQueryClient(credential)


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime):
        return obj.strftime("%Y-%m-%d %I:%S %p")
    else:
        return str(obj)

# create function to run kql query 
def run_kql_query(query, workspace_id, time_range):
    query_results = client.query(workspace_id, query, time_range=time_range)
    return query_results

def to_json(query_results):
    json_results = []
    for table in query_results:
        for row in table.rows:
            json_results.append(dict(zip(table.columns, row)))
    return json_results

def test():
    query= """AppRequests | take 5
| extend FullName_ = tostring(Properties.FullName)
| extend TriggerReason_ = tostring(Properties.TriggerReason)
| project TimeGenerated, Id, Name, Success, FullName_, TriggerReason_"""
    
    return test_query(query)

def test_query(query):
    try:
        response = client.query_workspace(workspace, query, timespan=timedelta(days=1))
        if response.status == LogsQueryStatus.PARTIAL:
            # handle error here
            error = response.partial_error
            data = response.partial_data
            print(error)
        elif response.status == LogsQueryStatus.SUCCESS:
            data = response.tables
        
        json_data = to_json(data)
        
        return json_data

    except HttpResponseError as err:
        print("something fatal happened")
        print (err)

if __name__ == "__main__":
    # kql = options.config

    # for query in kql:
    #     print(f"Query: {query['kql']}")

    data = test()
    print(len(data))
    # print(json.dumps(data, indent=4, sort_keys=True, default=json_serial))