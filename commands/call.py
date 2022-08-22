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
            res.send(json.dumps({'response':'call', 'status': 'inactive service'}).encode())
            return

        sname = service['name']
        sector = service['sector']
        
        
        ticket, tickets = dequeue_tickets(sid)
        if ticket == None:
            #res.send(json.dumps({'status':'empty'}).encode())
            return
        number = ticket['number']
        print("number -> {}".format(number))

        #get current duration from current time - last time
        last = service['last']
        now = datetime.now()
        duration = tw(now) - tw(last)

        #put req info in dispatch for screen update
        dispatch(req={'command':'call', 'number': number, "counter":counter, 'sname':sname, 'sector':sector, 'duration':duration})

        #set up data for boradcasr from server
        mssg = json.dumps({'response':'call', 'ticket': ticket, 'tickets':tickets, "counter":counter, 'sname':sname, 'sector':sector, 'sid':sid, 'uid':uid})
        server.broadcast(mssg, res)
        
        #Update number and last attribute in Service
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
        sid = req['sid']
        uid = req['uid']

        #retreive Service from database and check if it is active
        service = DBManager.get_row(obj=Service, id=sid)
        

        missed_ticket, missed_tickets = dequeue_missed_tickets(req, res)
        if missed_ticket == None:
            return

        #get current duration from current time - last time
        last = service['last']
        now = datetime.now()
        duration = tw(now) - tw(last)

        #put req info in dispatch for screen update
        dispatch(req={'command':'missed_call', 'number': missed_ticket['number'], "counter":counter})

        #set up data for boradcasr from server
        server.broadcast(json.dumps({'response':'missed_call', 'missed_ticket': missed_ticket, 'missed_tickets':missed_tickets, "counter":counter, 'sid':sid, 'uid':uid}), res)
        
        #Update number and last attribute in Service
        DBManager.mod_row(obj=Service, id=sid, attr='last', value=now)
        

        #added a new row to history
        try:
            history = None 
            if duration == -1:
                history = History(
                    serviceid=sid,
                    servicename='',
                    userid=uid,
                    username='',
                    number=missed_ticket['number'],
                    wait = "00:00:00"
                )
            else:
                history = History(
                    serviceid=sid,
                    servicename='',
                    userid=uid,
                    username='',
                    number=missed_ticket['number'],
                    wait = duration.gettime()
                )
            DBManager.add_row(history)
        except Exception as e:
            print(e)