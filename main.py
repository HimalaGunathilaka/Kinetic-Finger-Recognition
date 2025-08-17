import serial
import serial.tools.list_ports
import time
import re
import tkinter as tk
import threading

from keys import keys  # Use your exact dictionary

def find_esp32_port():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if "USB" in port.description or "UART" in port.description:
            return port.device
    return None

def read_piezo_serial(update_fn):
    port = find_esp32_port()
    if not port:
        update_fn("ESP32 not found.")
        return

    print(f"Connecting to ESP32 on {port}...")
    ser = serial.Serial(port, 115200, timeout=1)
    time.sleep(2)

    try:
        while True:
            line = ser.readline().decode('utf-8').strip()
            if line:
                signal = ''.join(re.findall(r'\d+', line))
                if signal in keys:
                    update_fn(keys[signal])
                else:
                    print(f"Unknown signal: {signal}")
    except Exception as e:
        update_fn(f"Error: {e}")
    finally:
        ser.close()

# --- GUI Setup ---
def start_gui():
    root = tk.Tk()
    root.title("Piezo Input Typing")
    root.geometry("600x300")

    output_label = tk.Label(root, text="", font=("Consolas", 18), wraplength=580, justify="left", anchor="nw")
    output_label.pack(padx=10, pady=10, fill="both", expand=True)

    typed_text = []
    shift_next = [False]  # Use a list to keep it mutable in the inner scope

    def update_output(signal_word):
        if signal_word == "space":
            typed_text.append(" ")
        elif signal_word == "enter":
            typed_text.append("\n")
        elif signal_word == "backspace":
            if typed_text:
                typed_text.pop()
        elif signal_word == "shift":
            shift_next[0] = True
        else:
            char = signal_word.upper() if shift_next[0] else signal_word
            shift_next[0] = False  # Reset shift
            typed_text.append(char)

        output_label.config(text=''.join(typed_text))

    threading.Thread(target=read_piezo_serial, args=(update_output,), daemon=True).start()

    root.mainloop()

if __name__ == "__main__":
    start_gui()
