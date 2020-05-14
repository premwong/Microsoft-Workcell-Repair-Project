# keep trying to connect to NUC
import bluetooth    

target_name = "workcell-NUC"
target_address = None

print("Looking for " + target_name)
nearby_devices = bluetooth.discover_devices(duration=20, lookup_names = True)

for pair in nearby_devices:
    print(pair)
    if target_name == pair[1]:
        target_address = pair[0]
        break

if target_address is not None:
    print("found target bluetooth device with address ", target_address)
    port = 1
    sock=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((target_address, port))
    sock.send("A")
    sock.close()
else:
    print("could not find target bluetooth device nearby")

