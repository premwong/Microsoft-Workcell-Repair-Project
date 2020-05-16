#!/usr/bin/env python
# based off: https://github.com/pybluez/pybluez/tree/master/examples/simple

# This node connects to a desktop via bluetooth
# publishes to bl_ready: to let the workcell know that server is ready to go
# subscribes to conveyor_done: to let the desktop know that the server has been repaired and is ready to go

import rospy
from iiwa_msgs.srv import BluetoothFlag
from bluetooth import *

receive_state = True
server_sock = None

def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("conveyor_done", String, callback)
    rospy.spin()

def callback(data):
    if data == "done":
        server_sock.send(data)
        receive_state = True
        print("Waiting for next server.")

def setup_bluetooth():
    server_sock=BluetoothSocket( RFCOMM )
    server_sock.bind(("",PORT_ANY))
    server_sock.listen(1)
    port = server_sock.getsockname()[1]
    uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
    advertise_service(server_sock, "Command_Server",
                service_id = uuid,
                service_classes = [ uuid, SERIAL_PORT_CLASS ],
                profiles = [ SERIAL_PORT_PROFILE ], 
                    )
    print("Waiting for connection on RFCOMM channel %d" % port)

    client_sock, client_info = server_sock.accept()
    print("Accepted connection from ", client_info)


if __name__ == "__main__":
    rospy.init_node('bt_node', anonymous=True)
    pub = rospy.Publisher('bl_ready', BluetoothFlag, queue_size=10)
    rate = rospy.Rate(10)

    setup_bluetooth()

    try:
        while not rospy.is_shutdown():
            if receive_state:
                data = client_sock.recv(1024)
                if len(data) == 0: 
                    break
                else:
                    print("received [%s]" % data)
                    if (data == "start"):
                        pub.publish(data)
                        receive_state = False
            else:
                listener()

            rate.sleep()
    except IOError:
        print("IOError.")

    finally:        
        print("Disconnected.")
        client_sock.close()
        server_sock.close()
    