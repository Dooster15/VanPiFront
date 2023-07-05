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
from barchart import tk_bar_graph
from stacks import qqueue
import random

# inputToggle = 0
# def remap_range(value, minInput, maxInput, minOutput, maxOutput):

#     value = maxInput if value > maxInput else value
#     value = minInput if value < minInput else value

#     inputSpan = maxInput - minInput
#     outputSpan = maxOutput - minOutput

#     scaledThrust = float(value - minInput) / float(inputSpan)

#     return minOutput + (scaledThrust * outputSpan)

# def write_text():
#     print("Tkinter is easy to create GUI!")

# def toggleInput():
#     if inputToggle == 0:
#         serialPort.write(b"/o1 \r\n")
#         inputToggle = 1
#         buttonToggleInput.config(text = "Solar Battery\nPress to toggle to car battery")
#     else:
#         serialPort.write(b"/o0 \r\n")
#         inputToggle = 0
#         buttonToggleInput.config(text="Car battery\nPress to switch to solar battery")
load_current_queue_minute = qqueue(60)
load_current_queue_hour = qqueue(60)

battery_volt_queue_minute = qqueue(60)
battery_volt_queue_hour = qqueue(60)

battery_current_queue_minute = qqueue(60)
battery_current_queue_hour = qqueue(60)

battery_power_queue_minute = qqueue(60)
battery_power_queue_hour = qqueue(60)

pv_volt_queue_minute = qqueue(60)
pv_volt_queue_hour = qqueue(60)

