import tkinter as tk
from tkinter import messagebox
import snap7
from snap7.util import set_bool, get_bool
import time

PLC_IP = "192.168.0.1"
RACK = 0
SLOT = 1

# Using MB20 because MB0 and MB1 are already used in TIA
M_BYTE = 20

FORWARD_BIT = 0   # M20.0
RETRACT_BIT = 1   # M20.1

plc = snap7.client.Client()


def connect_plc():
    try:
        if plc.get_connected():
            status_label.config(text="PLC already connected")
            return

        plc.connect(PLC_IP, RACK, SLOT)

        if plc.get_connected():
            status_label.config(text="PLC connected")
            enable_control_buttons()
        else:
            status_label.config(text="PLC not connected")

    except Exception as e:
        messagebox.showerror("Connection Error", str(e))
        status_label.config(text="Connection failed")


def write_m_bits(forward=False, retract=False):
    try:
        if not plc.get_connected():
            messagebox.showwarning("PLC", "PLC is not connected")
            return

        # Read MB20
        data = plc.mb_read(M_BYTE, 1)

        # Write M20.0 and M20.1
        set_bool(data, 0, FORWARD_BIT, forward)
        set_bool(data, 0, RETRACT_BIT, retract)

        # Write back MB20
        plc.mb_write(M_BYTE, 1, data)

        # Read back for confirmation
        data_check = plc.mb_read(M_BYTE, 1)
        f_status = get_bool(data_check, 0, FORWARD_BIT)
        r_status = get_bool(data_check, 0, RETRACT_BIT)

        status_label.config(
            text=f"M20.0 Forward={f_status}, M20.1 Retract={r_status}"
        )

    except Exception as e:
        messagebox.showerror("PLC Write Error", str(e))


def forward_command():
    # Forward ON, Retract OFF
    write_m_bits(forward=True, retract=False)


def retract_command():
    # Retract ON, Forward OFF
    write_m_bits(forward=False, retract=True)


def stop_command():
    # Both commands OFF
    write_m_bits(forward=False, retract=False)


def disconnect_plc():
    try:
        if plc.get_connected():
            stop_command()
            time.sleep(0.1)
            plc.disconnect()

        status_label.config(text="PLC disconnected")
        disable_control_buttons()

    except Exception as e:
        messagebox.showerror("Disconnect Error", str(e))


def enable_control_buttons():
    forward_button.config(state="normal")
    retract_button.config(state="normal")
    stop_button.config(state="normal")
    disconnect_button.config(state="normal")


def disable_control_buttons():
    forward_button.config(state="disabled")
    retract_button.config(state="disabled")
    stop_button.config(state="disabled")
    disconnect_button.config(state="disabled")


root = tk.Tk()
root.title("Pneumatic Cylinder Control")
root.geometry("420x300")

connect_button = tk.Button(
    root,
    text="Connect PLC",
    width=25,
    command=connect_plc
)
connect_button.pack(pady=10)

forward_button = tk.Button(
    root,
    text="Forward",
    width=25,
    height=2,
    command=forward_command
)
forward_button.pack(pady=5)

retract_button = tk.Button(
    root,
    text="Retract",
    width=25,
    height=2,
    command=retract_command
)
retract_button.pack(pady=5)

stop_button = tk.Button(
    root,
    text="Stop",
    width=25,
    height=2,
    command=stop_command
)
stop_button.pack(pady=5)

disconnect_button = tk.Button(
    root,
    text="Disconnect",
    width=25,
    command=disconnect_plc
)
disconnect_button.pack(pady=10)

status_label = tk.Label(root, text="PLC not connected")
status_label.pack(pady=10)

disable_control_buttons()

root.protocol("WM_DELETE_WINDOW", disconnect_plc)

root.mainloop()