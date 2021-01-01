#!/usr/bin/env python3

class DalyBms:

	def __init__():
		pass

	def __init__(self, serialConnection):
		self.ser = serialConnection

	def update(self):
		# SOC, Voltage, Current
		self.send(0x90) 
		data = self.read(0x90) 
		self.voltage = self.twoBytes(data,0)/10.0 
		self.current = ((self.twoBytes(data,4) - 30000) / 10.0) 
		self.soc = (100 - (self.twoBytes(data,6)/10.0)) 

		# Max / Min Cell voltages
		self.send(0x91)
		data = self.read(0x91)
		self.bat_maxv = self.twoBytes(data, 0) / 1000.0
		self.bat_maxc = self.oneByte(data, 2)
		self.bat_minv = self.twoBytes(data, 3) / 1000.0
		self.bat_minc = self.oneByte(data, 5)

		# Individual cell temperatures
		self.send(0x92);
		data = self.read(0x92)

		# Charge / Discharge Mos status
		self.send(0x93)
		data = self.read(0x93)

		# Status information, Temperature, charger status, load status
		self.send(0x94)
		data = self.read(0x94)
		self.bat_temp = self.twoBytes(data, 1)

		# Individual Cell voltages
		self.send(0x95)
		data = self.read(0x95)
		self.volt_cell1 = self.twoBytes(data, 0)
		# self.volt_cell2 =
		# self.volt_cell3
		# self.volt_cell4
		# self.volt_cell5
		# self.volt_cell6
		# self.volt_cell7
		# self.volt_cell8
		# self.volt_cell9
		# self.volt_cell10
		# self.volt_cell11
		# self.volt_cell12
		# self.volt_cell13
		# self.volt_cell14
		# self.volt_cell15
		# self.volt_cell16

		# Individual Cell Temp
		self.send(0x96)
		data = self.read(0x96)

		# Cell equilibrium state
		self.send(0x97)
		data = self.read(0x97)
		bal_status_1_8 = self.oneByte(0)
		bal_status_9_16 = self.oneByte(1)

		# BMS Errors
		self.send(0x98)
		data = self.read(0x98)

	def infoprint(self):
		print ("voltage: ", self.voltage)
		print("current: ", self.current)
		print("soc: ", self.soc)
		print("max cell voltage: ", self.bat_maxv)
		print("max cell no: ", self.bat_maxc)
		print("min cell voltage: ", self.bat_minv)
		print("min cell no: ", self.bat_minc)
		print("Battery Temp", self.bat_temp)
		print("Cell 1 Voltage", self.volt_cell1)

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

	def read(self, command):
		ser_bytes = bytearray(self.ser.read(13))
		print("Read: ", " ".join("{:02x}".format(thisByte) for thisByte in ser_bytes))
		if self.checkReadCheckSum(command ,ser_bytes):
			return ser_bytes
		else:
			raise Exception('Read Checksum failed')

	def checkReadCheckSum(self, command, ser_bytes):
		checksum = sum(ser_bytes[0:-1])
		#print("RCheckSum: ",hex(checksum))
		return ((ser_bytes[0] == 0xa5) & (ser_bytes[1] == 0x01) & (ser_bytes[2] == command) & (ser_bytes[3] == 0x08) & (ser_bytes[12] == (checksum  % 0x100 )))

	def twoBytes(self, ser_bytes,offset):
	        # print("Packing 2 bytes as int")
	        data = ser_bytes[offset + 4: offset +6]
	        # print("Data: ", " ".join("{:02x}".format(thisByte) for thisByte in data))
	        value = int.from_bytes(data, byteorder='big', signed=False)
	        # print(value)
	        return value

	def oneByte(self,ser_bytes,offset):
		#print("Packing 1 byte as int")
		data = ser_bytes[offset + 4: offset +5]
		#print("Data: ", " ".join("{:02x}".format(thisByte) for thisByte in data))
		value = int.from_bytes(data, byteorder='big', signed=False)
		#print(value)
		return value

if __name__ == '__main__':
	import serial.rs485
	ser = serial.rs485.RS485(port='/dev/ttyUSB0', baudrate=9600, timeout=5)
	ser.rs485_mode = serial.rs485.RS485Settings()
	bms = DalyBms(ser)
	bms.update()
	bms.infoprint()
