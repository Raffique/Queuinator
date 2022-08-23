
from database import DBManager
from models import *
import json
from .tickets import forward, reverse

def adjust(req, res=None, dispatch=None, server=None):
    print("activae adjust function ")

    # #Extract data from request payload 
    sid = req['sid']
    counter = req['counter']
    opt = req['opt']

    # #retreive Service from database and check if it is active
    # service = DBManager.get_row(obj=Service, id=sid)
    # if service['active'] == False:
    #     res.send(json.dumps({'response':'adjust', 'status': 'INVALID'}).encode())
    #     return

    #get current customer nuber and update it
    ticket, tickets = None, None
    

    if req['opt'] == '++':
        ticket, tickets = forward(req)
    elif req['opt'] == '--':
        ticket, tickets = reverse(req)
    elif req['opt'] == '=':
        pass

    print("ticket --> {} \n".format(ticket))
    print("tickets --> {}".format(tickets))

    if ticket == None:
        return

    #set up data for boradcasr from server
    server.broadcast(json.dumps({'response':'adjust', 'ticket': ticket, 'tickets':tickets, 'sid':sid, 'counter':counter, 'opt':opt}), res)
    
    #put req info in dispatch for screen update
    dispatch(req={'command':'adjust', 'number': ticket['number']})
    print("dispatch to screen")
