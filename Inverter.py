
class DeyeInverter:

    def __init__(self, serialConnection):
        self.ser = serialConnection

    def sendCheckSum(self, command):
        checksum = 0xa5 + 0x40 + command + 0x08
        # print("WChecksum: ",hex(checksum)) #checksum mod 256 to get lower 2 bytes
        # print(hex(256))
        # print (hex(checksum  % 0x100))
        return checksum % 0x100

    def send(self, command):
        hexs = "a5 40 {:02X} 08 00 00 00 00 00 00 00 00 {:02X}".format(command, self.sendCheckSum(command))
        # print("Write: " ,hexs)
        self.ser.write(bytearray.fromhex(hexs))

if __name__ == '__main__':
    import serial.rs485

    ser = serial.rs485.RS485(port='/dev/ttyAMA0', baudrate=9600, timeout=5)
    ser.rs485_mode = serial.rs485.RS485Settings
    inverter = DeyeInverter(ser)
    DeyeInverter.send(inverter, 316)



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







