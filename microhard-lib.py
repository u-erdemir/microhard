from telnetlib import Telnet

class Microhard():
    def __init__(self,host,username,password):
        self.host = host
        self.username = username
        self.password = password
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
        print("Connection established")
        # Set timeout disabled
        self.tn.write(b"AT+MSCNTO=0\n")
        self.tn.read_until(b"OK")

        
    def disconnect(self):
        self.tn.write(b"ATA")
        return True
        
    def get_status(self):
        self.tn.write(b"AT+MWSTATUS\n")
        data = self.tn.read_until(b"OK")
        dec = data.decode('ascii').split('\r\n')
        self.frequency = int(dec[7].split(' ')[13])
        self.tx_power = int(dec[8].split(' ')[15])
        self.rx_byte = int(dec[11].split(" ")[10].split("B")[0])
        self.tx_byte = int(dec[13].split(" ")[9].split("B")[0])
        return dec
    
    def radio_on(self):
        self.tn.write(b"AT+MWRADIO=1\n")
        self.tn.read_until(b"OK")
        return True
        
    def radio_off(self):
        self.tn.write(b"AT+MWRADIO=0\n")
        self.tn.read_until(b"OK")
        return True
    
    def set_frequency(self, freq): #Extra parameter need to be added to set frequency
        self.tn.write(b"AT+MWFREQ900=freq\n")
        self.tn.read_until(b"OK")
        return True
    
    def get_frequency(self):
        asd = True
        return asd
    
    def reboot(self):
        # Attention !!! Reboot needs reconnection
        self.tn.write(b"AT+MSREB\n")
        return True
    
    def get_snr(self):
        self.tn.write(b"AT+MWSNR\n") 
        self.tn.read_until(b"OK")
        return True
    
    def get_datarate(self):
        asd = True
        return asd
    
    def get_rssi(self):
        self.tn.write(b"AT+MWRSSI\n") 
        self.tn.read_until(b"OK")
        return True
    
    def set_txpower(self,txpower):
        self.tn.write(b"AT+MWTXPOWER=txpower\n")
        self.tn.read_until(b"OK")
        return True
    
    def get_txpower(self):
        asd = True
        return True
    
a = Microhard("192.168.168.3","admin","hisar123")
data = a.get_status()

print(a.frequency)
print(a.tx_power)
print(data[13].split(" ")[9].split("B")[0])
print(data[13].split(" "))
