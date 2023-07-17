import os
import logging
import sys
from datetime import datetime

dir_path =  os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path)

import azure.functions as func
import template_mail as template
from send_mail import SendMail

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    mail = SendMail()

    prev_subject = os.getenv("subject")
    send_to = ['rsandoval@REDACTED.com']
    subject = 'REDACTED Alert'
    html_template = 'default'
    data = {}

    status = 200

    try:
        req_body = req.get_json()
    except ValueError:
        pass
    else:
        send_to = req_body.get('sendTo')
        subject = req_body.get('subject')
        html_template = req_body.get('template')
        data = req_body.get('data')


    if not isinstance(send_to, list):
        sendto_list = []
        sendto_list.append(send_to)
        send_to = sendto_list

    if (prev_subject == subject):
        timeout = os.getenv('timeout')
        if timeout is not None:
            timestamp = datetime.fromtimestamp(float(timeout))
            now = datetime.now()
            if (now > timestamp):
                os.environ['subject'] = ''

    if isinstance(data, list):
        html_template_list = html_template + "-list"
        content = ""

        for element in data:
            content += template.render(html_template_list, **element)

        body = template.render(html_template, content=content)
    else:
        body = template.render(html_template, **data)

    status, result = mail.send(subject, body, send_to)

    print(body)

    return func.HttpResponse(result, status_code=status)