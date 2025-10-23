from pynput import keyboard
import tkinter as tk

from keys import key_pot,keys

last_key = "None"
head = 0

def on_press(key):
    global last_key, head
    try:
        last_key = key.char  # letter, number, symbol
    except AttributeError:
        last_key = str(key)  # special keys like shift, enter
        
    # Handle control keys immediately when pressed
    if last_key == "Key.ctrl":
        head -= 1
        if head < 0: head = 5
        print("ctrl left was pressed!")
        
    elif last_key == "Key.ctrl_r":
        head += 1
        head %= 6
        print("ctrl right was pressed!")

# Start keyboard listener
listener = keyboard.Listener(on_press=on_press)
listener.start()

# Tkinter window
root = tk.Tk()
root.title("Typing Pet 🐾")
root.geometry("250x100")
root.attributes("-topmost", True)
root.attributes("-alpha", 0.9)
root.resizable(False, False)

label = tk.Label(root, text="Press any key...", font=("Segoe UI", 12))
label.pack(expand=True)

def update_label():
    # label.config(text=f"Last key pressed: {last_key}")
    
    global head
            
    if last_key in key_pot:
        head = key_pot[last_key]
        label.config(text=f"{keys[head*5]} {keys[head*5 +1]} {keys[head*5 +2]} {keys[head*5+3]} {keys[head*5+4]}")
    else:
        # For control keys and other special keys, just show the current head
        label.config(text=f"{keys[head*5]} {keys[head*5 +1]} {keys[head*5 +2]} {keys[head*5+3]} {keys[head*5+4]}")
    root.after(100, update_label)

update_label()
root.mainloop()
