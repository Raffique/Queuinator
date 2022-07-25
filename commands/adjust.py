
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
        number = service['number']

        if req['opt'] == '++':
            forward(req)
            if service['number'] < service['limit']:
                number += 1
            else:
                number = 0
        elif req['opt'] == '--':
            reverse(req)
            if service['number'] == 0:
                number = service['limit']
            else:
                number -= 1
        elif req['opt'] == '=':
            number = int(req['data'])

        #put req info in dispatch for screen update
        dispatch(req={'command':'adjust', 'number': number})

        #set up data for boradcasr from server
        server.broadcast(json.dumps({'response':'adjust', 'number': number,}), res)
        
        #Update number and last attribute in Service
        DBManager.mod_row(obj=Service, id=service['id'], attr='number', value=number)
