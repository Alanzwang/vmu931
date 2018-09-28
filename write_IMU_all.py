#!/usr/bin/env python3

#import matplotlib.pyplot as plt
from pyvmu.vmu931 import VMU931Parser
from pyvmu import messages
import time
import csv

# We want to be able to update the plot in real-time, plt.ion() is non-blocking.
#plt.ion()
#
#figure = plt.figure()
#acc_axes = figure.add_subplot(111)
#acc_axes.set_title("Accelerometer")
#acc_axes.set_xlabel("Timestamp (ms)")
#acc_axes.set_ylabel("Force (g)")
#acc_axes.set_ylim([-16, 16])  # -8 <= g <= 8
#
#x_line, = acc_axes.plot([], [], label="X")
#y_line, = acc_axes.plot([], [], label="Y")
#z_line, = acc_axes.plot([], [], label="Z")
#
#plt.legend()

ts_pointsA = []
x_pointsA = []
y_pointsA = []
z_pointsA = []
#csv_pointsA = [('Attribute', 'Timestamp', 'x', 'y', 'z')]
csv_pointsA = []
    
ts_pointsG = []
x_pointsG = []
y_pointsG = []
z_pointsG = []
#csv_pointsG = [('Attribute', 'Timestamp', 'x', 'y', 'z')]
csv_pointsG = []

ts_pointsE = []
x_pointsE = []
y_pointsE = []
z_pointsE = []
csv_pointsE = []

ts_pointsQ = []
w_pointsQ = []
x_pointsQ = []
y_pointsQ = []
z_pointsQ = []
csv_pointsQ = []

timestr = time.strftime("%Y%m%d_%H%M%S")
fnameA = 'acceleration_' + timestr + '.csv'
fnameG = 'gyroscope_' + timestr + '.csv'
fnameE = 'euler_' + timestr + '.csv'
fnameQ = 'quaternion_' + timestr + '.csv'

# write csv function
def write_csv(data, csvfilename):
    with open(csvfilename, 'a') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(data)


#with VMU931Parser(device = "COM5", accelerometer=True, gyroscope=True, euler=True, quaternion=True) as vp:
with VMU931Parser(device = "/dev/ttyACM0", accelerometer=True, gyroscope=True, euler=True, quaternion=True) as vp:
    vp.set_accelerometer_resolution(16)  # Set resolution of accelerometer to 8g.
    vp.set_gyroscope_resolution(250)
    start_time = time.time() # Time capture started, in seconds
    seconds_to_capture = 600 
    while time.time() - start_time <= seconds_to_capture:
#    while True:
#    for n in range(20):
        pkt = vp.parse()

        if isinstance(pkt, messages.Status):
            print(pkt)

        if isinstance(pkt, messages.Accelerometer):
            tsA, xA, yA, zA = pkt
            ts_pointsA.append(tsA)
            x_pointsA.append(xA)
            y_pointsA.append(yA)
            z_pointsA.append(zA)
           # csv_pointsA.append(('acceleration', tsA, xA, yA, zA))
           # print(csv_pointsA)
            csv_pointsA = [('acceleration', tsA, xA, yA, zA)]
            write_csv(csv_pointsA, fnameA)
          #  print(csv_pointsA)
            
        if isinstance(pkt, messages.Gyroscope):
            tsG, xG, yG, zG = pkt
            ts_pointsG.append(tsG)
            x_pointsG.append(xG)
            y_pointsG.append(yG)
            z_pointsG.append(zG)
           # csv_pointsG.append(('gyroscope', tsG, xG, yG, zG))
           # print(csv_pointsG)
            csv_pointsG = [('gyroscope', tsG, xG, yG, zG)]
            write_csv(csv_pointsG, fnameG)
            
        if isinstance(pkt, messages.Euler):
            tsE, xE, yE, zE = pkt
            ts_pointsE.append(tsE)
            x_pointsE.append(xE)
            y_pointsE.append(yE)
            z_pointsE.append(zE)
           # csv_pointsG.append(('gyroscope', tsG, xG, yG, zG))
           # print(csv_pointsG)
            csv_pointsE = [('euler', tsE, xE, yE, zE)]
            write_csv(csv_pointsE, fnameE)
         #   print(csv_pointsG)

        if isinstance(pkt, messages.Quaternion):
            tsQ, wQ, xQ, yQ, zQ = pkt
            ts_pointsQ.append(tsQ)
            w_pointsQ.append(wQ)
            x_pointsQ.append(xQ)
            y_pointsQ.append(yQ)
            z_pointsQ.append(zQ)
           # csv_pointsG.append(('gyroscope', tsG, xG, yG, zG))
           # print(csv_pointsG)
            csv_pointsQ = [('quaternion', tsQ, wQ, xQ, yQ, zQ)]
            write_csv(csv_pointsQ, fnameQ)
            #with open("gyroscope.csv", "w", 1) as csvfile:
             #   csvwriter = csv.writer(csvfile)
              #  csvwriter.writerows(csv_pointsG)
            
        # Only plot every 100 points (still quite smooth), otherwise we're bottle-necked by matplotlib.
        # Note that when angular data is not being streamed, the faster update rate is assumed.
#        if len(ts_points) % 100 == 0:
#
 #           # set_data is faster than drawing a whole new line
  #          x_line.set_data(ts_points[-1000:], x_points[-1000:])
   #         y_line.set_data(ts_points[-1000:], y_points[-1000:])
    #        z_line.set_data(ts_points[-1000:], z_points[-1000:])
#
 #           acc_axes.relim()
  #          acc_axes.autoscale_view()
   #         figure.canvas.draw()
##
  #          # Pause to force redraw. Actually blocks until re-draw is complete, 0.00001 is an arbitrary small number.
   #         plt.pause(0.00001)

#with open("Acceleration.csv", "w") as csvfile:
 #   csvwriter = csv.writer(csvfile)
  #  csvwriter.writerows(csv_points)
    
    
