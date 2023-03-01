import os
import logging
import json
import azure.functions as func
from azure.identity import DeviceCodeCredential, ClientSecretCredential
from msgraph.core import GraphClient
from pprint import pprint

device_code_credential: DeviceCodeCredential
user_client: GraphClient
client_credential: ClientSecretCredential
app_client: GraphClient

client_id = os.getenv("CLIENT_ID", "00000000-0000-0000-0000-000000000000")
client_secret = os.getenv("CLIENT_SECRET")
from_email = os.getenv("FROM_EMAIL", "REDACTEDEmailPOC")
graph_scopes = os.getenv("GRAPH_SCOPE", "https://graph.microsoft.com/.default").split(" ")
tenant_id = os.getenv("TENANT_ID", "00000000-0000-0000-0000-000000000000")

endpoint = f"/users/{client_id}/sendmail"

# client_credential = ClientSecretCredential(tenant_id, client_id, client_secret)
# user_client = GraphClient(credential=client_credential, scopes=graph_scopes)
user_client = None

def test():
    print("test")

def main():
    recipients = ['rsandoval1@REDACTED.com', 'rsandoval2@REDACTED.com']
    subject = "Testing Microsoft Graph"
    body = "Hello world!"

    send(subject, body, recipients)

    print(tenant_id)

    print("Mail sent.\n")

def send(subject, body, recipients):
    request_body = {
        "message": {
            "subject": subject,
            "body": {
                "contentType": "text",
                "content": body
            },
            "toRecipients": []
        }
    }

    for recipient in recipients:
        request_body["message"]["toRecipients"].append({
            "emailAddress": { "address": recipient }
        })


    if (user_client is not None):
        user_client.post(endpoint, data=json.dumps(request_body), headers={"Content-Type": "application/json"})
    else:
        print(request_body)

    return (200, "OK")

if __name__ == "__main__":
    main()    