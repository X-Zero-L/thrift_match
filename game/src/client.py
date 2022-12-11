#import sys
#import glob
#sys.path.append('gen-py')
#sys.path.insert(0, glob.glob('../../lib/py/build/lib*')[0])
from sys import stdin
from match_client.match import Match
from match_client.match.ttypes import User

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol


# 一个指令函数，向服务端发送指定信息
def operate(op,user_id,user_name,score):
    # Make socket
    transport = TSocket.TSocket('localhost', 9090)
    # Buffering is critical. Raw sockets are very slow
    transport = TTransport.TBufferedTransport(transport)
    # Wrap in a protocol
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    # Create a client to use the protocol encoder
    client = Match.Client(protocol)
    # Connect!
    transport.open()

    user = User(user_id, user_name, score)

    if op == "add":
        client.add_user(user, "")
    else:
        client.remove_user(user, "")
    
    # Close!
    transport.close()


def main():
    for line in stdin:
        op, user_id, user_name, score = line.split(' ')
        operate(op, int(user_id), user_name, int(score))

if __name__ == "__main__":
    main()