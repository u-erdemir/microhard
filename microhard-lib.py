from telnetlib import Telnet

class Microhard():
    def __init__(self,host,username,password):
        """This """
        self.host = host
        self.username = username
        self.password = password
        """ Connection timeout can be disabled from Microhard WebUI
          System > Settings > Console Timeout(s)"""
        self.connect(self.host) 
        
    def connect(self,host):
        self.tn = Telnet(host)
        self.tn.read_until(b"login: ")
        self.tn.write(self.username.encode('ascii')+b"\n")
        if self.password:
            self.tn.read_until(b"Password: ")
            self.tn.write(self.password.encode('ascii') + b"\n")
        self.tn.write(b"AT\n")
        self.tn.read_until(b"OK")
        
    
    def get_status(self):
        self.tn.write(b"AT+MWSTATUS\n")
        data = self.tn.read_until(b"OK")
        dec = data.decode('ascii').split('\r\n')
        freq = dec[7]
        self.frequency = 1
        return dec

a = Microhard("192.168.168.3","admin","hisar123")
data = a.get_status()
frequency = data[7]
print(frequency)
