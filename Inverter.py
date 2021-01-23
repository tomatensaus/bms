
class DeyeInverter:
    def __init__():
        pass

    def __init__(self, canConnect):
        os.system('sudo ip link set can0 type can bitrate 9600')
        os.system('sudo ifconfig can0 up')
        self.can0 = canConnect

    def messageData(self):
        self.arbitration_id = 0x351
        self.data = [0x03, 0x00, 0x6B, 0x00, 0x03]

    def send(self):
        msg = can.Message(self.messageData())
        can0.send(msg)
        print(can.Message)

    def receive(self):
        msg = can0.recv(15)
        print(msg)


if __name__ == '__main__':
    import can
    import time
    import os

    can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan_ctypes')
    inv = DeyeInverter(can0)

    while True:
        inv.send()
        time.sleep(10)
        inv.receive()








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







