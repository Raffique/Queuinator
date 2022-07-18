from datetime import datetime, time
from commands.adjust import adjust
from server import Server
from design_patterns import Subscriber, Publisher
from database import DBManager
from models import *
import json
import re
from timewatch import timewatch as tw

def sign_in_out(req, res=None):

    alias = req['alias']
    email = req['email']
    password = req['password']


    user = None
    if alias == "":
        user = DBManager.get_row(obj=User, email=email)
    else:
        user = DBManager.get_row(obj=User, alias=alias)

    if user == None:
        res.send(json.dumps({'status': 'user doesnt exist'}).encode())
        return

    service = DBManager.get_row(obj=Service, id=user['service1'])
    if service == None:
        res.send(json.dumps({'status': 'service doesnt exist'}).encode())
        return
    if service['active'] == False:
        res.send(json.dumps({'status': 'inactive service'}).encode())
        return

    del user['date']
    del service['last']
    del service['created']
    if user['password'] == password:
        res.send(json.dumps({'command':'sign-in-res', 'status': 'ok', 'service': service, 'user': user}).encode())