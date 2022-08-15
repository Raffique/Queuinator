from datetime import datetime, time
from server import Server
from design_patterns import Subscriber, Publisher
from database import DBManager
from models import *
import json
import re
from timewatch import timewatch as tw



def transfer_req(req, res=None):
    services = DBManager.get_row(obj=Service, active=True)
    tickets = []
    idx = 0
    

    for m in range(len(services)):
        print(m)
        if req['sid'] == services[m]['id']:
            tickets = json.loads(services[m]['tickets'])
            idx = m
        else:
            del services[m]['created']
            del services[m]['last']
    
    del services[idx]
    print("deleted that servie from list")

    mssg = json.dumps({'response':'transfer_req', 'services':services, 'tickets':tickets})
    print("message encoded!")
    try:
        res.send(mssg.encode())
    except Exception as e:
        print(e)
    print("finised")
    
    
def transfer_update(req, res=None):
    print("transfer update has reached be proud of yourself young lad its never an easy road")