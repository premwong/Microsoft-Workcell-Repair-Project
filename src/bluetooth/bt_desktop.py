from bluetooth import *
import sys

# search for the SampleServer service
uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
print("Looking for uuid: " + str(uuid))
service_matches = find_service(uuid = uuid, address = None)

if len(service_matches) == 0:
    print("couldn't find the service =(")
    sys.exit(0)

first_match = service_matches[0]
port = first_match["port"]
name = first_match["name"]
host = first_match["host"]

print("connecting to \"%s\" on %s" % (name, host))

# Create the client socket
sock=BluetoothSocket(RFCOMM )
sock.connect((host, port))

send_state = True

print("Connected! Type 'start' to tell the workcell to go:")
while True:
    if send_state:
        data = input()
        if len(data) == 0: break
        sock.send(data)
        if data == "start":
            send_state = False
    else:
        data = sock.recv(1024)
        print("received [%s]" % data)
        if data == "done":
            send_state = True
            print("Work cell is done, ready for next server. Type 'start' when ready:")

sock.close()