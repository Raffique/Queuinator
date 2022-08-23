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

    
def transfer(req, res=None, server=None):
    found_already = False

    transfer_ticket = req['transfer_ticket']
    trans_sid = transfer_ticket['trans_sid']
    init_sid = transfer_ticket['sid']
    counter = req['counter']

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
        sz = len(init_recycle_bin)
        if sz >= 1:
            for idx in range(1,sz+1):
                if init_recycle_bin[-idx]['number'] == transfer_ticket['number']:
                    init_recycle_bin.pop(-idx)
                    DBManager.mod_row(obj=Service, id=init_sid, attr='recycle_bin', value=json.dumps(init_recycle_bin))
                    found_already = True
                    break
                if idx >= 15:
                    break

    trans_service = DBManager.get_row(obj=Service, id=trans_sid)
    trans_tickets = json.loads(trans_service['tickets'])

    if trans_tickets == []:
        trans_tickets.append(transfer_ticket)
    else:
        insertaion = False
        for idx, t in enumerate(trans_tickets):
            if tm(transfer_ticket) < tm(t):
                trans_tickets.insert(idx, transfer_ticket)
                insertaion = True
                break
        if insertaion == False:
            trans_tickets.append(transfer_ticket)
        
    DBManager.mod_row(obj=Service, id=trans_sid, attr='tickets', value=json.dumps(trans_tickets))

    mssg = json.dumps({'response':'transfer', 'status':'OK', 'init_tickets':init_tickets, 'trans_tickets':trans_tickets, 'init_sid':init_sid, 'trans_sid':trans_sid, 'counter':counter})
    server.broadcast(mssg, res)
    

