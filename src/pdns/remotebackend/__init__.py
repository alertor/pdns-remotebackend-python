import json

VERSION="0.1"

class Handler:
    def __init__(self):
        self.log = []
        self.result = False
        self.ttl = 300
        self.params = {}

    def record_prio_ttl(self, qname, qtype, content, prio, ttl, auth=1):
        return {'qtype': qtype, 'qname': qname, 'content': content, 
                'ttl': ttl, 'auth': auth}
    
    def do_initialize(self, *args):
        self.params = args
        self.log.append("PowerDNS python remotebackend version {0} initialized".format(VERSION))
        self.result = True

    def do_lookup(self, args):
        pass

class Connector:
    def __init__(self, klass, options):
        self.handler = klass # initialize the handler class
        self.options = options

    def mainloop(self, reader, writer):
        h = self.handler()
        while(True):
            line = reader.readline()
            if line == "":
                break
            try:
                data_in = json.loads(line)
                method = "do_{0}".format(data_in['method'].lower())
                args = {}
                if ('parameters' in data_in):
                    args = data_in['parameters']
                h.result = False
                h.log = []
                if (callable(getattr(h, method, None))):
                    getattr(h,method)(args)
                writer.write(json.dumps({'result':h.result,'log':h.log}) + "\n")
            except ValueError:
                writer.write(json.dumps({'result':False,'log':"Cannot parse input"}) + "\n")
