from datetime import datetime, time
from server import Server
from design_patterns import Subscriber, Publisher
from database import DBManager
from models import *
import json
import re
from timewatch import timewatch as tw

def adjust(self, req, res=None, dispatch=None, server=None):

        #Extract data from request payload 
        sname = req['sname']
        counter = req['counter']
        sid = int(req['sid'])
        uid = int(req['uid'])

        #retreive Service from database and check if it is active
        service = DBManager.get_row(obj=Service, id=sid)
        if service['active'] == False:
            res.send(json.dumps({'status': 'inactive service'}).encode())
            return

        #get current customer nuber and update it
        number = service['number']

        if req['op'] == '++':
            if service['number'] < service['limit']:
                number += 1
            else:
                number = 0
        elif req['op'] == '--':
            if service['number'] == 0:
                number = service['limit']
            else:
                number -= 1
        elif req['op'] == '=':
            number = int(req['data'])

        #put req info in dispatch for screen update
        dispatch(req={'number': number, "counter":counter})

        #set up data for boradcasr from server
        server.broadcast(json.dumps({'number': number, "counter":counter}), res)
        
        #Update number and last attribute in Service
        DBManager.mod_row(obj=Service, id=service['id'], attr='number', value=number)
