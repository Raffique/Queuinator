from datetime import datetime, time
from server import Server
from design_patterns import Subscriber, Publisher
from database import DBManager
from models import *
import json
import re
from timewatch import timewatch as tw

def stringlist_to_list(x:str):
    if x[0] != '[' and x[-1] != ']':
        return None
    if x == "[]":
        return [] 
    x = x[1:-1]
    x = x.split(',')
    x = [int(y) for y in x]
    return x

############################  TICKET FUNCTIONS ######################################
def add_tickets(req, res=None):

    sid = int(req['sid'])

    service = DBManager.get_row(obj=Service, id=sid)
    number = service['number']
    limit = service['limit']
    tickets = stringlist_to_list(service['tickets'])
    ticket = None
    if tickets == []:
        if number+1 > limit:
            tickets.append(0)
            ticket = 0
        else:
            tickets.append(number+1)
            ticket = number + 1
    else:
        temp = tickets[-1]
        if temp+1 > limit:
            tickets.append(0)
            ticket = 0
        else:
            tickets.append(temp+1)
            ticket = temp + 1

    DBManager.mod_row(obj=Service, id=sid, attr='tickets', value=str(tickets))

    res.send(json.dumps({'ticket':ticket}).encode())


def dequeue_tickets(sid:int):
    #removes number from front of queue because that number is called

    #1 can place ticket number  in forgiveness queue automaticcally if number is passed too quickly or manually
    #2 customer can place themselves in forgiveness que from customer app

    service = DBManager.get_row(obj=Service, id=sid)
    tickets = stringlist_to_list(service['tickets'])
    if tickets == []:
        return None
    ticket = tickets[1:]
    DBManager.mod_row(obj=Service, id=sid, attr='tickets', value=str(tickets))
    return ticket

# deletes number from back of queue
def pop_tickets(req, res=None):

    sid = int(req['sid'])
    service = DBManager.get_row(obj=Service, id=sid)
    tickets = stringlist_to_list(service['tickets'])
    tickets = tickets[0:-1]
    DBManager.mod_row(obj=Service, id=sid, attr='tickets', value=str(tickets))

def check_tickets(req, res=None):

    sid = int(req['sid'])

    service = DBManager.get_row(obj=Service, id=sid)
    tickets = stringlist_to_list(service['tickets'])
    res.send(json.dumps({'tickets':tickets}).encode())



################### MISSED TICKET FUNCTIONS #################################
def add_missed_tickets(req, res=None):

    sid = int(req['sid'])
    number = int(req['number'])

    service = DBManager.get_row(obj=Service, id=sid)
    missed_tickets = stringlist_to_list(service['missed_tickets'])
    missed_tickets.append(number)
    DBManager.mod_row(obj=Service, id=sid, attr='missed_tickets', value=str(missed_tickets))

    res.send(json.dumps({'status':'OK'}).encode())

def dequeue_missed_tickets(sid:int):


    service = DBManager.get_row(obj=Service, id=sid)
    missed_tickets = stringlist_to_list(service['missed_tickets'])
    if missed_tickets == []:
        return None
    ticket = missed_tickets[0]
    missed_tickets = missed_tickets[1:]
    DBManager.mod_row(obj=Service, id=sid, attr='missed_tickets', value=str(missed_tickets))

    return ticket

def check_missed_tickets(req, res=None):

    sid = int(req['sid'])
    service = DBManager.get_row(obj=Service, id=sid)
    missed_tickets = stringlist_to_list(service['missed_tickets'])
    res.send(json.dumps({'missed_tickets':missed_tickets}).encode())