import snap7

PLC_IP = "192.168.0.1"
RACK = 0
SLOT = 1

plc = snap7.client.Client()
plc.connect(PLC_IP, RACK, SLOT)

print("Connected:", plc.get_connected())

cpu_state = plc.get_cpu_state()
print("CPU State:", cpu_state)

plc.disconnect()