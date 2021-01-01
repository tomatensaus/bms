import unittest
import daly 

class DalyBmsTest(unittest.TestCase):
	def testSendCheckSum(self):
		bms = daly.DalyBms(None)
		self.assertEqual(bms.sendCheckSum(0x90), 0x7d)
		self.assertEqual(bms.sendCheckSum(0x91), 0x7e)
		self.assertEqual(bms.sendCheckSum(0x92), 0x7f)
		self.assertEqual(bms.sendCheckSum(0x93), 0x80)
		self.assertEqual(bms.sendCheckSum(0x94), 0x81)

	def testReadCheckSum(self):
		bms = daly.DalyBms(None)
		self.assertTrue(bms.checkReadCheckSum(0x90, bytearray.fromhex("a5 01 90 08 02 10 00 00 00 00 00 00 50")))
		self.assertTrue(bms.checkReadCheckSum(0x90, bytearray.fromhex("a5 01 90 08 02 10 00 00 aa 02 01 00 fd")))		
		self.assertFalse(bms.checkReadCheckSum(0x90, bytearray.fromhex("a5 01 90 08 02 10 00 00 00 00 00 00 51")))
		self.assertFalse(bms.checkReadCheckSum(0x90, bytearray.fromhex("a5 01 90 08 02 10 00 00 aa 02 01 00 ff")))
if __name__ == '__main__':
	unittest.main()

# Read:  a5 01 90 08 02 03 00 00 77 24 03 38 19
# Read:  a5 01 91 08 0c b7 07 0c 13 05 03 38 68
# Read:  a5 01 93 08 02 01 01 71 00 04 86 c0 00
# Read:  a5 01 94 08 10 01 00 00 02 00 05 c0 1a
# Read:  a5 01 95 08 01 0c aa 0c 95 0c 59 c0 c0

# Read:  a5 01 92 08 47 01 47 01 13 05 03 38 23
# Read:  a5 01 90 08 02 0a 00 00 75 eb 03 70 1d
# Read:  a5 01 91 08 0c d2 02 0c 67 05 03 70 0a
# Read:  a5 01 92 08 47 01 47 01 67 05 03 70 af
# Read:  a5 01 93 08 02 01 01 95 00 04 d5 80 33
# Read:  a5 01 94 08 10 01 00 00 02 00 05 80 da
# Read:  a5 01 95 08 01 0c cb 0c d3 0c aa 80 30

# Read:  a5 01 90 08 02 03 00 00 76 d0 03 2d b9
# Read:  a5 01 91 08 0c b7 0a 0b cb 05 03 2d 17
# Read:  a5 01 92 08 47 01 47 01 cb 05 03 2d d0
# Read:  a5 01 93 08 02 01 01 ad 00 04 77 48 b5
# Read:  a5 01 94 08 10 01 00 00 02 00 05 48 a2
# Read:  a5 01 95 08 01 0c a6 0c 9b 0c 4c 48 3d

# Read:  a5 01 90 08 02 03 00 00 77 2f 03 12 fe
# Read:  a5 01 91 08 0c b5 07 0c 15 05 03 12 42
# Read:  a5 01 92 08 49 01 49 01 15 05 03 12 03
# Read:  a5 01 93 08 02 01 01 91 00 04 51 50 7b
# Read:  a5 01 94 08 10 01 00 00 02 00 05 50 aa
# Read:  a5 01 95 08 01 0c 9f 0c 8e 0c 5d 50 42

Read:  a5 01 90 08 02 03 00 00 77 3e 03 1b 16
Read:  a5 01 91 08 0c b5 07 0c 28 05 03 1b 5e
Read:  a5 01 92 08 49 01 49 01 28 05 03 1b 1f
Read:  a5 01 93 08 02 01 01 a8 00 04 5d f8 46
Read:  a5 01 94 08 10 01 00 00 02 00 05 f8 52
Read:  a5 01 95 08 01 0c a3 0c 8f 0c 60 f8 f2

