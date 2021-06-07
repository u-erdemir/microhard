from microhard_lib import Microhard

a = Microhard("192.168.168.3","admin","hisar123")
data = a.get_status()
# print(a.get_frequency())
# print(a.get_datarate())
# print(a.get_snr())
print(a.get_status())
