from datetime import datetime, time
from server import Server
from design_patterns import Subscriber, Publisher
from database import DBManager
from models import *
import json
import re
from timewatch import timewatch as tw


def transfer_req(req, res=None):
    
    sid = req['sid']
    uid = req['req']

    services = DBManager.get_row(obj=Service, active=True)
    res.send(json.dumps({'response':'transfer_req', 'services':services}).encode())

    
def transfer_update(req, res=None):
    pass