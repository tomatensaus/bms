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
		self.soc = self.twoBytes(data,6)/10.0
		self.D0x90 = data
		self.M90B0_1 = self.twoBytes(data, 0)
		self.M90B2_3 = self.twoBytes(data, 2)
		self.M90B4_5 = self.twoBytes(data, 4)
		self.M90B6_7 = self.twoBytes(data, 6)

		# Max / Min Cell voltages
		self.send(0x91)
		data = self.read(0x91)
		self.bat_maxv = self.twoBytes(data, 0) / 1000.0
		self.bat_maxc = self.oneByte(data, 2)
		self.bat_minv = self.twoBytes(data, 3) / 1000.0
		self.bat_minc = self.oneByte(data, 5)
		self.D0x91 = data
		self.M91B0_1 = self.twoBytes(data, 0)
		self.M91B2 = self.oneByte(data, 2)
		self.M91B3_4 = self.twoBytes(data, 3)
		self.M91B5 = self.oneByte(data, 5)

		# Individual cell temperatures
		self.send(0x92)
		data = self.read(0x92)
		self.bat_temp = self.oneByte(data,0) - 40
		self.D0x92 = data
		self.M92B0 = self.oneByte(data, 0)
		self.M92B1 = self.oneByte(data, 1)
		self.M92B2 = self.oneByte(data, 2)
		self.M92B3 = self.oneByte(data, 3)

		# Charge / Discharge Mos status
		self.send(0x93)
		data = self.read(0x93)
		self.D0x93 = data
		self.charge_stat = self.oneByte(data, 0)
		self.cycles = self.oneByte(data, 4)
		self.M93B0 = self.oneByte(data, 0)
		self.M93B1 = self.oneByte(data, 1)
		self.M93B2 = self.oneByte(data, 2)
		self.M93B3 = self.oneByte(data, 3)
		self.M93B4_7 = self.twoBytes(data, 4)

		# Status information, Temperature, charger status, load status
		self.send(0x94)
		data = self.read(0x94)
		self.D0x94 = data
		self.charge_cycles = self.twoBytes(data, 6)
		self.M94B0 = self.oneByte(data, 0)
		self.M94B1 = self.oneByte(data, 1)
		self.M94B2 = self.oneByte(data, 2)
		self.M94B3 = self.oneByte(data, 3)
		self.M94B4 = self.twoBytes(data, 4)
		self.M94B5_6 = self.oneByte(data, 6)

		# Individual Cell voltages
		self.cellVoltage = []
		self.send(0x95)
		self.D0x95 = data
		for i in range(6):
			data = self.readForCellVoltages(0x95)
			frame  = self.oneByte(data,0)
			#print(i," Frame: ", hex(frame))
			self.cellVoltage.append(self.twoBytes(data, 1))
			self.cellVoltage.append(self.twoBytes(data, 3))
			self.cellVoltage.append(self.twoBytes(data, 5))

		# Individual Cell Temp
		#self.send(0x96)
		#data = self.read(0x96)

		# Cell equilibrium state
		#self.send(0x97)
		#data = self.read(0x97)
		#bal_status_1_8 = self.oneByte(0)
		#bal_status_9_16 = self.oneByte(1)

		# BMS Errors
		#self.send(0x98)
		#data = self.read(0x98)

	def rawprintall(self):
		print(self.D0x90)
		print("0x90 byte 0-1:", self.M90B0_1)
		print("0x90 byte 2-3:", self.M90B2_3)
		print("0x90 byte 4-5:", self.M90B4_5)
		print("0x90 byte 6-7:", self.M90B6_7)

		print(self.D0x91)
		print("0x91 byte 0-1:", self.M91B0_1)
		print("0x91 byte 1:", self.M91B2)
		print("0x91 byte 3-4:", self.M91B3_4)
		print("0x91 byte 5:", self.M91B5)

		print(self.D0x92)
		print("0x92 byte 0:", self.M92B0)
		print("0x92 byte 1:", self.M92B1)
		print("0x92 byte 2:", self.M92B2)
		print("0x92 byte 3:", self.M92B3)

		print(self.D0x93)
		print("0x93 byte 0:", self.M93B0)
		print("0x93 byte 1:", self.M93B1)
		print("0x93 byte 2:", self.M93B2)
		print("0x93 byte 3:", self.M93B3)
		print("0x93 byte 4-7:", self.M93B4_7)

		print(self.D0x94)
		print("0x94 byte 0:", self.M94B0)
		print("0x94 byte 1:", self.M94B1)
		print("0x94 byte 2:", self.M94B2)
		print("0x94 byte 3:", self.M94B3)
		print("0x94 byte 4:", self.M94B4)
		print("0x94 byte 5-6:", self.M94B5_6)

		print(self.D0x95)
		# print(self.D0x96)
		# print(self.D0x97)
		# print(self.D0x98)

	def infoprint(self):
		print ("voltage: ", self.voltage)
		print("current: ", self.current)
		print("soc: ", self.soc)
		print("max cell voltage: ", self.bat_maxv)
		print("max cell no: ", self.bat_maxc)
		print("min cell voltage: ", self.bat_minv)
		print("min cell no: ", self.bat_minc)
		print("Battery Temp", self.bat_temp)
		print("Battery Cycles", self.charge_cycles)
		for i in range(len(self.cellVoltage)):
			print("Cell % 2d Voltage % 2f" %(i+1, self.cellVoltage[i]/1000.0))

	def sendCheckSum(self, command):
		checksum = 0xa5 + 0x40 + command + 0x08
		# print("WChecksum: ", hex(checksum))  # checksum mod 256 to get lower 2 bytes
		# print(hex(256))
		# print(hex(checksum % 0x100))
		return checksum % 0x100

	def send(self, command):
		hexs = "a5 40 {:02X} 08 00 00 00 00 00 00 00 00 {:02X}".format(command, self.sendCheckSum(command))
		# print("Write: " ,hexs)
		self.ser.write(bytearray.fromhex(hexs))

	def read(self, command):
		ser_bytes = bytearray(self.ser.read(13))
		self.readInfo = ("Read: ", " ".join("{:02x}".format(thisByte) for thisByte in ser_bytes))
		if self.checkReadCheckSum(command ,ser_bytes):
			return ser_bytes
		else:
			raise Exception('Read Checksum failed')
			print(str(Exception))

	def readForCellVoltages(self, command):
		ser_bytes = bytearray(self.ser.read(13))
		readCellInfo = ("Read: ", " ".join("{:02x}".format(thisByte) for thisByte in ser_bytes))
		if self.checkReadCheckSum(command, ser_bytes):
			return ser_bytes
		else:
			print(ser_bytes)
			raise Exception('Read Checksum failed')
			print(str(Exception))

	def checkReadCheckSum(self, command, ser_bytes):
		checksum = sum(ser_bytes[0:-1])
		#print("RCheckSum: ",hex(checksum))
		try:
			return ((ser_bytes[0] == 0xa5) & (ser_bytes[1] == 0x01) & (ser_bytes[2] == command) & (ser_bytes[3] == 0x08) & (ser_bytes[12] == (checksum  % 0x100 )))
		except IndexError as e:
			print(ser_bytes)
			print(str(e))

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

	def chargeDerate(self):
		trg_charge_V = TRG_CHARGE_V  # FROM INVERTER (mV)
		trg_charge_I = TRG_CHARGE_I  # FROM INVERTER (0.01A)

		self.bat_mode = 0
		self.bat_chg_v = 55.5
		self.bat_chg_i = 0.0
		# bat_mode_ms: time = 0 # milliseconds
		# bat_dis_i = BAT_DIS_I * 100U
		# bat_dis_v = BAT_DIS_V
		# derate_error_count: int = 0

		#Tests if battery is in a good state to accept charge
		while self.bat_mode == 0:
			if self.bat_maxv > 3600 or self.bat_temp > 60:  # Ensure bat_temp are decoded correctly
				trg_charge_I = 0

			time.sleep(60)
			if self.bat_maxv < 3300:
				trg_charge_V = 56.0
				trg_charge_I = 60.0
			elif self.bat_maxv > 3300 :
				trg_charge_V = 55.0
				trg_charge_I = 100 - self.soc


if __name__ == '__main__':
	import serial.rs485
	import time

	ser = serial.rs485.RS485(port='/dev/ttyUSB0', baudrate=9600, timeout=5)
	ser.rs485_mode = serial.rs485.RS485Settings()
	bms = DalyBms(ser)


	print("DALY BMS DATA COMMUNICATION PROGRAM")
	print("Press y for raw data only")
	answer = input()

	while True:
		bms.update()
		if answer == "y" or answer == "Y":
			bms.rawprintall()
		else:
			bms.infoprint()


		# time.sleep(300)

