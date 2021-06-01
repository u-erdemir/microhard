from telnetlib import Telnet
import time

class Microhard():
    def __init__(self,host,username,password):
        self.host = host
        self.username = username
        self.password = password
        self.connect(self.host) 
        self.get_status()
        
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
        self.rx_byte = dec[11].split(" ")[10].split("B")[0]
        self.tx_byte = dec[13].split(" ")[9].split("B")[0]
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
        # Must be in range between 906 and 924
        if freq > 924 or freq < 906:
            print("Frequency must be in range: [906,924]")
            # raise ValueError
            return False
        self.frequency = freq
        data = int(freq - 902)
        cmd = "AT+MWFREQ900="+str(data)+"\n"
        self.tn.write(cmd.encode('ascii'))
        self.tn.read_until(b"OK")
        return True
    
    def get_frequency(self):
        return self.frequency
    
    def reboot(self):
        # Attention !!! Reboot needs reconnection
        self.tn.write(b"AT+MSREB\n")
        return True
    
    def get_snr(self):
        self.tn.write(b"AT+MWSNR\n") 
        data = self.tn.read_until(b"OK")
        dec = data.decode('ascii').split('\r\n')
        return dec
    
    def get_datarate(self):
        self.get_status()
        i_1=self.rx_byte
        time.sleep(3)
        self.get_status()
        i_2=self.rx_byte
        if i_1[-1]=='T' and i_2[-1]=='T':
            i_1=float(i_1[0:-1])*(2**40)
            i_2=float(i_2[0:-1])*(2**40)  
        elif i_1[-1]=='G' and i_2[-1]=='T':
            i_1=float(i_1[0:-1])*(2**30)
            i_2=float(i_2[0:-1])*(2**40)          
        elif i_1[-1]=='G' and i_2[-1]=='G':
            i_1=float(i_1[0:-1])*(2**30)
            i_2=float(i_2[0:-1])*(2**30)
        elif i_1[-1]=='M' and i_2[-1]=='G':
            i_1=float(i_1[0:-1])*(2**20)
            i_2=float(i_2[0:-1])*(2**30)
        elif i_1[-1]=='M' and i_2[-1]=='M':
            i_1=float(i_1[0:-1])*(2**20)
            i_2=float(i_2[0:-1])*(2**20)
        elif i_1[-1]=='K' and i_2[-1]=='M':
            i_1=float(i_1[0:-1])*(2**10)
            i_2=float(i_2[0:-1])*(2**20)
        elif i_1[-1]=='K' and i_2[-1]=='K':
            i_1=float(i_1[0:-1])*(2**10)
            i_2=float(i_2[0:-1])*(2**10)
        else:
            print('Run get_datarate command again!')        
        return str(round(((i_2-i_1)/3),2))+str("bps")
    
    def get_rssi(self):
        self.tn.write(b"AT+MWRSSI\n") 
        self.tn.read_until(b"OK")
        return True
    
    def set_txpower(self,tx_power):
        self.tx_power=tx_power
        cmd="AT+MWTXPOWER="+str(tx_power)+"\n"
        self.tn.write(cmd.encode('ascii'))
        self.tn.read_until(b"OK")
        return True
    
    def get_txpower(self):
        return self.tx_power
    
a = Microhard("192.168.168.3","admin","hisar123")
data = a.get_status()
# print(a.get_frequency())
print(a.get_datarate())
# print(a.get_snr())
# print(a.get_status())

