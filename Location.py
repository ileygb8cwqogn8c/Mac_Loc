import re
import os
import json
import urllib.request


ipRegex = re.compile("^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$")
macRegex = re.compile("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$")




# Getting location via IP Address

def Location(Value, ip=''):
 try:
  result = urllib.request.urlopen(f'http://ip-api.com/json/{ip}').read().decode('utf-8')
 except:
  return None
 else:
  result = json.loads(result)
  return result[Value]



def GetDefaultGateway():
    cmd = "chcp 65001 && ipconfig | findstr /i \"Default Gateway\""
    res = os.popen(cmd).read()

    for word in res.split(' '):
        if word and ipRegex.match(word):
            return word.replace("\n", '')

gateway=GetDefaultGateway()


def GetMacByIP(ip):
    _ = os.popen(f"arp -a {ip}").read()
    f = _.find("Physical Address")
    o = _[f:].split(' ')
    for _ in o:
        if macRegex.match(_):
            return _.replace('-', ':')



def GetLocationByBSSID(bssid):
    try:
        result = urllib.request.urlopen(f"http://api.mylnikov.org/geolocation/wifi?bssid={bssid}").read().decode('utf8')
    except:
        Logging('GetLocationByBSSID')
    else:
        result = json.loads(result)
        return result["data"]


data = GetLocationByBSSID(GetMacByIP(''))
lat = data['lat']
lon = data['lon']

print('Location')
print('\n')
print('IP Address » '+Location('query'))
print('Country » '+Location('country'))
print('City » '+Location('city'))
print('\n')
print('Latitude » '+str(data['lat']))
print('Longitude » '+str(data['lon']))
print('Range » '+str(data['range']))
print('\n')
print('BSSID » '+GetMacByIP(''))


