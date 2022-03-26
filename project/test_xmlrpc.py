import sys
import urlib
from xmlrpc.server import SimpleXMLRPCServer

def get_next_pose(p):
    assert type(p) is dict
    pose = urlib.poseToList(p)
    print("Received pose: " + str(pose))
    pose = [-0.18, -0.61, 0.23, 0, 3.12, 0.04]
    return 5

server = SimpleXMLRPCServer(('localhost', 40404), allow_none=True)
server.RequestHandlerClass.protocol_version = "HTTP/1.1"
print("Listening on port 50000...")

server.register_function(get_next_pose, "get_next_pose")

server.serve_forever()