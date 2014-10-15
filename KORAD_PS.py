# -*- coding: utf-8 -*-
"""
Created on Thu Oct  9 23:05:05 2014

@author: jason
"""

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import serial
import time

#==============================================================================
# Define protocol commands
#==============================================================================
REQUEST_STATUS = b"STATUS?"  # Request actual status.
    # 0x40 (Output mode: 1:on, 0:off)
    # 0x20 (OVP and/or OCP mode: 1:on, 0:off)
    # 0x01 (CV/CC mode: 1:CV, 0:CC)
REQUEST_ID = b"*IDN?"

REQUEST_SET_VOLTAGE = b"VSET1?"  # request the set voltage
REQUEST_ACTUAL_VOLTAGE = b"VOUT1?"  # Request output voltage

REQUEST_SET_CURRENT = b"ISET1?"  # Request the set current
REQUEST_ACTUAL_CURRENT = b"IOUT1?"  # Requst the output current

SET_VOLTAGE = b"VSET1:"  # Set the maximum output voltage
SET_CURRENT = b"ISET1:"  # Set the maximum output current

SET_OUTPUT = b"OUT"  # Enable the power output

SET_OVP = b"OVP"  # Enable(1)/Disable(0) OverVoltageProtection

SET_OCP = b"OCP"  # Enable(1)/Disable(0) OverCurrentProtection

#==============================================================================
# Methods
#==============================================================================


def GetID():
    PS = serial.Serial("/dev/ttyACM0",
                       baudrate=9600,
                       bytesize=8,
                       parity='N',
                       stopbits=1,
                       timeout=1)
    PS.flushInput()
    PS.write(REQUEST_ID)  # Request the ID from the Power Supply
    PSID = PS.read(16)
    print(b'PSID = '+PSID)
    PS.flushInput()
    return(PSID)


def Get_I_Set():
    PS = serial.Serial("/dev/ttyACM0",
                       baudrate=9600,
                       bytesize=8,
                       parity='N',
                       stopbits=1,
                       timeout=1)
    PS.flushInput()
    PS.write(REQUEST_SET_CURRENT)  # Request the target current
    I_set = PS.read(5)
    if (I_set == b''):
        I_set = b'0'
    I_set = float(I_set)
    print(str('Current is set to ')+str(I_set))
    PS.flushInput()
    return(I_set)


def Get_V_Set():
    PS = serial.Serial("/dev/ttyACM0",
                       baudrate=9600,
                       bytesize=8,
                       parity='N',
                       stopbits=1,
                       timeout=1)
    PS.flushInput()
    PS.write(REQUEST_SET_VOLTAGE)  # Request the target voltage
    V_set = float(PS.read(5))
    print(str('Voltage is set to ')+str(V_set))
    PS.flushInput()
    return(V_set)


def Get_Status():
    PS = serial.Serial("/dev/ttyACM0",
                       baudrate=9600,
                       bytesize=8,
                       parity='N',
                       stopbits=1,
                       timeout=1)
    PS.flushInput()
    PS.write(REQUEST_STATUS)  # Request the status of the PS
    Stat = str(PS.read(5))
    print('Status = '+Stat)
    PS.flushInput()
    return(Stat)


def SetVoltage(Voltage):
    PS = serial.Serial("/dev/ttyACM0",
                       baudrate=9600,
                       bytesize=8,
                       parity='N',
                       stopbits=1,
                       timeout=1)
    PS.flushInput()
    if (float(Voltage) > float(VMAX)):
        Voltage = VMAX
    Voltage = "{:2.2f}".format(float(Voltage))
    Output_string = SET_VOLTAGE + bytes(Voltage, "utf-8")
    PS.write(Output_string)
    print(Output_string)
    PS.flushInput()
    time.sleep(0.2)
    VeriVolt = "{:2.2f}".format(float(Get_V_Set()))  # Verify PS accepted
        # the setting
#    print(VeriVolt)
#    print(Voltage)
    while (VeriVolt != Voltage):
        PS.write(Output_string)  # Try one more time
    vEntry.delete(0, 5)
    vEntry.insert(0, "{:2.2f}".format(float(VeriVolt)))
    return(Output_string)


def SetCurrent(Current):
    PS = serial.Serial("/dev/ttyACM0",
                       baudrate=9600,
                       bytesize=8,
                       parity='N',
                       stopbits=1,
                       timeout=1)
    PS.flushInput()
    if (float(Current) > float(IMAX)):
        Current = IMAX
    Current = "{:2.3f}".format(float(Current))
    Output_string = SET_CURRENT + bytes(Current, "utf-8")
    PS.write(Output_string)
    print(Output_string)
    PS.flushInput()
    time.sleep(0.2)
    VeriAmp = "{:2.3f}".format(float(Get_I_Set()))
    if (VeriAmp != Current):
        VeriAmp = 0.00
    iEntry.delete(0, 5)
    iEntry.insert(0, "{:2.3f}".format(float(VeriAmp)))
    return(Output_string)


def V_Actual():
    PS = serial.Serial("/dev/ttyACM0",
                       baudrate=9600,
                       bytesize=8,
                       parity='N',
                       stopbits=1,
                       timeout=1)
    PS.flushInput()
    PS.write(REQUEST_ACTUAL_VOLTAGE)  # Request the actual voltage
    time.sleep(0.015)
    V_actual = PS.read(5)
    if (V_actual == b''):
            V_actual = b'0'  # deal with the occasional NULL from PS
#    print('V_actual = ' + str(V_actual))
    V_actual = float(V_actual)
    PS.flushInput()
    return(V_actual)


