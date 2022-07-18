
#----------------------------SINGLETON------------------------------->>>
def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance


#---------------------------OBSERVER-------------------------------->>>
class Subscriber:
    def __init__(self, name):
        self.name = name
    def update(self, req, res=None):
        print('{} got message "{}"'.format(self.name, req))
        
class Publisher:
    def __init__(self):
        self.subscribers = set()
    def register(self, who):
        self.subscribers.add(who)
    def unregister(self, who):
        self.subscribers.discard(who)
    def dispatch(self, req, res=None):
        for subscriber in self.subscribers:
            subscriber.update(req, res)