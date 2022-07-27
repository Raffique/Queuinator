from datetime import datetime, time
from server import Server
from design_patterns import Subscriber, Publisher
from database import DBManager
from models import *
import json
import re
from timewatch import timewatch as tw


def transfer_req(req, res=None):
    #print("enters transfer req function")

    services = DBManager.get_row(obj=Service, active=True)
    for m in range(len(services)):
        del services[m]['created']
        del services[m]['last']
    mssg = json.dumps({'response':'transfer_req', 'services':services})
    res.send(mssg.encode())
    print("finised")
    
    
def transfer_update(req, res=None):
    print("transfer update has reached be proud of yourself young lad its never an easy road")