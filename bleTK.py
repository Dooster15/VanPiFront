# ==============
# File: bleTK.py
# By: Jack Holdsworth 
# Use: A UI program to control other devices in my vehicle via ble serial connection.
# Written on: Python 3.8
# ==============
import tkinter as tk   
import serial
import time
from tkinter import ttk

from datetime import datetime  
inputToggle = 0
def remap_range(value, minInput, maxInput, minOutput, maxOutput):

    value = maxInput if value > maxInput else value
    value = minInput if value < minInput else value

    inputSpan = maxInput - minInput
    outputSpan = maxOutput - minOutput

    scaledThrust = float(value - minInput) / float(inputSpan)

    return minOutput + (scaledThrust * outputSpan)

def write_text():
    print("Tkinter is easy to create GUI!")

def toggleInput():
    if inputToggle == 0:
        serialPort.write(b"/o1 \r\n")
        inputToggle = 1
        buttonToggleInput.config(text = "Solar Battery\nPress to toggle to car battery")
    else:
        serialPort.write(b"/o0 \r\n")
        inputToggle = 0
        buttonToggleInput.config(text="Car battery\nPress to switch to solar battery")

class SerialConnection:
    # ble serial connection decoder between an arduino and a raspberry pi
    def ___init__(self):
        f = open("/home/pi/deviceName.txt", "r")
        dev_name = f.read()
        self.battery_voltage = ""

    def connect(self,dev_name):
        self.serial_port = serial.Serial(port = f"{devName}", baudrate=96000,
                           bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)


    def remap_range(self,value, minInput, maxInput, minOutput, maxOutput):

        value = maxInput if value > maxInput else value
        value = minInput if value < minInput else value

        inputSpan = maxInput - minInput
        outputSpan = maxOutput - minOutput

        scaledThrust = float(value - minInput) / float(inputSpan)

        return minOutput + (scaledThrust * outputSpan)

    def read_queue(self):
        serial_string = ""
        while True:
            if (self.serial_port.in_waiting == 0):
                break
            serial_string = self.serial_port.readline()
            ble_text = serial_string.decode('Ascii').strip()

            if ble_text == "Battery Voltage:":
                serial_string = self.serial_port.readline()
                self.battery_voltage = float(serial_string.decode('Ascii').strip())
            elif ble_text == "Battery Current:":
                serial_string = self.serial_port.readline()
                self.battery_current = float(serial_string.decode('Ascii').strip())
            elif ble_text == "Battery Power:":
                serial_string = self.serial_port.readline()
                self.battery_power = float(serial_string.decode('Ascii').strip())
            elif ble_text == "Load Current:":
                serial_string = self.serial_port.readline()
                self.load_current = float(serial_string.decode('Ascii').strip())
            elif ble_text == "PV Voltage:":
                serial_string = self.serial_port.readline()
                self.pv_voltage = float(serial_string.decode('Ascii').strip())

    def update_gui(self):
        # battery voltage
        with open("testBLE.txt", "a") as myfile:
            myfile.write(str(self.battery_voltage))
            myfile.write(",")
        labelBVoltage.config(text = f"Battery Voltage: {self.battery_voltage}")
        progressbarBVoltage['value'] = self.remap_range(self.battery_voltage,10,14,0,100)
        # battery current
        labelBCurrent.config(text = f"Battery Current In: {self.battery_current}")
        # battery power
        labelBPower.config(text = f"Battery Power In: {self.battery_power}")
        progressbar['value'] = self.battery_power
        # load current
        with open("testBLE.txt", "a") as myfile:
            myfile.write(str(self.load_current))
            time_stamp = time.time()
            date_time = datetime.fromtimestamp(time_stamp)
            myfile.write(",")
            myfile.write(str(date_time))
            myfile.write("\n")
        labelLCurrent.config(text = f"Load Current: {self.load_current}")
        # pv voltage
        labelPVVoltage.config(text = f"PV Voltage: {self.pv_voltage}")
        



parent = tk.Tk()
parent.configure(background='black')
parent.geometry('600x480')
frame = tk.Frame(parent,bg='black')

frame.pack()




buttonToggleInput= tk.Button(frame, 
                   text="Car battery\nPress to switch to solar battery", 
                   command=toggleInput,
                   width=40,
                   height=20,
                   fg='#ffffff',
                   bg='#000000',
                   highlightthickness=1,
                   highlightbackground="#0c0c0c"
                   )
progressbarBVoltage = ttk.Progressbar(frame)
progressbarBVoltage.pack(side=tk.BOTTOM)
progressbar = ttk.Progressbar(frame)
progressbar.pack(side=tk.BOTTOM)
labelPVVoltage = tk.Label(frame,
                  text = "start")
labelPVVoltage.pack(side=tk.BOTTOM)

labelBVoltage = tk.Label(frame,
                  text = "start")
labelBVoltage.pack(side=tk.BOTTOM)

labelBCurrent = tk.Label(frame,
                  text = "start")
labelBCurrent.pack(side=tk.BOTTOM)

labelBPower = tk.Label(frame,
                  text = "start")
labelBPower.pack(side=tk.BOTTOM)

labelLCurrent = tk.Label(frame,
                  text = "start")
labelLCurrent.pack(side=tk.BOTTOM)

buttonToggleInput.pack(side=tk.LEFT)


connection = SerialConnection()
time.sleep(15)
f = open("/home/pi/deviceName.txt", "r")
dev_name = f.read()

connection.connect(dev_name)

while(1):


    

    connection.read_queue()
    connection.update_gui()
    # Wait until there is data waiting in the serial buffer
    parent.update()
