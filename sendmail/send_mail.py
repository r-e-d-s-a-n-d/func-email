import os
import logging
import json
import azure.functions as func
from azure.identity import ClientSecretCredential
from msgraph.core import GraphClient
from datetime import datetime, timedelta

class SendMail:
    def __init__(self):
        
        self.user_client: GraphClient
        client_credential: ClientSecretCredential

        client_id = os.getenv("CLIENT_ID", "00000000-0000-0000-0000-000000000000")
        client_secret = os.getenv("CLIENT_SECRET")
        from_email = os.getenv("FROM_EMAIL", "FuncEmail")
        graph_scopes = os.getenv("GRAPH_SCOPE", "https://graph.microsoft.com/.default").split(" ")
        tenant_id = os.getenv("TENANT_ID", "00000000-0000-0000-0000-000000000000")

        # client_credential = ClientSecretCredential(tenant_id, client_id, client_secret)
        # user_client = GraphClient(credential=client_credential, scopes=graph_scopes)
        self.user_client = None
        self.endpoint = f"/users/{client_id}/sendmail"
        

    def test(self):
        recipients = ['rsandoval1@REDACTED.com', 'rsandoval2@REDACTED.com']
        subject = "Testing Microsoft Graph"
        body = "Hello world!"

        self.send(subject, body, recipients)

        print("Mail sent.\n")

    def send(self, subject, body, recipients):
        
        prev_subject = os.getenv("subject")
        
        if (prev_subject == subject):
            timestamp = os.getenv('timeout')
            if timestamp is None:
                timeout = datetime.now() + timedelta(minutes=30)
                timestamp = str(timeout.timestamp())
                os.environ['timeout'] = timestamp

            datestamp = datetime.fromtimestamp(float(timestamp))
            return (200, f"SKIPPED - {datestamp}")
        else:
            os.environ['subject'] = subject

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


        if (self.user_client is not None):
            self.user_client.post(self.endpoint, data=json.dumps(request_body), headers={"Content-Type": "application/json"})
        else:
            print(request_body)

        return (200, ','.join(recipients))

if __name__ == "__main__":
    main()    
