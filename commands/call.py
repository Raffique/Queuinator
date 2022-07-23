from datetime import datetime, time
from server import Server
from design_patterns import Subscriber, Publisher
from database import DBManager
from models import *
import json
import re
from timewatch import timewatch as tw
from .tickets import *

def call(req, res=None, dispatch=None, server=None):
        
        #Extract data from request payload
        
        counter = req['counter']
        sid = int(req['sid'])
        uid = int(req['uid'])
        


        #retreive Service from database and check if it is active
        service = DBManager.get_row(obj=Service, id=sid)
        if service['active'] == False:
            res.send(json.dumps({'status': 'inactive service'}).encode())
            return
        sname = service['name']
        sector = service['sector']
        
        #get current customer nuber and update it
        """
        number = service['number']
        if service['number'] < service['limit']:
            number += 1
        else:
            number = 0
        """
        number = dequeue_tickets(sid)
        if number == None:
            #res.send(json.dumps({'status':'empty'}).encode())
            return
        print("number -> {}".format(number))

        #get current duration from current time - last time
        last = service['last']
        now = datetime.now()
        duration = tw(now) - tw(last)

        #put req info in dispatch for screen update
        dispatch(req={'command':'call', 'number': number, "counter":counter, 'sname':sname, 'sector':sector, 'duration':duration})

        #set up data for boradcasr from server
        server.broadcast(json.dumps({'command':'call-res', 'number': number, "counter":counter, 'sname':sname, 'sector':sector}), res)
        
        #Update number and last attribute in Service
        DBManager.mod_row(obj=Service, id=service['id'], attr='number', value=number)
        DBManager.mod_row(obj=Service, id=service['id'], attr='last', value=now)
        

        #added a new row to history
        try:
            history = None 
            if duration == -1:
                history = History(
                    serviceid=sid,
                    servicename=sname,
                    userid=uid,
                    username='',
                    number=number,
                    wait = "00:00:00"
                )
            else:
                history = History(
                    serviceid=sid,
                    servicename=sname,
                    userid=uid,
                    username='',
                    number=number,
                    wait = duration.gettime()
                )
            DBManager.add_row(history)
        except Exception as e:
            print(e)


def missed_call(req, res=None, dispatch=None, server=None):
        
        #Extract data from request payload 
        counter = req['counter']
        sid = int(req['sid'])
        uid = int(req['uid'])

        #retreive Service from database and check if it is active
        service = DBManager.get_row(obj=Service, id=sid)
        if service['active'] == False:
            res.send(json.dumps({'status': 'inactive service'}).encode())
            return

        sname = service['name']

        #get current customer nuber and update it
        """
        number = service['number']
        if service['number'] < service['limit']:
            number += 1
        else:
            number = 0
        """
        number = dequeue_missed_tickets(sid)
        if number == None:
            #res.send(json.dumps({'status':'empty'}).encode())
            return

        #get current duration from current time - last time
        last = service['last']
        now = datetime.now()
        duration = tw(now) - tw(last)

        #put req info in dispatch for screen update
        dispatch(req={'number': number, "counter":counter})

        #set up data for boradcasr from server
        server.broadcast(json.dumps({'number': number, "counter":counter}), res)
        
        #Update number and last attribute in Service
        DBManager.mod_row(obj=Service, id=service['id'], attr='number', value=number)
        DBManager.mod_row(obj=Service, id=service['id'], attr='last', value=now)
        

        #added a new row to history
        try:
            history = None 
            if duration == -1:
                history = History(
                    serviceid=sid,
                    servicename=sname,
                    userid=uid,
                    username='',
                    number=number,
                    wait = "00:00:00"
                )
            else:
                history = History(
                    serviceid=sid,
                    servicename=sname,
                    userid=uid,
                    username='',
                    number=number,
                    wait = duration.gettime()
                )
            DBManager.add_row(history)
        except Exception as e:
            print(e)