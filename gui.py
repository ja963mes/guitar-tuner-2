from tkinter import *
from tkinter import ttk
import dsp_processor
from main import detected_data


root = Tk()
window = Canvas(root, width = 400, height = 600)
window.pack()
canvas_height = 600
canvas_width = 400

Cord_label = window.create_text(200, 50, text="Corde Value", font=("Arial", 24))
Hitz_label = window.create_text(200, 325, text="Hitz Value", font=("Arial", 24))
left_cents_value = window.create_text(20, 140, text="0", font=("Arial", 16))
target_value = window.create_text(200, 140, text="0.5", font=("Arial", 16))
right_cents_value = window.create_text(380, 140, text="1", font=("Arial", 16))



window.create_line(0, 100, 400, 100, fill="black")
window.create_polygon(200, 150, 190, 500, 210, 500, fill="black", width=3)
window.create_arc(20, 150, 380, 230, start=180, extent=-180, fill="", style=ARC, width=2)
window.create_oval(190, 490, 210, 510, fill="black")

window.itemconfig(Hitz_label, text="real time value of Hz")
window.itemconfig(target_value, text="0 cents") 
window.itemconfig(left_cents_value, text="-50")  
window.itemconfig(right_cents_value, text="+50")  

def read_latest_freq():
    freq = detected_data["frequency"]
    window.itemconfig(Hitz_label, text=f"{freq:.2f} Hz")
    note = detected_data["note"]
    cents_off = detected_data["cents_off"]
    if detected_data["note"] is None or detected_data["note"] == "":
        window.itemconfig(Cord_label, text="--")
    else:
        window.itemconfig(Cord_label, text=f"{note}, {cents_off:.2f} cents")

    root.after(50, read_latest_freq)


read_latest_freq()
root.mainloop()


