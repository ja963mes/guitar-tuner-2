from tkinter import *
from tkinter import ttk
import numpy as np
import dsp_processor
from main import detected_data


root = Tk()
window = Canvas(root, width = 400, height = 600)
window.pack()
canvas_height = 600
canvas_width = 400
smoothed_cents = 0.0

Cord_label = window.create_text(200, 50, text="Corde Value", font=("Arial", 24))
Hitz_label = window.create_text(200, 325, text="Hitz Value", font=("Arial", 24))
left_cents_value = window.create_text(20, 140, text="0", font=("Arial", 16))
target_value = window.create_text(200, 140, text="0.5", font=("Arial", 16))
right_cents_value = window.create_text(380, 140, text="1", font=("Arial", 16))



window.create_line(0, 100, 400, 100, fill="black")
needle = window.create_polygon(200, 200, 190, 450, 210, 450, fill="black", width=3)
window.create_arc(-50, 200, 450, 700, start=180, extent=-180, fill="", style=ARC, width=2)
window.create_oval(190, 440, 210, 460, fill="black")

window.itemconfig(Hitz_label, text="real time value of Hz")
window.itemconfig(target_value, text="0 cents") 
window.itemconfig(left_cents_value, text="-50")  
window.itemconfig(right_cents_value, text="+50")  

def read_latest_freq():
    global smoothed_cents
    
    freq = detected_data["frequency"]
    window.itemconfig(Hitz_label, text=f"{freq:.2f} Hz")
    
    note = detected_data["note"]
    target_cents = detected_data["cents_off"]

    if detected_data["note"] is None or detected_data["note"] == "":
        window.itemconfig(Cord_label, text="--")
        target_cents = 0.0
    else:
        window.itemconfig(Cord_label, text=f"{note}, {target_cents:.2f} cents")

    smoothing_factor = 0.1 
    
    # Calculate the new smoothed position
    smoothed_cents += (target_cents - smoothed_cents) * smoothing_factor

    angle = 270 + (smoothed_cents / 50) * 90
    theta = np.deg2rad(angle)
    
    # NEW GEOMETRY: Center pivot is (200, 450), Radius is 250.
    tip_x = 200 + 250 * np.cos(theta)
    tip_y = 450 + 250 * np.sin(theta)
    
    # Update the polygon with the new tip and the fixed base (y=450)
    window.coords(needle, tip_x, tip_y, 190, 450, 210, 450)

    # Schedule the next frame
    root.after(50, read_latest_freq)

read_latest_freq()
root.mainloop()


