# pyhton3
from tkinter import *
from datetime import datetime
import threading
import time
from tello import Tello
import sys
config = {
    "dest_ip": "192.168.10.1",
    "dest_port": 8889,
}
d = '20'
a = '1'

# tello = Tello(config=config)

tello = Tello()


# Init GUI
root = Tk()
root.geometry("800x450+100+50")
root.title('Tello Drone Control')

frame0 = Frame(root, width=800, height=10)
frame_scale = Frame(root)

frame12 = Frame(root)
frame1 = Frame(frame12)
frame2 = Frame(frame12)

frame_flip = Frame(root)

button_command = Button(frame0, text='command', width=10, command=lambda: tello.send_command(
    'command')).grid(row=0, column=0, padx=90, pady=10)
button_takeoff = Button(frame0, text='takeoff', width=10, command=lambda: tello.send_command(
    'takeoff')).grid(row=0, column=1, padx=90, pady=10)
button_land = Button(frame0, text='land', width=10, command=lambda: tello.send_command(
    'land')).grid(row=0, column=2, padx=90, pady=10)


button_follow_auto_sweep = Button(
    frame0, text='Follow Sweep', width=10, command=lambda: threading.Thread(target=tello.sweep).start()).grid(row=1, column=0, padx=90, pady=10)
button_take_over = Button(
    frame0, text='Take Over', width=10, command=lambda: threading.Thread(target=tello.start_manual_control).start()).grid(row=1, column=1, padx=90, pady=10)
button_continue_sweep = Button(
    frame0, text='Continue sweep', width=10, command=lambda: threading.Thread(target=tello.continue_sweep).start()).grid(row=1, column=2, padx=90, pady=10)

stream_on = Button(
    frame0, text='Stream ON', width=10, command=lambda: threading.Thread(target=tello.streamon).start()).grid(row=3, column=0, padx=90, pady=10)
stream_off = Button(
    frame0, text='Stream OFF', width=10, command=lambda: threading.Thread(target=tello.streamoff).start()).grid(row=3, column=1, padx=90, pady=10)
print_stats = Button(
    frame0, text='Print Stats', width=10, command=lambda: threading.Thread(target=tello.printStats).start()).grid(row=3, column=2, padx=90, pady=10)

# buttons to control flying forward, back, left and right
button_forward = Button(frame1, text='forward', height=1, width=8,
                        command=lambda: tello.send_command('forward '+d)).grid(row=0, column=1)
button_back = Button(frame1, text='back', height=1, width=8,
                     command=lambda: tello.send_command('back '+d)).grid(row=2, column=1)
button_left = Button(frame1, text='left', height=1, width=8,
                     command=lambda: tello.send_command('left '+d)).grid(row=1, column=0)
button_right = Button(frame1, text='right', height=1, width=8,
                      command=lambda: tello.send_command('right '+d)).grid(row=1, column=2)


# buttons to control flying up, down, spin left and spin right
button_up = Button(frame2, text='up', height=1, width=8,
                   command=lambda: tello.send_command('up '+d)).grid(row=0, column=1)
button_down = Button(frame2, text='down', height=1, width=8,
                     command=lambda: tello.send_command('down '+d)).grid(row=2, column=1)
button_spinleft = Button(frame2, text='spin left', height=1, width=8,
                         command=lambda: tello.send_command('cw '+a)).grid(row=1, column=0)
button_spinright = Button(frame2, text='spin right', height=1, width=8,
                          command=lambda: tello.send_command('ccw '+a)).grid(row=1, column=2)

# buttons to control flipping forward, back, left and right
button_flip_f = Button(frame_flip, text='flip forward', height=1, width=10,
                       command=lambda: tello.send_command('flip f')).grid(row=0, column=1)
button_flip_b = Button(frame_flip, text='flip back', height=1, width=10,
                       command=lambda: tello.send_command('flip b')).grid(row=2, column=1)
button_flip_l = Button(frame_flip, text='flip left', height=1, width=10,
                       command=lambda: tello.send_command('flip l')).grid(row=1, column=0)
button_flip_r = Button(frame_flip, text='flip right', height=1, width=10,
                       command=lambda: tello.send_command('flip r')).grid(row=1, column=2)

# scrollbar to set the angle to rotate
angle_slider = Scale(frame_scale, from_=1, to=360,
                     orient=HORIZONTAL, tickinterval=60, resolution=1, length=200)
angle_slider.grid(row=0, column=1, padx=95)


def angle_change():
    global a
    a = str(angle_slider.get())
    print(f"angel set to {a}")


def speed_change():
    global d
    d = str(distance_change.get())
    print(f"distance set to {d}")


angle = Button(frame_scale, text='angle confirm', padx=4, command=angle_change)
angle.grid(row=1, column=1)

# scrollbar to set the distance to fly
distance_change = Scale(frame_scale, from_=20, to=500,
                        orient=HORIZONTAL, tickinterval=100, resolution=10, length=200)
distance_change.grid(row=0, column=0, padx=95)

distance = Button(frame_scale, text='distance confirm',
                  padx=4, command=speed_change)
distance.grid(row=1, column=0)


frame0.pack()
frame_scale.pack(pady=20)
frame1.grid(row=0, column=0, padx=80)
frame2.grid(row=0, column=1, padx=80)
frame12.pack(pady=0)
frame_flip.pack(pady=30)

mainloop()
