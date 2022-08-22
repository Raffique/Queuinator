from datetime import datetime, time
from commands.adjust import adjust
from server import Server
from design_patterns import Subscriber, Publisher
from database import DBManager
from models import *
import json
import re
from timewatch import timewatch as tw

def isEmail(email):

    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
 
    if(re.fullmatch(regex, email)):
        return True
 
    return False

def sign_in(req, res=None):

    user = req['user']
    password = req['password']

    user_data = None
    if isEmail(user):
        print('use email')
        user_data = DBManager.get_row(obj=User, email=user)
    else:
        print('use alias')
        user_data = DBManager.get_row(obj=User, alias=user)

    if user_data == None:
        res.send(json.dumps({'response':'sign_in', 'status':'INVALID', 'message': 'user doesnt exist'}).encode())
        return

    if password != user_data['password']:
        res.send(json.dumps({'response':'sign_in', 'status':'INVALID', 'message': 'invalid credentials'}).encode())
        return

    del user_data['date']

    #s1,s2,s3,s4,s5 = user_data['service1'],user_data['service2'],user_data['service3'],user_data['service4'],user_data['service5']
    active_services = DBManager.get_row(obj=Service, all=True)
    services = []
    multi_tickets = {
        'service1':None,
        'service2':None,
        'service3':None,
        'service4':None,
        'service5':None
    }

    multi_missed_tickets = {
        'service1':None,
        'service2':None,
        'service3':None,
        'service4':None,
        'service5':None
    }

    for m in range(len(active_services)):

        services.append({
            'id':active_services[m]['id'],
            'name':active_services[m]['name'],
            'sector':active_services[m]['sector'],
            'active':active_services[m]['active']
        })

        if user_data['service1'] == active_services[m]['id']:
            user_data['service1'] = {
                'id':active_services[m]['id'], 
                'name':active_services[m]['name'], 
                'sector':active_services[m]['sector']
            }
            multi_tickets['service1'] = json.loads(active_services[m]['tickets'])
            multi_missed_tickets['service1'] = json.loads(active_services[m]['missed_tickets'])
        
        if user_data['service2'] == active_services[m]['id']:
            user_data['service2'] = {
                'id':active_services[m]['id'], 
                'name':active_services[m]['name'], 
                'sector':active_services[m]['sector']
            }
            multi_tickets['service2'] = json.loads(active_services[m]['tickets'])
            multi_missed_tickets['service2'] = json.loads(active_services[m]['missed_tickets'])

        if user_data['service3'] == active_services[m]['id']:
            user_data['service3'] = {
                'id':active_services[m]['id'], 
                'name':active_services[m]['name'], 
                'sector':active_services[m]['sector']
            }
            multi_tickets['service3'] = json.loads(active_services[m]['tickets'])
            multi_missed_tickets['service3'] = json.loads(active_services[m]['missed_tickets'])

        if user_data['service4'] == active_services[m]['id']:
            user_data['service4'] = {
                'id':active_services[m]['id'], 
                'name':active_services[m]['name'], 
                'sector':active_services[m]['sector']
            }
            multi_tickets['service4'] = json.loads(active_services[m]['tickets'])
            multi_missed_tickets['service4'] = json.loads(active_services[m]['missed_tickets'])

        if user_data['service5'] == active_services[m]['id']:
            user_data['service5'] = {
                'id':active_services[m]['id'], 
                'name':active_services[m]['name'], 
                'sector':active_services[m]['sector']
            }
            multi_tickets['service5'] = json.loads(active_services[m]['tickets'])
            multi_missed_tickets['service5'] = json.loads(active_services[m]['missed_tickets'])

    mssg = json.dumps({
        'response':'sign_in',
        'status':'OK',
        'user':user_data,
        'multi_tickets':multi_tickets,
        'multi_missed_tickets':multi_missed_tickets,
        'services':services  
    })

    res.send(mssg.encode())