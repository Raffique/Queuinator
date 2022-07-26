from datetime import datetime, time
from server import Server
from design_patterns import Subscriber, Publisher
from database import DBManager
from models import *
import json
import re
from timewatch import timewatch as tw
from commands import call, adjust, transfer, announce, sign_in_out, tickets


def isEmail(email):
    
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
  
    if(re.search(regex,email)):   
        return True   
    else:   
        return False   


class Controller(Subscriber, Publisher):

    def __init__(self, name):
        Publisher.__init__(self)
        Subscriber.__init__(self, name)
        self.server = Server()
        self.server.register(self)
        self.call = call.call
        self.adjust = adjust.adjust
        self.transfer_req = transfer.transfer_req
        self.transfer_update = transfer.transfer_update
        #self.announce = announce.announce
        self.sign_in_out = sign_in_out.sign_in_out


    def startserver(self):
        self.server.main()

    def stopserver(self):
        self.server.stop()

    def update(self, req, res=None):

        print(req)
        req = json.loads(req)
        
        if req['command'] == 'call':
            self.call(req, res, self.dispatch, self.server)
        elif req['command'] == 'adjust':
            self.adjust(req, res, self.dispatch, self.server)
        elif req['command'] == 'transfer_req':
            self.transfer_req(req, res)
        elif req['command'] == 'transfer_update':
            self.transfer_update(req, res)
        elif req['command'] == 'announce':
            print("announce activated!!...")
        elif req['command'] == 'sign-in':
            print("sign-in activated!!...")
            self.sign_in_out(req, res)
        elif req['command'] == 'sign-out':
            print("sign-out activated!!...")
           


    def signin(self, req, res=None):
        username = req['username']
        password = req['password']
        user = None
        if isEmail(username):
            user = DBManager.get_row(obj=User, email=username)
        else:
            user = DBManager.get_row(obj=User, alias=username)

        if user != None:
            if password == user['password']:
                user['status'] = 200
                user = json.dumps(user)
                res.send(user.encode())
            else:
                user['status'] = 300
                user = json.dumps(user)
                res.send(user.encode())
        
        user = {'status', 404}
        user = json.dumps(user)
        res.send(user.encode())

    def lastsave(self):
        pass
