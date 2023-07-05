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


time.sleep(10)

f = open("/home/pi/deviceName.txt", "r")
devName = f.read()

serialPort = serial.Serial(port = f"{devName}", baudrate=96000,
                           bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
serialString = ""                           # Used to hold data coming over UART

# awns = int(input("1 or 0: "))
# if awns == 1:
#     serialPort.write(b"/o1 \r\n")
# else:
#     serialPort.write(b"/o0 \r\n")

# while(1):

#     # Wait until there is data waiting in the serial buffer
    
#     if(serialPort.in_waiting > 0):
#         #print(str(serialPort.in_waiting))  

#         # Read data out of the buffer until a carraige return / new line is found
#         serialString = serialPort.readline()

#         # Print the contents of the serial data
#         print(serialString.decode('Ascii').strip())

#         # Tell the device connected over the serial port that we recevied the data!
#         # The b at the beginning is used to indicate bytes!
#         # serialPort.write(b"/o1 \r\n")
#         # time.sleep(3)
#         # serialPort.write(b"/o0 \r\n")


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

# exit_button = tk.Button(frame,
#                    text="Off",
#                    fg="green",
#                    command=turnOff,
#                    width=40,
#                    height=20,
#                    bg='#000000'
#                    )
# exit_button.pack(side=tk.RIGHT)


while(1):

    # Wait until there is data waiting in the serial buffer
    
    if(serialPort.in_waiting > 0):
        print(str(serialPort.in_waiting))  

        # Read data out of the buffer until a carraige return / new line is found
        serialString = serialPort.readline()

        # Print the contents of the serial data
        ble_text = serialString.decode('Ascii').strip()
        if ble_text == "Battery Voltage:":
            serialString = serialPort.readline()
            batteryVoltage = float(serialString.decode('Ascii').strip())
            with open("testBLE.txt", "a") as myfile:
                myfile.write(str(batteryVoltage))
                myfile.write(",")
            labelBVoltage.config(text = f"Battery Voltage: {batteryVoltage}")
            progressbarBVoltage['value'] = remap_range(batteryVoltage,10,14,0,100)
        elif ble_text == "Battery Current:": 
            serialString = serialPort.readline()
            batteryCurrent = float(serialString.decode('Ascii').strip())
            labelBCurrent.config(text = f"Battery Current In: {batteryCurrent}")
        elif ble_text == "Battery Power:":
            serialString = serialPort.readline()
            batteryPower = float(serialString.decode('Ascii').strip())
            labelBPower.config(text = f"Battery Power In: {batteryPower}")
            progressbar['value'] = batteryPower
        elif ble_text == "Load Current:":
            serialString = serialPort.readline()
            loadCurrent = float(serialString.decode('Ascii').strip())
            with open("testBLE.txt", "a") as myfile:
                myfile.write(str(loadCurrent))
                time_stamp = time.time()
                date_time = datetime.fromtimestamp(time_stamp)
                myfile.write(",")
                myfile.write(str(date_time))
                myfile.write("\n")
            labelLCurrent.config(text = f"Load Current: {loadCurrent}")
        elif ble_text == "PV Voltage:":
            serialString = serialPort.readline()
            PVVoltage = float(serialString.decode('Ascii').strip())
            labelPVVoltage.config(text = f"PV Voltage: {PVVoltage}")



        # Tell the device connected over the serial port that we recevied the data!
        # The b at the beginning is used to indicate bytes!
        # serialPort.write(b"/o1 \r\n")
        # time.sleep(3)
        # serialPort.write(b"/o0 \r\n")
    parent.update()
