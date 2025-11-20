#!/usr/bin/env python3
import threading
import time
import struct
import sys
from typing import List, Optional, Tuple

try:
    import tkinter as tk
    from tkinter import ttk, messagebox
except Exception as e:
    print("Tkinter is required to run this UI:", e)
    sys.exit(1)

try:
    import serial
    from serial.tools import list_ports
except Exception as e:
    print("pyserial is required: pip install pyserial\n", e)
    sys.exit(1)


MSG_START = 0xAA
MSG_END = 0x55
MSG_CMD_ARRAY = 0x10
MSG_ODOM = 0x02
MSG_STATUS = 0x03
MSG_ESTOP = 0x04


def clamp_i8(v: int) -> int:
    return max(-127, min(127, int(v)))


class SerialBridge:
    def __init__(self):
        self.ser: Optional[serial.Serial] = None
        self.rx_thread: Optional[threading.Thread] = None
        self.stop_event = threading.Event()
        self.on_odom = None  # type: Optional[callable]
        self.on_status = None  # type: Optional[callable]
        self.lock = threading.Lock()

    def open(self, port: str, baud: int = 115200):
        self.close()
        self.stop_event.clear()
        self.ser = serial.Serial(port, baudrate=baud, timeout=0.05)
        self.rx_thread = threading.Thread(target=self._rx_loop, daemon=True)
        self.rx_thread.start()

    def close(self):
        self.stop_event.set()
        if self.rx_thread and self.rx_thread.is_alive():
            self.rx_thread.join(timeout=0.5)
        if self.ser:
            try:
                self.ser.close()
            except Exception:
                pass
        self.ser = None
        self.rx_thread = None

    def send_array(self, data9: List[int]):
        if not self.ser:
            return
        if len(data9) != 9:
            raise ValueError("data9 must be length 9")
        # convert to signed int8 bytes
        payload = bytes(((x + 256) % 256 for x in map(clamp_i8, data9)))
        frame = bytes([MSG_START, MSG_CMD_ARRAY]) + payload + bytes([MSG_END])
        with self.lock:
            self.ser.write(frame)

    def send_estop(self):
        if not self.ser:
            return
        # Arduino expects [START][TYPE] only for ESTOP; keep minimal
        frame = bytes([MSG_START, MSG_ESTOP])
        with self.lock:
            self.ser.write(frame)

    def _rx_loop(self):
        buf = bytearray()
        while not self.stop_event.is_set():
            try:
                if not self.ser:
                    time.sleep(0.05)
                    continue
                chunk = self.ser.read(64)
                if not chunk:
                    continue
                buf.extend(chunk)
                # parse frames
                while True:
                    si = buf.find(bytes([MSG_START]))
                    if si < 0:
                        buf.clear()
                        break
                    if si > 0:
                        del buf[:si]
                    if len(buf) < 2:
                        break
                    t = buf[1]
                    need = None
                    if t == MSG_ODOM:
                        need = 1 + 1 + 20 + 1
                    elif t == MSG_STATUS:
                        need = 1 + 1 + 1 + 1
                    else:
                        # Unknown, drop one byte
                        del buf[0]
                        continue
                    if len(buf) < need:
                        break
                    frame = bytes(buf[:need])
                    if frame[-1] != MSG_END:
                        del buf[0]
                        continue
                    payload = frame[2:-1]
                    if t == MSG_ODOM and len(payload) == 20:
                        x, y, th, vx, vth = struct.unpack('<fffff', payload)
                        if self.on_odom:
                            self.on_odom(x, y, th, vx, vth)
                    elif t == MSG_STATUS and len(payload) == 1:
                        code = payload[0]
                        if self.on_status:
                            self.on_status(code)
                    del buf[:need]
            except Exception:
                time.sleep(0.05)


class RobotGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Robot Control GUI (9-byte array)")
        self.bridge = SerialBridge()
        self.bridge.on_odom = self._on_odom
        self.bridge.on_status = self._on_status

        # state
        self.connected = False
        self.data9 = [0] * 9
        self.last_odom: Optional[Tuple[float, float, float]] = None
        self._pressed_keys = set()

        # top bar
        top = ttk.Frame(root)
        top.pack(fill='x', padx=8, pady=8)
        ttk.Label(top, text="Port:").pack(side='left')
        self.port_var = tk.StringVar(value=self._default_port())
        self.port_combo = ttk.Combobox(top, textvariable=self.port_var, values=self._list_ports(), width=18)
        self.port_combo.pack(side='left', padx=4)
        ttk.Button(top, text="Refresh", command=self._refresh_ports).pack(side='left')
        ttk.Label(top, text="Baud:").pack(side='left', padx=(12, 2))
        self.baud_var = tk.IntVar(value=115200)
        ttk.Entry(top, textvariable=self.baud_var, width=8).pack(side='left')
        self.connect_btn = ttk.Button(top, text="Connect", command=self._toggle_connect)
        self.connect_btn.pack(side='left', padx=8)
        self.estop_btn = ttk.Button(top, text="EMERGENCY STOP", command=self._estop)
        self.estop_btn.pack(side='right')

        # tracks sliders
        mid = ttk.Frame(root)
        mid.pack(fill='x', padx=8, pady=8)
        self.left_var = tk.IntVar(value=0)
        self.right_var = tk.IntVar(value=0)
        left_frame = ttk.LabelFrame(mid, text="Left track")
        left_frame.pack(side='left', expand=True, fill='both', padx=6)
        self.left_scale = tk.Scale(left_frame, from_=127, to=-127, orient='vertical', variable=self.left_var, command=self._on_track_change)
        self.left_scale.pack(expand=True, fill='y')

        right_frame = ttk.LabelFrame(mid, text="Right track")
        right_frame.pack(side='left', expand=True, fill='both', padx=6)
        self.right_scale = tk.Scale(right_frame, from_=127, to=-127, orient='vertical', variable=self.right_var, command=self._on_track_change)
        self.right_scale.pack(expand=True, fill='y')

        buttons = ttk.Frame(mid)
        buttons.pack(side='left', fill='y', padx=8)
        ttk.Button(buttons, text="Stop All", command=self._stop_all).pack(fill='x', pady=4)

        # flippers/camera
        grp = ttk.LabelFrame(root, text="Flippers & Camera (momentary)")
        grp.pack(fill='x', padx=8, pady=8)
        # Rear flipper index 2
        self._add_momentary(grp, "Rear Down", idx=2, val=-127).grid(row=0, column=0, padx=4, pady=2)
        self._add_momentary(grp, "Rear Up", idx=2, val=+127).grid(row=0, column=1, padx=4, pady=2)
        # Front-right 3/4 separate channels
        self._add_momentary(grp, "FR Down", idx=3, val=+127).grid(row=1, column=0, padx=4, pady=2)
        self._add_momentary(grp, "FR Up", idx=4, val=+127).grid(row=1, column=1, padx=4, pady=2)
        # Front-left 5/6
        self._add_momentary(grp, "FL Down", idx=5, val=+127).grid(row=2, column=0, padx=4, pady=2)
        self._add_momentary(grp, "FL Up", idx=6, val=+127).grid(row=2, column=1, padx=4, pady=2)
        # Camera 7/8
        self._add_momentary(grp, "Cam Up", idx=7, val=+127).grid(row=3, column=0, padx=4, pady=2)
        self._add_momentary(grp, "Cam Down", idx=8, val=+127).grid(row=3, column=1, padx=4, pady=2)

        # status
        status = ttk.Frame(root)
        status.pack(fill='x', padx=8, pady=8)
        self.status_var = tk.StringVar(value="Disconnected")
        ttk.Label(status, textvariable=self.status_var).pack(side='left')
        self.odom_var = tk.StringVar(value="x=0.00 y=0.00 th=0.00")
        ttk.Label(status, textvariable=self.odom_var).pack(side='right')

        # keyboard control
        for ev in ("<KeyPress>", "<KeyRelease>"):
            root.bind(ev, self._on_key)

        # periodic sender
        self._tx_job()

    # UI helpers
    def _list_ports(self):
        try:
            return [p.device for p in list_ports.comports()]
        except Exception:
            return []

    def _default_port(self):
        ports = self._list_ports()
        return ports[0] if ports else "COM3"

    def _refresh_ports(self):
        self.port_combo["values"] = self._list_ports()

    def _toggle_connect(self):
        if not self.connected:
            try:
                self.bridge.open(self.port_var.get(), int(self.baud_var.get()))
                self.connected = True
                self.connect_btn.config(text="Disconnect")
                self.status_var.set(f"Connected to {self.port_var.get()} @ {self.baud_var.get()}")
            except Exception as e:
                messagebox.showerror("Serial", f"Failed to open: {e}")
        else:
            self.bridge.close()
            self.connected = False
            self.connect_btn.config(text="Connect")
            self.status_var.set("Disconnected")

    def _on_track_change(self, _evt=None):
        self.data9[0] = clamp_i8(self.left_var.get())
        self.data9[1] = clamp_i8(self.right_var.get())

    def _stop_all(self):
        self.left_var.set(0)
        self.right_var.set(0)
        for i in range(2, 9):
            self.data9[i] = 0
        self._on_track_change()

    def _estop(self):
        try:
            self.bridge.send_estop()
            self.status_var.set("ESTOP sent (release requires hardware)")
        except Exception as e:
            messagebox.showerror("E-STOP", str(e))

    def _add_momentary(self, parent, label, idx: int, val: int):
        btn = ttk.Button(parent, text=label)
        def on_press(_evt):
            self.data9[idx] = clamp_i8(val)
        def on_release(_evt):
            self.data9[idx] = 0
        btn.bind('<ButtonPress-1>', on_press)
        btn.bind('<ButtonRelease-1>', on_release)
        return btn

    # Keyboard: arrows for differential, space stop, E for estop
    def _on_key(self, event):
        if event.type == tk.EventType.KeyPress:
            self._pressed_keys.add(event.keysym)
        elif event.type == tk.EventType.KeyRelease:
            self._pressed_keys.discard(event.keysym)
        self._apply_keys()

    def _apply_keys(self):
        fwd = 'Up' in self._pressed_keys or 'w' in self._pressed_keys
        back = 'Down' in self._pressed_keys or 's' in self._pressed_keys
        left = 'Left' in self._pressed_keys or 'a' in self._pressed_keys
        right = 'Right' in self._pressed_keys or 'd' in self._pressed_keys
        stop = 'space' in self._pressed_keys
        if stop:
            self.left_var.set(0); self.right_var.set(0)
        else:
            lv = 0; rv = 0; mag = 90  # keyboard magnitude
            if fwd: lv += mag; rv += mag
            if back: lv -= mag; rv -= mag
            if left: lv -= mag; rv += mag
            if right: lv += mag; rv -= mag
            self.left_var.set(clamp_i8(lv))
            self.right_var.set(clamp_i8(rv))
        self._on_track_change()
        if 'e' in self._pressed_keys or 'E' in self._pressed_keys:
            self._estop()

    # Periodic TX at ~20 Hz
    def _tx_job(self):
        if self.connected:
            try:
                self.bridge.send_array(self.data9)
            except Exception:
                pass
        self.root.after(50, self._tx_job)

    # RX callbacks
    def _on_odom(self, x, y, th, vx, vth):
        def _upd():
            self.odom_var.set(f"x={x:.2f} y={y:.2f} th={th:.2f}")
        self.root.after(0, _upd)

    def _on_status(self, code: int):
        def _upd():
            txt = 'ESTOP' if code == 0x00 else f'STATUS_{code}'
            self.status_var.set(txt)
        self.root.after(0, _upd)


def main():
    root = tk.Tk()
    app = RobotGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
