import time

vu_ams = 'None'
AMS = None
# Marker
try:
	from ctypes import windll
	AMS = windll.amsserial # requires AmsSerial.dll !!!

	print('ECG driver is found')
	# global io
	# global AMS
except:
	print('windll is not supported')
	
try:
	for i in range(255):
		dev = 'COM%d' % (i+1) #as COM ports start from 1 on Windows
		AMS.Connect(dev.encode('utf-8'), 'AMS5fs'.encode('utf-8'))

		# Try to get VU-AMS Serial to check is a VU-AMS device is connected
		if(AMS.GetSerial()>0):
			print("connected to ", dev)
			vu_ams = dev
			break

		AMS.Disconnect()
	
except:
	print('### Failed to connect!')


def universal_marker(trigger):
	try:
		# io.DlPortWritePortUchar(port, trigger)
		AMS.SendCodedMarker(int(trigger))
		# AMS.SendBeepingCodedMarker(trigger)
	except:
		print('Failed to send universal trigger ' + str(trigger))

def test_sensor():
	if (vu_ams == "None"):
		print("VUAMS not connected")
	
	else:
		AMS.SendCodedMarker(10)
		time.sleep(5)
		AMS.SendBeepingCodedMarker(11)
		time.sleep(5)
		print("done, please unplug")

if __name__ == "__main__":
	test_sensor()
	