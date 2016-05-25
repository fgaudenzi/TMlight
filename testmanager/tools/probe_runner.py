#from testagent.services.WorkerService import WorkerService, WorkerServiceException
#from tornado.options import options
#from tornado.options import parse_command_line, parse_config_file
#from testagent.options import DEFAULT_CONFIG_FILE
#from testagent.subscription_options import DEFAULT_SUBSCRIPTION_FILE
#from celery import Celery
#from testagent.tasks import start_certification
#import fileinput
from testmanager.model.evaluation import Evidence
import datetime
from testmanager.database import db_session
import thread


#TODO: delete comment when deployed
#arse_config_file(options.conf, final=False)
#arse_config_file(options.subscription_conf, final=False)
#pp = Celery()
#WorkerService().configure(app, options)

def runner_thread(probe_id,message_xml):
    xml = message_xml
    #result = start_certification.delay(xml)
    result=True
    r=Evidence(probe_id,result,datetime.datetime.now())
    db_session.add(r)
    db_session.commit()



def runner_p(p_id,message_xml):
    print "starting thread"
    thread.start_new_thread(runner_thread, (p_id,message_xml))
    return True