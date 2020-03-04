import requests
import json
from multiprocessing import Process
import time
import datetime
import RPi.GPIO as GPIO

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)

red = 17
blue = 27
yellow = 22

GPIO.setup(17,GPIO.OUT)
GPIO.setup(27,GPIO.OUT)
GPIO.setup(22,GPIO.OUT)



def get_next_bus():
    payload = {"rt": "73", "key": "", "stpid": "4051", "top": "1","format": "json"}
    r = requests.get("http://ctabustracker.com/bustime/api/v2/getpredictions", params=payload)

    responses = r.json()
    print("********************")
    print(responses)
    print("********************")

    #if responses['bustime-response']['error'][0]['msg'] == 'No arrival times':
        #next_bus_due_time = 'None'
     
        #Example response:
        #{'bustime-response': {'prd': [{'tmstmp': '20191006 18:40', 'typ': 'A', 'stpnm': 'Armitage & Albany',
        #'stpid': '4051', 'vid': '1960', 'dstp': 13967, 'rt': '73', 'rtdd': '73', 'rtdir': 'Eastbound',
        #'des': 'Clark/North', 'prdtm': '20191006 18:53', 'tablockid': '73 -802', 'tatripid': '65', 'dly': False,
        #'prdctdn': '12', 'zone': ''}]}}
        #{'bustime-response': {'error': [{'rt': '73', 'stpid': '4051', 'msg': 'No service scheduled'}]}}
    
    #No arrival times
    #{'bustime-response': {'error': [{'rt': '73', 'stpid': '4051', 'msg': 'No arrival times'}]}}

    #16
    #10:58:08.626844
    #{u'bustime-response': {u'prd': [{u'rt': u'73', u'rtdd': u'73', u'tmstmp': u'20191127 10:48', u'vid': u'1797', u'stpnm': u'Armitage & Albany', u'des': u'Clark/North', u'dstp': 17469, u'zone': u'', u'tablockid': u'73 -811', u'prdctdn': u'16', u'rtdir': u'Eastbound', u'tatripid': u'83', u'typ': u'A', u'dly': False, u'prdtm': u'20191127 11:14', u'stpid': u'4051'}]}}
    #____________________________
    #********************
    #{u'bustime-response': {u'error': [{u'msg': u'No arrival times', u'stpid': u'4051'}]}}
    #********************
    #Traceback (most recent call last):
    #  File "cta_get_predictions.py", line 120, in <module>
    #    run()
    #  File "cta_get_predictions.py", line 117, in run
    #    get_next_bus()
    #  File "cta_get_predictions.py", line 52, in get_next_bus
    #    next_bus_due_time = responses['bustime-response']['prd'][0]['prdctdn']

    # HANDLE API KEY ERROR
    # {u'bustime-response': {u'error': [{u'msg': u'Invalid API access key supplied'}]}
 
    #Possible responses: 'error', 'DLY', 'DUE', int
            #while int(next_bus_due_time) < 5:
            #GPIO.output(17,GPIO.HIGH)
            #time.sleep(0.5)
            #GPIO.output(17,GPIO.LOW)
            #time.sleep(0.5)
    response = responses['bustime-response']
    
    if list(response.keys())[0] == 'error':
        error = response['error']
        print("///////////////////////////////////////////")
        print(error)
        print("///////////////////////////////////////////")
    else:
    
        next_bus_due_time = responses['bustime-response']['prd'][0]['prdctdn']
        
        if next_bus_due_time == 'None':
            for _ in range(6):
                make_blinks(red)
                make_blinks(blue)
                make_blinks(yellow)
        elif next_bus_due_time == 'DLY':
            all_on()
            time.sleep(0.75)
            all_off()
        elif next_bus_due_time == 'DUE' or int(next_bus_due_time) < 4:
            for _ in range(4):
                make_blinks(red)
        elif int(next_bus_due_time) >= 10:
            for _ in range(4):
                make_blinks(yellow)
        elif 10 > int(next_bus_due_time) >= 4:
            for _ in range(4):
                make_blinks(blue)


        print("____________________________")
        print(next_bus_due_time)
        print(datetime.datetime.now().time())
        print(responses)
        print("____________________________")


def make_blinks(x):
    GPIO.output(x,GPIO.HIGH)
    time.sleep(0.075)
    GPIO.output(x,GPIO.LOW)
    time.sleep(0.075)


    
def red_on():
    GPIO.output(17,GPIO.HIGH)
    GPIO.output(27,GPIO.LOW)
    GPIO.output(22,GPIO.LOW)
    
def blue_on():
    GPIO.output(17,GPIO.LOW)
    GPIO.output(27,GPIO.HIGH)
    GPIO.output(22,GPIO.LOW)
    
def yellow_on():
    GPIO.output(17,GPIO.LOW)
    GPIO.output(27,GPIO.LOW)
    GPIO.output(22,GPIO.HIGH)
    
def all_on():
    GPIO.output(27,GPIO.HIGH)
    GPIO.output(17,GPIO.HIGH)
    GPIO.output(22,GPIO.HIGH)

def all_off():
    GPIO.output(17,GPIO.LOW)
    GPIO.output(27,GPIO.LOW)
    GPIO.output(22,GPIO.LOW)


def run():
    while True:
        get_next_bus()
        time.sleep(5)

run()

'''
if __name__ == '__main__':
    p1 = Process(target=
    '''