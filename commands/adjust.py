
from database import DBManager
from models import *
import json
from .tickets import forward, reverse

def adjust(req, res=None, dispatch=None, server=None):

        #Extract data from request payload 
        sid = int(req['sid'])
        uid = int(req['uid'])

        #retreive Service from database and check if it is active
        service = DBManager.get_row(obj=Service, id=sid)
        if service['active'] == False:
            res.send(json.dumps({'status': 'inactive service'}).encode())
            return

        #get current customer nuber and update it
        number = None
        

        if req['opt'] == '++':
            number = forward(req)
        elif req['opt'] == '--':
            number = reverse(req)
        elif req['opt'] == '=':
            pass

        if number == None:
            return

        #put req info in dispatch for screen update
        dispatch(req={'command':'adjust', 'number': number})

        #set up data for boradcasr from server
        server.broadcast(json.dumps({'response':'adjust', 'number': number}), res)
        