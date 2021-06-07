from telnetlib import Telnet
import time

class Microhard():
    """ 
    Bu sınıf, Microhard pDDL900 haberlesme modulu ile Ethernet arayuzu uzerinden 
    Telnet Protokolunu kullanarak konfigurasyon yapılması icin olusturulmustur. 
    
    Baslıklar(Attributes)
    -----------
    host : str
        Microhard IP adresi. 
        Fabrika ayarlarinda varsayilan: 192.168.168.1
    username : str
        Microhard cihazina erisim icin kullanilan kullanici adi. 
        Fabrika ayarlarinda varsayilan: admin 
    password : str
        Microhard cihazina erisim icin kullanilan sifre. 
        Fabrika ayarlarinda varsayilan: admin

    Metodlar
    ----------
    connect(host)
        Microhard ile baglantiyi kurar.
    get_status()
        Bagli olan Microhard’in anlik durum bilgisini alan metoddur.
        Bu metod ile Microhard’in bazi ozellikleri alinir.
    disconnect()
        AT komutu ekranından çıkar ve giriş ekranına geri döner.
    radio_on()
        Bu metod ile yapilan konfigurasyonlara gore kablosuz haberlesme acilir.
    radio_off()
        Bu metod ile kablosuz haberlesme kapatilir.
    set_frequency(freq)
        Microhard'larin haberlesmesi icin calisma frekansi ayarlanir.
        freq parametresi 906 ile 924 arasinda olmalidir.
    get_frequency()
        Microhard'in haberlestigi frekans degeri alinir.
    reboot()
        Microhard yeniden baslatilir. 
        Bu metod icin haberlesmenin saglaniyor olmasi gerekir.
    get_snr()
        Anlik SNR degeri alinir.
    get_datarate()
        Anlik datarate olculur.
    get_rssi()
        Anlik RSSI degeri alinir.
    set_txpower(tx_power) 
        Verici Microhard'in cikis gucu ayarlanir.  
        tx_power parametresi 7 ile 30 arasinda olmalidir. 
    get_txpower()
        Verici Microhard'in cikis gucunu dondurur.
    """
    def __init__(self,host,username,password):
        # init() metodu, Telnet Protokolü 
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
            raise ValueError
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
        if tx_power > 30 or tx_power < 7:
            print("Power must be in range: [7,30]")
            raise ValueError
        self.tx_power=tx_power
        cmd="AT+MWTXPOWER="+str(tx_power)+"\n"
        self.tn.write(cmd.encode('ascii'))
        self.tn.read_until(b"OK")
        return True
    
    def get_txpower(self):
        return self.tx_power


