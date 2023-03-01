import logging
import azure.functions as func

from . import send_mail as mail
from . import template_mail as template

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

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

    if isinstance(data, list):
        html_template_list = html_template + "-list"
        content = ""

        for element in data:
            content += template.render(html_template_list, **element)

        body = template.render(html_template, content=content)
    else:
        body = template.render(html_template, **data)

    #status, result = mail.send(subject, body, send_to)

    print(body)

    if status == 200:
        result = f"Message sent to {','.join(send_to)}"

    return func.HttpResponse(result, status_code=status)