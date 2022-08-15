from datetime import datetime, time
from server import Server
from design_patterns import Subscriber, Publisher
from database import DBManager
from models import *
import json
import re
from timewatch import timewatch as tw
from ticketMaker import TicketMaker as tk



############################  TICKET FUNCTIONS ######################################
def add_tickets(req, res=None):

    sid = int(req['sid'])

    service = DBManager.get_row(obj=Service, id=sid)
    limit = service['limit']
    x=service['tickets']
    print(type(x))
    tickets = json.loads(x)
    recycle_bin = json.loads(service['recycle_bin'])
    ticket = None
    if tickets == []:

        number = 0
        if recycle_bin != []:
            number = recycle_bin[-1]['number']

        if number+1 > limit:
            ticket = 0 #set to 0 if numbe is over limit
            tickets.append(tk(number=ticket, sid=sid).dict())
            
        else:
            if recycle_bin == []:
                ticket = number #set to 0 if the recycle bin is empty
            else:
                ticket = number + 1 #set to next number after last nunmber entered in the bin
            tickets.append(tk(number=ticket, sid=sid).dict())
            
    else:
        temp = tickets[-1]['number']
        if temp+1 > limit:
            ticket = 0
            tickets.append(tk(number=ticket, sid=sid).dict())
            
        else:
            ticket = temp + 1
            tickets.append(tk(number=ticket, sid=sid).dict())
            

    DBManager.mod_row(obj=Service, id=sid, attr='tickets', value=json.dumps(tickets))

    res.send(json.dumps({'response':'add ticket', 'ticket':ticket}).encode())


def dequeue_tickets(sid:int):
    #removes number from front of queue because that number is called

    #1 can place ticket number  in forgiveness queue automaticcally if number is passed too quickly or manually
    #2 customer can place themselves in forgiveness que from customer app

    service = DBManager.get_row(obj=Service, id=sid)
    tickets = json.loads(service['tickets'])
    recycle_bin = json.loads(service['recycle_bin'])
    if tickets == []:
        return None

    ticket = tickets[0]
    if len(tickets) == 1:
        tickets = []
    else:
        tickets = tickets[1:]
    
    recycle_bin.append(ticket)
    #limit size of recycle bin set up a config file for size 
    if len(recycle_bin) >= 100:
        recycle_bin = recycle_bin[1:]
    DBManager.mod_row(obj=Service, id=sid, attr='recycle_bin', value=json.dumps(recycle_bin))
    DBManager.mod_row(obj=Service, id=sid, attr='tickets', value=json.dumps(tickets))

    return ticket

#this doesnt have any planned use as of yet
# deletes number from back of queue
def pop_tickets(req, res=None):

    sid = int(req['sid'])
    service = DBManager.get_row(obj=Service, id=sid)
    tickets = json.loads(service['tickets'])
    tickets = tickets[0:-1]
    DBManager.mod_row(obj=Service, id=sid, attr='tickets', value=str(tickets))

def check_tickets(req, res=None):
    sid = int(req['sid'])

    service = DBManager.get_row(obj=Service, id=sid)
    tickets = json.loads(service['tickets'])
    res.send(json.dumps({'tickets':tickets}).encode())


def forward(req, res=None):

    sid = int(req['sid'])
    service = DBManager.get_row(obj=Service, id=sid)
    print('1')
    tickets = json.loads(service['tickets'])
    print('2')
    recycle_bin = json.loads(service['recycle_bin'])

    if tickets == []:
        return None

    ticket = tickets[0]

    if len(tickets) <= 1:
        tickets = []
    else:
        tickets = tickets[1:]

    print('3')
    recycle_bin.append(ticket)
    #limit size of recycle bin set up a config file for size 
    if len(recycle_bin) >= 100:
        recycle_bin = recycle_bin[1:]

    print('4')
    DBManager.mod_row(obj=Service, id=sid, attr='recycle_bin', value=json.dumps(recycle_bin))
    DBManager.mod_row(obj=Service, id=sid, attr='tickets', value=json.dumps(tickets))

    return ticket['number']


def reverse(req, res=None):

    sid = int(req['sid'])
    service = DBManager.get_row(obj=Service, id=sid)
    tickets = json.loads(service['tickets'])
    recycle_bin = json.loads(service['recycle_bin'])

    if recycle_bin == []:
        return None

    ticket = recycle_bin.pop()
    tickets = [ticket] + tickets

    DBManager.mod_row(obj=Service, id=sid, attr='recycle_bin', value=json.dumps(recycle_bin))
    DBManager.mod_row(obj=Service, id=sid, attr='tickets', value=json.dumps(tickets))

    if recycle_bin != []:
        return recycle_bin[-1]['number']
    else:
        if ticket['number'] - 1 < 0:
            return service['limit']
        else:
            return ticket['number'] - 1




################### MISSED TICKET FUNCTIONS #################################

# fix up 

def add_missed_tickets(req, res=None):

    sid = int(req['sid'])
    number = int(req['number'])

    service = DBManager.get_row(obj=Service, id=sid)
    missed_tickets = json.loads(service['missed_tickets'])
    missed_tickets.append(number)
    DBManager.mod_row(obj=Service, id=sid, attr='missed_tickets', value=json(missed_tickets))

    res.send(json.dumps({'status':'OK'}).encode())

def dequeue_missed_tickets(sid:int):
 

    service = DBManager.get_row(obj=Service, id=sid)
    missed_tickets = json.loads(service['missed_tickets'])
    if missed_tickets == []:
        return None
    ticket = missed_tickets[0]
    missed_tickets = missed_tickets[1:]
    DBManager.mod_row(obj=Service, id=sid, attr='missed_tickets', value=json.dumps(missed_tickets))

    return ticket

def check_missed_tickets(req, res=None):

    sid = int(req['sid'])
    service = DBManager.get_row(obj=Service, id=sid)
    missed_tickets = json.loads(service['missed_tickets'])
    res.send(json.dumps({'missed_tickets':missed_tickets}).encode())