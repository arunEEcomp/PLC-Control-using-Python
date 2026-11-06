import snap7

ips = ["192.168.0.1", "192.168.0.2"]

for ip in ips:
    for slot in [1, 2]:
        plc = snap7.client.Client()
        try:
            plc.connect(ip, 0, slot)
            if plc.get_connected():
                print(f"Connected: IP={ip}, Rack=0, Slot={slot}")
                plc.disconnect()
            else:
                print(f"Not connected: IP={ip}, Rack=0, Slot={slot}")
        except Exception as e:
            print(f"Failed: IP={ip}, Rack=0, Slot={slot}, Error={e}")