from datetime import datetime
from email.policy import default
from sqlalchemy import Boolean, Integer, String, DateTime, Time, ForeignKey, Column
from sqlalchemy.orm import relationship, declarative_base 

Base = declarative_base()

# Create your models here.

class Service(Base):
    __tablename__ = "service"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    sector = Column(String) #when there are multiple services, this is used to identify diffcd vim with alphanumeric numbers like A22 or D22 
    type = Column(Integer, default=0)
    limit = Column(Integer, default=999)
    active = Column(Boolean, default=True)
    number = Column(Integer, default=0)
    created = Column(DateTime, default=datetime.now)
    last = Column(DateTime, default=datetime.now)
    tickets = Column(String, default="[]")
    missed_tickets = Column(String, default="[]")
    last_dispensed_ticket = Column(Integer, nullable=True)

    sub1 = Column(String, default='')
    sub2 = Column(String, default='')
    sub3 = Column(String, default='')
    sub4 = Column(String, default='')
    sub5 = Column(String, default='')
    sub6 = Column(String, default='')
    sub7 = Column(String, default='')
    sub8 = Column(String, default='')
    sub9 = Column(String, default='')
    sub10 = Column(String, default='')

    #user = relationship('User', back_populates='service')
    #chain = relationship('Chain', back_populates='service')
    history = relationship('History', back_populates='service', uselist=False)

    


class Chain(Base):

    __tablename__ = "chain"

    id = Column(Integer, primary_key=True)
    name = Column(String, default='')
    active = Column(Boolean, default=True)

    s1 = Column(Integer, ForeignKey('service.id'), nullable=True)
    s2 = Column(Integer, ForeignKey('service.id'), nullable=True)
    s3 = Column(Integer, ForeignKey('service.id'), nullable=True)
    s4 = Column(Integer, ForeignKey('service.id'), nullable=True)
    s5 = Column(Integer, ForeignKey('service.id'), nullable=True)
    s6 = Column(Integer, ForeignKey('service.id'), nullable=True)
    s7 = Column(Integer, ForeignKey('service.id'), nullable=True)
    s8 = Column(Integer, ForeignKey('service.id'), nullable=True)
    s9 = Column(Integer, ForeignKey('service.id'), nullable=True)
    s10 = Column(Integer, ForeignKey('service.id'), nullable=True)

    #service = relationship('Service', foreign_keys=[s1,s2,s3,s4,s5,s6,s7,s8,s9,s10])
    sr1 = relationship('Service', foreign_keys='Chain.s1')
    sr2 = relationship('Service', foreign_keys='Chain.s2')
    sr3 = relationship('Service', foreign_keys='Chain.s3')
    sr4 = relationship('Service', foreign_keys='Chain.s4')
    sr5 = relationship('Service', foreign_keys='Chain.s5')
    sr6 = relationship('Service', foreign_keys='Chain.s6')
    sr7 = relationship('Service', foreign_keys='Chain.s7')
    sr8 = relationship('Service', foreign_keys='Chain.s8')
    sr9 = relationship('Service', foreign_keys='Chain.s9')
    sr10 = relationship('Service', foreign_keys='Chain.s10')






class User(Base):

    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    service1 = Column(Integer, ForeignKey('service.id'), nullable=True) #or can just be service id
    service2 = Column(Integer, ForeignKey('service.id'), nullable=True)
    service3 = Column(Integer, ForeignKey('service.id'), nullable=True)
    service4 = Column(Integer, ForeignKey('service.id'), nullable=True)
    service5 = Column(Integer, ForeignKey('service.id'), nullable=True)
    anonymous = Column(Boolean, default=False)
    email = Column(String, default='default@default.com')
    alias = Column(String, default='')
    fname = Column(String, default='')
    lname = Column(String, default='')
    password = Column(String, default='')
    counter = Column(Integer, default=-1)
    date = Column(DateTime, default=datetime.now)
    calls = Column(Integer, default=0)

    sr1 = relationship('Service', foreign_keys=[service1])
    sr2 = relationship('Service', foreign_keys=[service2])
    sr3 = relationship('Service', foreign_keys=[service3])
    sr4 = relationship('Service', foreign_keys=[service4])
    sr5 = relationship('Service', foreign_keys=[service5])

    history = relationship('History', back_populates='user', uselist=False)


class History(Base):

    __tablename__ = "history"

    id = Column(Integer, primary_key=True)
    serviceid = Column(Integer, ForeignKey('service.id'), nullable=True)
    servicename = Column(String, default = '')
    userid = Column(Integer, ForeignKey('user.id'), nullable=True)
    username = Column(String, default = '')
    number = Column(Integer, default=0)
    date = Column(DateTime, default=datetime.now)
    wait = Column(String, default="00:00:00")

    service = relationship('Service', back_populates='history', foreign_keys=[serviceid])
    user = relationship('User', back_populates='history', foreign_keys=[userid])