class SerialConnection:
    # ble serial connection decoder between an arduino and a raspberry pi
    def __init__(self):
        # f = open("/home/pi/deviceName.txt", "r")
        # dev_name = f.read()
        self.battery_voltage = 0
        self.battery_current = 0
        self.battery_power = 0
        self.load_current = 0
        self.pv_voltage = 0
        self.inputToggle = 0
        self.last_time = 0
        self.load_power = 0


    def close_serial(self):
        self.serial_port.close()

    def battery_toggle(self):
        if self.inputToggle == 0:
            self.serial_port.write(b"/o1 \r\n")
            self.inputToggle = 1
            buttonToggleInput.config(text = "Solar Battery\nPress to toggle to car battery")
        else:
            self.serial_port.write(b"/o0 \r\n")
            self.inputToggle = 0
            buttonToggleInput.config(text="Car battery\nPress to switch to solar battery")

    def connect(self, dev_name):
        print(dev_name)
        self.serial_port = serial.Serial(port = f"{dev_name}", baudrate=96000,
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
            else:
                break

    def update_gui(self):
        now = datetime.now()
        if self.last_time != now.second:
            self.last_time = now.second
            # battery voltage
            with open("testBLE.txt", "a") as myfile:
                myfile.write(str(self.battery_voltage))
                myfile.write(",")
            # labelBVoltage.config(text = f"Battery Voltage: {self.battery_voltage}")
            battery_volt_queue_minute.push(self.battery_voltage)
            for count,value in enumerate(battery_volt_queue_minute.get_stack()):
                bar_value = int(self.remap_range(value,10,13,0,80))
                if bar_value > 80:
                    bar_value = 80
                graph_battery_volt_minute.bar_val(count,bar_value)
                graph_label_battery_volt.config(text=f'{value:.2f}')
            # progressbarBVoltage['value'] = self.remap_range(self.battery_voltage,10,14,0,100)
            

            # battery current
            # labelBCurrent.config(text = f"Battery Current In: {self.battery_current}")
            battery_current_queue_minute.push(self.battery_current)
            for count,value in enumerate(battery_current_queue_minute.get_stack()):
                bar_value = int(self.remap_range(value,0,8,0,80))
                if bar_value > 80:
                    bar_value = 80
                graph_battery_current_minute.bar_val(count,bar_value)
                graph_label_battery_current.config(text=f'{value:.2f}')

            # battery power
            # labelBPower.config(text = f"Battery Power In: {self.battery_power}")
            self.load_power = self.load_current*self.battery_voltage
            battery_power_queue_minute.push(self.battery_power-self.load_power)
            for count,value in enumerate(battery_power_queue_minute.get_stack()):
                if value >= 0:
                    colour = 'green'
                    bar_value = int(self.remap_range(value,0,100,0,80))
                else:
                    colour = 'red'
                    bar_value = int(self.remap_range(value,-100,0,-80,0))
                if bar_value > 80:
                    bar_value = 80
                graph_battery_power_minute.bar_val(count,bar_value)

                graph_label_battery_power.config(text=f'{value:.2f}',background=colour)
            # progressbar['value'] = self.battery_power

            # load current
            with open("testBLE.txt", "a") as myfile:
                myfile.write(str(self.load_current))
                time_stamp = time.time()
                date_time = datetime.fromtimestamp(time_stamp)
                myfile.write(",")
                myfile.write(str(date_time))
                myfile.write("\n")
            # labelLCurrent.config(text = f"Load Current: {self.load_current}")
            load_current_queue_minute.push(self.load_current)
            for count,value in enumerate(load_current_queue_minute.get_stack()):
                bar_value = int(self.remap_range(value,0,10,0,80))
                if bar_value > 80:
                    bar_value = 80
                graph_load_current_minute.bar_val(count,bar_value)
                graph_label_load_current.config(text=f'{value:.2f}')


            # now = datetime.now()
            # if self.last_time != now.second:
            #     # waitqueue.push(self.load_current)
            #     waitqueue.push(random.randint(0,self.minute_rand)/100)
            #     self.last_time = now.second
            #     print(now.second)
            #     if now.second == 0:
            #         self.minute_rand = random.randint(0,100)
            #         print('here')
            #         minute_sum = 0
            #         for i in waitqueue.get_stack():
            #             minute_sum += i
            #         waitqueuehour.push(minute_sum/60)
                
            # pv voltage
            # labelPVVoltage.config(text = f"PV Voltage: {self.pv_voltage}")
            pv_volt_queue_minute.push(self.pv_voltage)
            for count,value in enumerate(pv_volt_queue_minute.get_stack()):
                bar_value = int(self.remap_range(value,0,22,0,80))
                if bar_value > 80:
                    bar_value = 80
                graph_pv_volt_minute.bar_val(count,bar_value)
                graph_label_pv_volt.config(text=f'{value:.2f}')

            

            if now.second == 0:

                sum = 0
                for i in load_current_queue_minute.get_stack():
                    sum += i
                load_current_queue_hour.push(sum/60)
                for count,value in enumerate(load_current_queue_hour.get_stack()):
                    bar_value = int(self.remap_range(value,0,10,0,80))
                    if bar_value > 80:
                        bar_value = 80
                    graph_load_current_hour.bar_val(count,bar_value)

                sum = 0 
                for i in pv_volt_queue_minute.get_stack():
                    sum += i
                pv_volt_queue_hour.push(sum/60)
                for count,value in enumerate(pv_volt_queue_hour.get_stack()):
                    bar_value = int(self.remap_range(value,0,22,0,80))
                    if bar_value > 80:
                        bar_value = 80
                    graph_pv_volt_hour.bar_val(count,bar_value)

                sum = 0
                for i in battery_power_queue_minute.get_stack():
                    sum += i
                battery_power_queue_hour.push(sum/60)
                for count,value in enumerate(battery_power_queue_hour.get_stack()):
                    if value >= 0:
                        bar_value = int(self.remap_range(value,0,100,0,80))
                    else:
                        bar_value = int(self.remap_range(value,-100,0,-80,0))
                    if bar_value > 80:
                        bar_value = 80
                    graph_battery_power_hour.bar_val(count,bar_value)

                sum = 0
                for i in battery_current_queue_minute.get_stack():
                    sum += i
                battery_current_queue_hour.push(sum/60)
                for count,value in enumerate(battery_current_queue_hour.get_stack()):
                    bar_value = int(self.remap_range(value,0,8,0,80))
                    if bar_value > 80:
                        bar_value = 80
                    graph_battery_current_hour.bar_val(count,bar_value)

                sum = 0 
                for i in battery_volt_queue_minute.get_stack():
                    sum += i
                battery_volt_queue_hour.push(sum/60)
                for count,value in enumerate(battery_volt_queue_hour.get_stack()):
                    bar_value = int(self.remap_range(value,10,13,0,80))
                    if bar_value > 80:
                        bar_value = 80
                    graph_battery_volt_hour.bar_val(count,bar_value)


    def update_label(self,text):
        pass
        # labelBVoltage.config(text = f"{text}")
        
time.sleep(15)
connection = SerialConnection()

parent = tk.Tk()
parent.configure(background='black')
parent.geometry('600x480')

frame_load_current = tk.Frame(parent,bg='blue',height=80,width=480)
graph_load_current_hour = tk_bar_graph(0,0,80,3,60,0,frame_load_current)
graph_load_current_minute = tk_bar_graph(185,0,80,3,60,0,frame_load_current)
graph_name_label_load_current = tk.Label(frame_load_current, text = 'LOAD CURRENT',font=('Segoe UI Black',10,'normal'),background='green')
graph_name_label_load_current.place(x=370,y=5)
graph_label_load_current = tk.Label(frame_load_current, text = '50.4',font=('8514oem',30,'normal'),background='green')
graph_label_load_current.place(x=380,y=30)
frame_load_current.place(x=10,y=10)

frame_pv_volt = tk.Frame(parent,bg='blue',height=80,width=480)
graph_pv_volt_hour = tk_bar_graph(0,0,80,3,60,0,frame_pv_volt)
graph_pv_volt_minute = tk_bar_graph(185,0,80,3,60,0,frame_pv_volt)
graph_name_label_pv_volt = tk.Label(frame_pv_volt, text = 'PV VOLTAGE',font=('Segoe UI Black',10,'normal'),background='green')
graph_name_label_pv_volt.place(x=370,y=5)
graph_label_pv_volt = tk.Label(frame_pv_volt, text = '50.4',font=('8514oem',30,'normal'),background='green')
graph_label_pv_volt.place(x=380,y=30)
frame_pv_volt.place(x=10,y=100)

frame_battery_power = tk.Frame(parent,bg='blue',height=80,width=480)
graph_battery_power_hour = tk_bar_graph(0,0,80,3,60,0,frame_battery_power)
graph_battery_power_minute = tk_bar_graph(185,0,80,3,60,0,frame_battery_power)
graph_name_label_battery_power = tk.Label(frame_battery_power, text = 'BATTERY POWER',font=('Segoe UI Black',10,'normal'),background='green')
graph_name_label_battery_power.place(x=370,y=5)
graph_label_battery_power = tk.Label(frame_battery_power, text = '50.4',font=('8514oem',30,'normal'),background='green')
graph_label_battery_power.place(x=380,y=30)
frame_battery_power.place(x=10,y=190)

frame_battery_current = tk.Frame(parent,bg='blue',height=80,width=480)
graph_battery_current_hour = tk_bar_graph(0,0,80,3,60,0,frame_battery_current)
graph_battery_current_minute = tk_bar_graph(185,0,80,3,60,0,frame_battery_current)
graph_name_label_battery_current = tk.Label(frame_battery_current, text = 'BATTERY CURRENT',font=('Segoe UI Black',10,'normal'),background='green')
graph_name_label_battery_current.place(x=370,y=5)
graph_label_battery_current = tk.Label(frame_battery_current, text = '50.4',font=('8514oem',30,'normal'),background='green')
graph_label_battery_current.place(x=380,y=30)
frame_battery_current.place(x=10,y=280)

frame_battery_volt = tk.Frame(parent,bg='blue',height=80,width=480)
graph_battery_volt_hour = tk_bar_graph(0,0,80,3,60,0,frame_battery_volt)
graph_battery_volt_minute = tk_bar_graph(185,0,80,3,60,0,frame_battery_volt)
graph_name_label_battery_volt = tk.Label(frame_battery_volt, text = 'BATTERY VOLTAGE',font=('Segoe UI Black',10,'normal'),background='green')
graph_name_label_battery_volt .place(x=370,y=5)
graph_label_battery_volt = tk.Label(frame_battery_volt, text = '50.4',font=('8514oem',30,'normal'),background='green')
graph_label_battery_volt.place(x=380,y=30)
frame_battery_volt.place(x=10,y=370)


frame = tk.Frame(parent,bg='blue',height=460,width=90)

frame.place(x=500,y=10)


buttonToggleInput= tk.Button(frame, 
                   text="Car battery\nPress to switch to solar battery", 
                   command=connection.battery_toggle,
                   width=11,
                   height=30,
                   fg='#ffffff',
                   bg='#000000',
                   highlightthickness=1,
                   highlightbackground="#0c0c0c"
                   )
buttonToggleInput.place(x=0, y=0)
# progressbarBVoltage = ttk.Progressbar(frame, orient='vertical')
# progressbarBVoltage.pack(side=tk.BOTTOM)
# progressbar = ttk.Progressbar(frame)
# progressbar.pack(side=tk.BOTTOM)
# labelPVVoltage = tk.Label(frame,
#                  text = "start",
#                  fg='#ffffff',
#                  bg='#000000'
#                  )
# labelPVVoltage.pack(side=tk.BOTTOM)

# labelBVoltage = tk.Label(frame,
#                   text = "start",
#                   fg='#ffffff',
#                   bg='#000000')
# labelBVoltage.pack(side=tk.BOTTOM)

# labelBCurrent = tk.Label(frame,
#                   text = "start",
#                   fg='#ffffff',
#                   bg='#000000')
# labelBCurrent.pack(side=tk.BOTTOM)

# labelBPower = tk.Label(frame,
#                   text = "start",
#                   fg='#ffffff',
#                   bg='#000000')
# labelBPower.pack(side=tk.BOTTOM)

# labelLCurrent = tk.Label(frame,
#                   text = "start",
#                   fg='#ffffff',
#                   bg='#000000')
# labelLCurrent.pack(side=tk.BOTTOM)

# buttonToggleInput.pack(side=tk.LEFT)


while True:
    parent.update()
    try:
            time.sleep(15)
            f = open("/home/pi/deviceName.txt", "r")
            dev_name = f.read()
            connection.connect(dev_name)
            while(1):
                connection.read_queue()
                connection.update_gui()

                # Wait until there is data waiting in the serial buffer
                parent.update()
    except:
        # connection.update_label('error')
        print('error')
