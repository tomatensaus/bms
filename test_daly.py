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


