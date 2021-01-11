import time
import can
import daly
import numpy as np
import serial

data = []
i = 0
w = 0

def canSetWord(i,w):
    w=np.int16(w)
    data.insert(i,0)
    data.insert(i+1, w)

def warnings():
        canID = 0x359
        data = [0,0,0,0,0,0x50,0x4E]
        msg = can.Message(arbitration_id=canID, data=data, is_extended_id=False)
        print(msg)

def chargesettngs():
        canID = 0x351
        canSetWord(0, 55) # Charge Voltage
        canSetWord(0, 60) # Target Charge Current from derate check
        canSetWord(0, 80)
        msg = can.Message(arbitration_id=canID, data=data, is_extended_id=False)
        print(msg)

def batteryState():
        canID = 0x355
        canSetWord(0, 55) # SOC
        canSetWord(2, 95) # SOH
        msg = can.Message(arbitration_id=canID, data=data, is_extended_id=False)
        print (msg)

def batteryPower():
        canID = 0x356
        canSetWord(0, daly.DalyBms.voltage)
        canSetWord(0, daly.DalyBms.current)
        canSetWord(0, daly.DalyBms.temp)
        msg = can.Message(arbitration_id=canID, data=data, is_extended_id=False)
        print(msg)

def messages():
        #warnings()
        #chargesettngs()
        batteryState()

def sender():

    while True:
        bus = can.interfaces.Bus(channel='/dev/ttyAMA0', baudrate=9600, timeout=5)
        try:
            bus.send(messages())
            print("Message sent on {}".format(bus.channel_info))
            time.sleep(1)
        except can.CanError:
            print("Message NOT sent")

sender()

#   Adress  Discription     R/W     Ranges  unit    remarks
#   200     Control mode    R/W                     0x0001 Lithium Battery
#   202     Absorbtion V    R/W             0.1V    5550
#   203     Float Voltage   R/W             0.1V    5400
#   204     Batt Capacity   R/W             1 Ah    360
#   210     Max A Charge    R/W             1 Ah    60
#   211     Max A Discharge R/W             1 Ah    80
#   314     Charging current limiting       1 Ah
#   316     real time Capacity              1%      SOC
#   317     real time voltage               0.01V
#   318     real time current               1 Ah
#   319     real time temp  R/W             0.1 C   1000 = 0 degrees C, 1200 = 20C, 800 = -20C







