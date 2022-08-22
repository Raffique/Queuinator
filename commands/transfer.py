from datetime import datetime, time
from pickle import FALSE
from server import Server
from design_patterns import Subscriber, Publisher
from database import DBManager
from models import *
import json
import re
from timewatch import timewatch as tw
from ticketMaker import TicketMaker as tm



def transfer_req(req, res=None):
    services = DBManager.get_row(obj=Service, active=True)
    tickets = []

    for m in range(len(services)):
        if req['sid'] == services[m]['id']:
            tickets = json.loads(services[m]['tickets'])
            del services[m]['created']
            del services[m]['last']

        else:
            del services[m]['created']
            del services[m]['last']

    mssg = json.dumps({'response':'transfer_req', 'services':services, 'tickets':tickets})
    try:
        res.send(mssg.encode())
    except Exception as e:
        print(e)
    
    
def transfer_update(req, res=None):
    print("transfer update has reached be proud of yourself young lad its never an easy road")
    found_already = False

    transfer_ticket = req['transfer_ticket']
    trans_sid = transfer_ticket['trans_sid']
    init_sid = transfer_ticket['sid']

    init_service = DBManager.get_row(obj=Service, id=init_sid)
    init_tickets = json.loads(init_service['tickets'])
    init_recycle_bin = json.loads(init_service['recycle_bin'])

    for idx, t in enumerate(init_tickets):
        if t['number'] == transfer_ticket['number']:
            init_tickets.pop(idx)
            DBManager.mod_row(obj=Service, id=init_sid, attr='tickets', value=json.dumps(init_tickets))
            found_already =True
            break

    if found_already == False:
        print("looking in recycle  bin")
        sz = len(init_recycle_bin)
        if sz >= 1:
            for idx in range(1,sz+1):
                if init_recycle_bin[-idx]['number'] == transfer_ticket['number']:
                    print("found ticket in bin")
                    init_recycle_bin.pop(-idx)
                    DBManager.mod_row(obj=Service, id=init_sid, attr='recycle_bin', value=json.dumps(init_recycle_bin))
                    found_already = True
                    break
                if idx >= 15:
                    break

    trans_service = DBManager.get_row(obj=Service, id=trans_sid)
    trans_tickets = json.loads(trans_service['tickets'])

    if trans_tickets == []:
        print("[placed ticket into empty queue")
        trans_tickets.append(transfer_ticket)
    else:
        insertaion = False
        for idx, t in enumerate(trans_tickets):
            if tm(transfer_ticket) < tm(t):
                trans_tickets.insert(idx, transfer_ticket)
                print("place ticket into correct time slot")
                insertaion = True
                break
        if insertaion == False:
            trans_tickets.append(transfer_ticket)
        
    DBManager.mod_row(obj=Service, id=trans_sid, attr='tickets', value=json.dumps(trans_tickets))

    mssg = json.dumps({'response':'transfer_update', 'success':'ok'})
    try:
        res.send(mssg.encode())
    except Exception as e:
        print(e)
    

