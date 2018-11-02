# Echo server program for both IPv4 and IPv6
# From https://docs.python.org/2.4/lib/socket-example.html
import socket
import sys

HOST = None  # Symbolic name meaning the local host
PORT = 4000  # Arbitrary non-privileged port
s = None
try:
    for res in socket.getaddrinfo(HOST, PORT, socket.AF_INET6, socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
        af, socktype, proto, canonname, sa = res
        try:
            s = socket.socket(af, socktype, proto)
        except socket.error as e:
            print("socket.socket failed\n"+str(e), file=sys.stderr)
            s = None
            continue
        try:
            s.bind(sa)
            print("Listening on socket", file=sys.stderr)
            s.listen(1)
            print("Done listening on socket", file=sys.stderr)
        except socket.error as e:
            print("Failed to bind\n"+str(e), file=sys.stderr)
            s.close()
            s = None
            continue
        break
except socket.gaierror as s:
    print("socket.getaddrinfo raised socket.gaierror exception.  Host is "+
          HOST )
    sys.exit(1)
if s is None:
    print('could not open socket', file=sys.stderr)
    sys.exit(1)
while True:
    print("Waiting to accept a connection", file=sys.stderr)
    conn, addr = s.accept()
    print('Connected by address: '+str(addr)+", conn is "+str(conn), file=sys.stderr)
    while True:
        try:
            data = conn.recv(100)
        except OSError as e:
            print("conn.recv raised OSError. Closing connection\n"+str(e))
            data = False
        if not data:
            print("Closing connection "+str(conn), file=sys.stderr)
            conn.close()
            print("Closed connection " + str(conn), file=sys.stderr)
            break
