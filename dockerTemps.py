import os
import glob
import subprocess
import calendar
import time
import urllib2
import json
from apixu.client import ApixuClient, ApixuException
from firebase import firebase

# initialize apixuclient
api_key = os.getenv('TEMP_API_KEY')
client = ApixuClient(api_key)

#initialize
#os.system('modprobe w1-gpio')
#os.system('modprobe w1-therm')

#device
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

# Opens raw device, code changed to reflect issue in Raspian
def read_temp_raw():
    catdata = subprocess.Popen(['cat',device_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out,err = catdata.communicate()
    out_decode = out.decode('utf-8')
    lines = out_decode.split('\n')
    return lines
# Reads temperature, outputs farenhiet
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_f

weather = client.getCurrentWeather(q='22304')

data_time = calendar.timegm(time.gmtime())
measured_temp = read_temp()
temp_f = weather['current']['temp_f']  # show temprature in f

auth=os.getenv('TEMP_EXPLICIT_AUTH')
uid=os.getenv('TEMP_UID')
url=os.getenv('TEMP_FIREBASE_URL')

auth = firebase.FirebaseAuthentication(auth, 'Ignore', extra={'explicitAuth': auth, 'uid':uid })
print auth.extra

firebase = firebase.FirebaseApplication(url, auth)

print temp_f
print measured_temp
print data_time
results = firebase.post('readings', data={'current_temp': temp_f, 'measured_temp':measured_temp, 'time':data_time}, params={'print': 'pretty'} )
print results
