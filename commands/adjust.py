
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
            res.send(json.dumps({'response':'adjust', 'status': 'inactive service'}).encode())
            return

        #get current customer nuber and update it
        ticket, tickets = None, None
        

        if req['opt'] == '++':
            ticket, tickets = forward(req)
        elif req['opt'] == '--':
            ticket, tickets = reverse(req)
        elif req['opt'] == '=':
            pass

        if ticket == None:
            return

        #put req info in dispatch for screen update
        dispatch(req={'command':'adjust', 'number': ticket['number']})

        #set up data for boradcasr from server
        server.broadcast(json.dumps({'response':'adjust', 'ticket': ticket, 'tickets':tickets, 'sid':sid}), res)
        