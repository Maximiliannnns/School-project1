from xmlrpc.server import SimpleXMLRPCServer

class myObject():
    def __init__(self, host, port):

        self.Server = SimpleXMLRPCServer((host, port), allow_one=True)

        self.Server.register_function(myFunction, "myFunction")

    def myFunction(self, argument1, argument2):
        return argument1 + argument2


if __name__ == "__main__":
    ObjectWithServer = myObject('localhost', 4040)
    
    print(ObjectWithServer.myFunction(10, 20))

    ObjectWithServer.Server.serve_forever()