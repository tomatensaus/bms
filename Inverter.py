import daly
from struct import *
import can
import serial.rs485
import time
import os

class DeyeInverter:
    def __init__():
        pass

    def __init__(self, canConnect):
        self.can0 = canConnect

    def hilobytes(self, integer):
        return divmod(integer, 0x100)

    def msg359(self):  # msg359 8 bytes: Protection, Protection, Alarm, Alarm, Module numbers, P & N at bits 5 and 6
        self.arbitration_id = 0x359
        self.data = [0x00, 0x00, 0x00, 0x00, 0x01, 0x50, 0x4e]
        self.extended_id = False
        self.msg = can.Message(arbitration_id=self.arbitration_id, data=self.data, extended_id=self.extended_id)
        print(self.msg)
        can0.send(self.msg)
        #Alarms and warnings to be included

    def msg351(self):  # msg351 6 bytes: Battery charge voltage(2), Charge current limit(2), Discharge current limit (2)
        self.arbitration_id = 0x351
        self.data = [0x2b, 0x02, 0x58, 0x02, 0x8e, 0x03]
        self.extended_id = False
        self.msg = can.Message(arbitration_id=self.arbitration_id, data=self.data, extended_id=self.extended_id)
        print(self.msg)
        can0.send(self.msg)
        #Hardcoded values for now, will include a reducing value on charge current as SOH increases

    def msg355(self):  # msg355 4 bytes: SOC (2), SOH (2)
        self.batsoc_high, self.batsoc_low = self.hilobytes(int(bms.soc))
        self.batsoh_high, self.batsoh_low = self.hilobytes(int(100))
        self.arbitration_id = 0x355
        self.data = [(self.batsoc_low), (self.batsoc_high),
                     (self.batsoh_low), (self.batsoh_high)]
        self.extended_id = False
        self.msg = can.Message(arbitration_id=self.arbitration_id, data=self.data, extended_id=self.extended_id)
        print(self.msg)
        can0.send(self.msg)

    def msg356(self):  # msg356 6 bytes: Battery voltage (2), Battery current (2), Battery temp (2)
        self.arbitration_id = 0x356
        self.battery_voltage_high, self.battery_voltage_low = self.hilobytes(int(bms.voltage*100))
        self.battery_current_high, self.battery_current_low = self.hilobytes(int(bms.current*10))
        self.battery_temp_high, self.battery_temp_low = self.hilobytes(int(bms.bat_temp*10))
        self.data = [self.battery_voltage_low, self.battery_voltage_high,
                     self.battery_current_low, self.battery_current_high,
                     self.battery_temp_low, self.battery_temp_high]
        self.extended_id = False
        self.msg = can.Message(arbitration_id=self.arbitration_id, data=self.data, extended_id=self.extended_id)
        print(self.msg)
        can0.send(self.msg)

    def msg35C(self):  # msg35C 1 byte: Discharge / Charge
        self.arbitration_id = 0x35C
        self.data = [0x60, 0x00]
        self.extended_id = False
        self.msg = can.Message(arbitration_id=self.arbitration_id, data=self.data, extended_id=self.extended_id)
        print(self.msg)
        can0.send(self.msg)
        # Hardcoded charge and discharge to always be enabled, can be changed in future to receive command from BMS

    def msg35E(self):  # msg35E 2 bytes: Manufacturer name
        self.arbitration_id = 0x35E
        self.data = [0x50, 0x59, 0x4C, 0x4f, 0x4e]
        self.extended_id = False
        self.msg = can.Message(arbitration_id=self.arbitration_id, data=self.data, extended_id=self.extended_id)
        print(self.msg)
        can0.send(self.msg)
        # For now, this reads PYLON

if __name__ == '__main__':

    while True:
        ser = serial.rs485.RS485(port='/dev/ttyUSB0', baudrate=9600, timeout=5)
        ser.rs485_mode = serial.rs485.RS485Settings()
        bms = daly.DalyBms(ser)

        os.system('sudo ip link set can0 type can bitrate 500000')
        os.system('sudo ifconfig can0 up')
        can0 = can.interface.Bus(channel = 'can0', bustype='socketcan_ctypes')
        can0.flush_tx_buffer()
        inv = DeyeInverter(can0)

        #
        #     inv.send()
        #     time.sleep(10)
        #     inv.receive()


        bms.update()
        inv.msg351()
        time.sleep(0.1)
        inv.msg355()
        time.sleep(0.1)
        inv.msg356()
        time.sleep(0.1)
        inv.msg359()
        time.sleep(0.1)
        # inv.msg35C()
        # time.sleep(0.1)
        inv.msg35E()

        print("BMS Voltage:", bms.voltage)
        print("BMS SOC:", bms.soc)
        print("BMS Current:", bms.current)
        print("BMS Temp:", bms.bat_temp)
        # print("Inv Voltage:", inv.battery_voltage)
        # print("Inv SOC:", inv.batsoc)
        # print("Inv Current:", inv.battery_current)
        # print("Inv Temp:", inv.battery_temp)







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

# self.batV1, self.batV2 = hex(self.battery_voltage)[2:][:-2], hex(self.battery_voltage)[2:][-2:]
# batV1Hex = format(int(self.batV1, 16), '#04x')
# batV2Hex = format(int(self.batV2, 16), '#04x')
# self.batC1, self.batC2 = hex(self.battery_current)[2:][:-2], hex(self.battery_current)[2:][-2:]
# batC1Hex = format(int(self.batC1, 16), '#04x')
# batC2Hex = format(int(self.batC2, 16), '#04x')
# self.batT1, self.batT2 = hex(self.battery_temp)[2:][:-2], hex(self.battery_temp)[2:][-2:]
# batT1Hex = format(int(self.batT1, 16), '#04x')
# batT2Hex = format(int(self.batT2, 16), '#04x')





