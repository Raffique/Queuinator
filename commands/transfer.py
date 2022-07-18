from datetime import datetime, time
from server import Server
from design_patterns import Subscriber, Publisher
from database import DBManager
from models import *
import json
import re
from timewatch import timewatch as tw


def transfer(req, res=None):
    
    trans = req['trans']
    sid = req['sidc']