def I_Actual():
    PS = serial.Serial("/dev/ttyACM0",
                       baudrate=9600,
                       bytesize=8,
                       parity='N',
                       stopbits=1,
                       timeout=1)
    PS.flushInput()
    PS.write(REQUEST_ACTUAL_CURRENT)  # Request the actual current
    time.sleep(0.015)
    I_actual = PS.read(5)
    if (I_actual == b''):
            I_actual = b'0'  # deal with the occasional NULL from PS
    I_actual = float(I_actual)
    PS.flushInput()
    return(I_actual)


def SetOP(OnOff):
    PS = serial.Serial("/dev/ttyACM0",
                       baudrate=9600,
                       bytesize=8,
                       parity='N',
                       stopbits=1,
                       timeout=1)
    PS.flushInput()

    Output_string = SET_OUTPUT + bytes(OnOff, "utf-8")

    PS.write(Output_string)
    print(Output_string)
    PS.flushInput()
    return(Output_string)


def SetOVP(OnOff):
    PS = serial.Serial("/dev/ttyACM0",
                       baudrate=9600,
                       bytesize=8,
                       parity='N',
                       stopbits=1,
                       timeout=1)
    PS.flushInput()
    Output_string = SET_OVP + str(OnOff)
    PS.write(bytes(Output_string, "utf-8"))
    print(Output_string)
    PS.flushInput()
    return(Output_string)


def SetOCP(OnOff):
    PS = serial.Serial("/dev/ttyACM0",
                       baudrate=9600,
                       bytesize=8,
                       parity='N',
                       stopbits=1,
                       timeout=1)
    PS.flushInput()
    Output_string = SET_OCP + str(OnOff)
    PS.write(bytes(Output_string, "utf-8"))
    print(Output_string)
    PS.flushInput()
    return(Output_string)


def Update_VandI():
#    print(V_Actual())
    V_actual = "{:2.2f}".format(V_Actual())
    vReadoutLabel.configure(text="{} {}".format(V_actual, 'V'))
#    print(V_actual)

    I_actual = "{0:.3f}".format(I_Actual())
    iReadoutLabel.configure(text="{} {}".format(I_actual, 'A'))
#    print(I_actual)


def Application_Loop():
#        print('application loop run')
        app.after(75, Update_VandI)
        app.after(100, Application_Loop)


def SetVA():
    Volts = vEntry.get()
    SetVoltage(Volts)

    Amps = iEntry.get()
    if (Amps == ''):
        Amps = b'0'
        print('changed Amps to 0')
    Amps = "{0:.3f}".format(float(Amps))
    SetCurrent(Amps)


def MemSet(MemNum):
    print(MemNum)


#==============================================================================
# Variables
#==============================================================================
V_set = "{0:.2f}".format(Get_V_Set(), 'V')
I_set = "{0:.3f}".format(Get_I_Set(), 'I')
PSID = GetID()
Stat = Get_Status()
VMAX = '61'
IMAX = '3.1'


#==============================================================================
# Create Window
#==============================================================================
app = Tk()
app.geometry("400x280+1200+1200")
app.title('TK Experiment')

# Actual Readout area
#==============================================================================
actualLabel = ttk.Label(app)
actualLabel.grid(row=0, column=0, sticky='W', padx=50, pady=10)
actualLabel.configure(text='Actual')

vReadoutLabel = ttk.Label(app, text="unknown")
vReadoutLabel.grid(row=1, column=0, sticky='E', padx=50, pady=5)

iReadoutLabel = ttk.Label(app, text="unknown")
iReadoutLabel.grid(row=2, column=0, sticky='E', padx=50, pady=0)

#spacerLabel = ttk.Label(app, text="         ")
#spacerLabel.grid(row=0, column=1, sticky=N)

# Set textentry area
#==============================================================================
setValLabel = ttk.Label(app, text="Set")
setValLabel.grid(row=0, column=2, sticky='N', padx=50, pady=10)


Volts = StringVar(name=str(V_set))
vEntry = Entry(app, textvariable=Volts)
vEntry.delete(0, 5)
vEntry.insert(0, Volts)
vEntry["width"] = 5
vEntry.grid(row=1, column=2, sticky='E', padx=50, pady=0)
#Amps = vEntry.get()


Amps = StringVar(name=str(I_set))
iEntry = Entry(app, textvariable=Amps)
iEntry.insert(0, I_set)
iEntry["width"] = 5
iEntry.grid(row=2, column=2, sticky='E', padx=50, pady=0)
#Amps = iEntry.get()

 #Button Area
#==============================================================================
Op_On_Button = Button(app)
Op_On_Button.configure(text='Turn OP On')
Op_On_Button.grid(row=4, column=1, sticky='N')
Op_On_Button.configure(command=lambda: SetOP('1'))


Op_Off_Button = Button(app)
Op_Off_Button.configure(text='Turn OP Off')
Op_Off_Button.grid(row=5, column=1, sticky='N')
Op_Off_Button.configure(command=lambda: SetOP('0'))


Set_Button = Button(app)
Set_Button.configure(text='Set V & I')
Set_Button.grid(row=4, column=2, sticky='N')
Set_Button.configure(command=lambda: SetVA())


#Mem1_Button = Button(app)
#Mem1_Button.configure(text='M1: ')
#Mem1_Button.grid(row=10, column=0, sticky='W')
#Mem1_Button.configure(command=lambda: MemSet(1))


#==============================================================================
# Loop
#==============================================================================
# Update_VandI()
Application_Loop()
app.mainloop()
