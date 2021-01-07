import serial
import pymodbus


class DeyeInverter:

    def __init__():
        pass

    def __init__(self, serialConnection):
        self.ser = serialConnection

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





ser = serial.Serial(port='/dev/ttyACM0', baudrate=9600, timeout=5)

