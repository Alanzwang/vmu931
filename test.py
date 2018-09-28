#!/usr/bin/env python3

import matplotlib.pyplot as plt
from pyvmu.vmu931 import VMU931Parser
from pyvmu import messages
import time
import csv

# We want to be able to update the plot in real-time, plt.ion() is non-blocking.
plt.ion()

figure = plt.figure()
acc_axes = figure.add_subplot(111)
acc_axes.set_title("Accelerometer")
acc_axes.set_xlabel("Timestamp (ms)")
acc_axes.set_ylabel("Force (g)")
acc_axes.set_ylim([-16, 16])  # -8 <= g <= 8

x_line, = acc_axes.plot([], [], label="X")
y_line, = acc_axes.plot([], [], label="Y")
z_line, = acc_axes.plot([], [], label="Z")

plt.legend()

ts_points = []
x_points = []
y_points = []
z_points = []

csv_points = [('Attribute', 'Time stamp', 'x', 'y', 'z')]

#with VMU931Parser(device = "COM3", accelerometer=True, quaternion=True) as vp:
with VMU931Parser(device = "COM3", accelerometer=True, ) as vp:

    vp.set_accelerometer_resolution(16)  # Set resolution of accelerometer to 8g.
    
    start_time = time.time() # Time capture started, in seconds
    seconds_to_capture = 30 
    while time.time() - start_time <= seconds_to_capture:
        pkt = vp.parse()

        if isinstance(pkt, messages.Status):
            print(pkt)

        if isinstance(pkt, messages.Accelerometer):
            ts, x, y, z = pkt
            ts_points.append(ts)
            x_points.append(x)
            y_points.append(y)
            z_points.append(z)
            
            csv_points.append(('Acceleration', ts, x, y, z))
            
#        if isinstance(pkt, messages.Quaternion):
#            ts, w, x, y, z = pkt
#            ts_points.append(ts)
#            x_points.append(x)
#            y_points.append(y)
#            z_points.append(z)
#            csv_points.append(('q', ts, w, x, y, z))
            
        # Only plot every 100 points (still quite smooth), otherwise we're bottle-necked by matplotlib.
        # Note that when angular data is not being streamed, the faster update rate is assumed.
        if len(ts_points) % 100 == 0:

            # set_data is faster than drawing a whole new line
            x_line.set_data(ts_points[-1000:], x_points[-1000:])
            y_line.set_data(ts_points[-1000:], y_points[-1000:])
            z_line.set_data(ts_points[-1000:], z_points[-1000:])

            acc_axes.relim()
            acc_axes.autoscale_view()
            figure.canvas.draw()

            # Pause to force redraw. Actually blocks until re-draw is complete, 0.00001 is an arbitrary small number.
            plt.pause(0.00001)

with open("Acceleration.csv", "w") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerows(csv_points)
    
    