"""
alembic init migrations

In alembic.ini file change sqlalchemy.url = "" to the url of your database eg. sqlite:///data.sqlite

change target_metadata = None to target_metadata = Base.metadata, also from models import Base before

alembic revision --autogenerate -m "message"

alembic upgrade heads
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models import *


class DBManager:

    session = sessionmaker(bind=create_engine('sqlite:///data.sqlite'))
    session = scoped_session(session) #making use of session safe in threading

    #kwargs --> obj=Table in database, id|email|name=value, attr=column, value=value
    def mod_row(**kwargs):

        with DBManager.session() as s:
            row = None
            for key, value in kwargs.items():
                if key == 'id':
                    s.query(kwargs['obj']).filter(kwargs['obj'].id==kwargs['id']).update({kwargs['attr']: kwargs['value']})
                elif key == 'email':
                    s.query(kwargs['obj']).filter(kwargs['obj'].emai==kwargs['email']).update({kwargs['attr']: kwargs['value']})
                elif key == 'name':
                    s.query(kwargs['obj']).filter(kwargs['obj'].name==kwargs['name']).update({kwargs['attr']: kwargs['value']})
            s.commit()

    def add_row(obj):
        with DBManager.session() as s:
            s.add(obj)
            s.commit()

    def del_row(obj, id):
        with DBManager.session() as s:
            row = s.query(obj).filter_by(id=id).first()
            s.delete(row)
            s.commit()

    #kwargs --> obj=table from database, id|email|name=..., all=True
    def get_row(**kwargs):

        def usermapper(obj):
            x = {
                'id': obj.id,
                'anonymous': obj.anonymous,
                'email': obj.email,
                'alias': obj.alias,
                'fname': obj.fname,
                'lname': obj.lname,
                'password': obj.password,
                'counter': obj.counter,
                'date': obj.date,
                'calls': obj.calls,
                'service1': obj.service1,
                'service2': obj.service2,
                'service3': obj.service3,
                'service4': obj.service4,
                'service5': obj.service5,
            }

            return x

        def servicemapper(obj):
            x = {
                'id': obj.id,
                'name': obj.name,
                'sector': obj.sector,
                'type': obj.type,
                'limit': obj.limit,
                'active': obj.active,
                'number': obj.number,
                'created': obj.created,
                'last': obj.last,
                'tickets': obj.tickets,
                'missed_tickets': obj.missed_tickets,
                'last_dispensed_ticket': obj.last_dispensed_ticket,

                'sub1': obj.sub1,
                'sub2': obj.sub2,
                'sub3': obj.sub3,
                'sub4': obj.sub4,
                'sub5': obj.sub5,
                'sub6': obj.sub6,
                'sub7': obj.sub7,
                'sub8': obj.sub8,
                'sub9': obj.sub9,
                'sub10': obj.sub10,

            }

            return x

        def chainmapper(obj):
            x = {
                'id': obj.id,
                'name': obj.name,
                'active': obj.active,

                's1': obj.s1,
                's2': obj.s2,
                's3': obj.s3,
                's4': obj.s4,
                's5': obj.s5,
                's6': obj.s6,
                's7': obj.s7,
                's8': obj.s8,
                's9': obj.s9,
                's10': obj.s10,
            }

            return x

        def historymapper(obj):
            x = {
                'id': obj.id,
                'serviceid': obj.serviceid,
                'servicename': obj.servicename,
                'userid': obj.userid,
                'username': obj.username,
                'customer': obj.customer,
                'date': obj.date,
                'wait': obj.wait,
            }

            return x

        records = None
        with DBManager.session() as s:

            for key, value in kwargs.items():
                if key == 'id':
                    records = s.query(kwargs['obj']).filter_by(id=kwargs['id']).first()
                elif key == 'email':
                    records = s.query(kwargs['obj']).filter_by(email=kwargs['email']).first()
                elif key == 'alias':
                    records = s.query(kwargs['obj']).filter_by(alias=kwargs['alias']).first()
                elif key == 'active':
                    records = s.query(kwargs['obj']).filter_by(active=kwargs['active'])

        if records == None:
            return None

        if kwargs['obj'] == Service:
            if 'active' in kwargs.keys():
                records = [servicemapper(x) for x in records]
            else:
                records = servicemapper(records)
        elif kwargs['obj'] == User:
            records = usermapper(records)
        elif kwargs['obj'] == Chain:
            records = chainmapper(records)
        elif kwargs['obj'] == History:
            records = historymapper(records)

        return records
        
if __name__ == "__main__":

    service = [Service(name='Senior Citizens', sector='B', )]
    user = [User(email='jermainedavis@gmail.com', fname='jermaine', lname='davis', alias='jay', password='xyz123', counter=7, service1=1)]
    history = History(
                serviceid=1,
                servicename="Customer Care",
                userid=1,
                username='',
                number=22,
            )
    #DBManager.add_row(service[0])
    #DBManager.add_row(user[0])
    #DBManager.add_row(history)
    #DBManager.mod_row(obj=User, id=1, attr='service1', value=None)
    #DBManager.del_row(History, 1)
    #a = DBManager.get_row(obj=User, id=1)
    services = DBManager.get_row(obj=Service, active=True)
    print(services)