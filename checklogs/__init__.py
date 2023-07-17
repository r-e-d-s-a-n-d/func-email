import os
import sys
import datetime
import logging

dir_path =  os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'sendmail')))

import azure.functions as func
import query_log as query
from send_mail import SendMail

def main(req: func.HttpRequest) -> func.HttpResponse:
# def main(mytimer: func.TimerRequest) -> None:
#     utc_timestamp = datetime.datetime.utcnow().replace(
#         tzinfo=datetime.timezone.utc).isoformat()

    # if mytimer.past_due:
    #     logging.info('The timer is past due!')
        
    mail = SendMail()
    t = query.test()

    logging.info("Results")
    logging.info(t)
    return func.HttpResponse(t, status_code=200)
