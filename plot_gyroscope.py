#!/usr/bin/env python3

import matplotlib.pyplot as plt
from pyvmu.vmu931 import VMU931Parser
from pyvmu import messages
import time
import csv

# We want to be able to update the plot in real-time, plt.ion() is non-blocking.
plt.ion()

figure = plt.figure()
gyro_axes = figure.add_subplot(111)
gyro_axes.set_title("Gyroscope")
gyro_axes.set_xlabel("Timestamp (ms)")
gyro_axes.set_ylabel("Velocity (°/s)")

x_line, = gyro_axes.plot([], [], label="X")
y_line, = gyro_axes.plot([], [], label="Y")
z_line, = gyro_axes.plot([], [], label="Z")

plt.legend()

ts_points = []
x_points = []
y_points = []
z_points = []

csv_points = [('Attribute', 'Time stamp', 'x', 'y', 'z')]

with VMU931Parser(device = "COM3", gyroscope=True) as vp:

    start_time = time.time() # Time capture started, in seconds
    seconds_to_capture = 30 
    while time.time() - start_time <= seconds_to_capture:
        pkt = vp.parse()

        if isinstance(pkt, messages.Status):
            print(pkt)

        if isinstance(pkt, messages.Gyroscope):
            ts, x, y, z = pkt
            ts_points.append(ts)
            x_points.append(x)
            y_points.append(y)
            z_points.append(z)
            
            csv_points.append(('Gyroscope', ts, x, y, z))

        # Only plot every 10 points (still quite smooth), otherwise we risk being bottle-necked by matplotlib.
        if len(ts_points) % 100 == 0:
            # set_data is faster than drawing a whole new line
            x_line.set_data(ts_points[-1000:], x_points[-1000:])
            y_line.set_data(ts_points[-1000:], y_points[-1000:])
            z_line.set_data(ts_points[-1000:], z_points[-1000:])

            gyro_axes.relim()
            gyro_axes.autoscale_view()
            figure.canvas.draw()

            # Pause to force redraw. Actually blocks until re-draw is complete, 0.00001 is an arbitrary small number.
            plt.pause(0.00001)

with open("Gyroscope.csv", "w") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerows(csv_points)