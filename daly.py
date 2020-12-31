#!/usr/bin/env python3

import serial.rs485

import struct

def send(command):
	checksum = 0xa5 + 0x40 + command + 0x08
	print("Checksum: ",hex(checksum)) #checksum mod 256 to get lower byte
	hexs = "a5 40 {:02X} 08 00 00 00 00 00 00 00 00 {:02X}".format(command, (checksum  % 0x100 ))
	print("Write: " ,hexs)
	#print(hex(256))
	ser.write(bytearray.fromhex(hexs))

def read(command):
	ser_bytes = bytearray(ser.read(13))
	#ser_bytes = bytearray.fromhex("a5 40 90 08 02 10 00 00 00 00 00 00 8F")
	print("Read: ", " ".join("{:02x}".format(thisByte) for thisByte in ser_bytes))
	checksum = sum(ser_bytes[0:-1])
	print("CheckSum: ",hex(checksum))
	if ((ser_bytes[0] == 0xa5) & (ser_bytes[1] == 0x01) & (ser_bytes[2] == command) & (ser_bytes[3] == 0x08) & (ser_bytes[12] == (checksum  % 0x100 ))):
		print("Serial Cheksum passed")
	else:
		print("Serial Checksum failed")
	return ser_bytes

def twoBytes(ser_bytes,offset):
        #print("Packing 2 bytes as int")
        data = ser_bytes[offset + 4: offset +6]
        #print("Data: ", " ".join("{:02x}".format(thisByte) for thisByte in data))
        value = int.from_bytes(data, byteorder='big', signed=False)
        #print(value)
        return value

def oneByte(ser_bytes,offset):
	#print("Packing 2 bytes as int")
	data = ser_bytes[offset + 4: offset +5]
	#print("Data: ", " ".join("{:02x}".format(thisByte) for thisByte in data))
	value = int.from_bytes(data, byteorder='big', signed=False)
	#print(value)
	return value

		

ser=serial.rs485.RS485(port='/dev/ttyUSB0',baudrate=9600,timeout=5) 
ser.rs485_mode = serial.rs485.RS485Settings() 
send(0x90) 
data = read(0x90) 
voltage = twoBytes(data,0)/10.0 
print ("voltage: ", voltage) 
current = ((twoBytes(data,4) - 30000) / 10.0) # leave as uint but 2's complement should be correct in binary anyway...
print("current: ",current)
soc = (100 - (twoBytes(data,6)/10.0)) 
print("soc: ", soc)
    
send(0x91)
data = read(0x91)
bat_maxv = twoBytes(data,0) /1000.0
bat_maxc = oneByte(data,2)
bat_minv = twoBytes(data,3) /1000.0
bat_minc = oneByte(data,5)
print("max cell voltage: ",bat_maxv)
print("max cell no: ",bat_maxc)
print("min cell voltage: ", bat_minv)
print("min cell no: ", bat_minc)
