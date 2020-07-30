
import time
import json
import numpy as np
from datetime import datetime
#import serial

string_test = ';BattV =;12.79158,;TimeStamp =;07/26/2019 23:28:00,Pin=;11,12,13,14,15,;Resist=;NAN,1680.253,1794.383,1808.095,1797.62,;FullBr=;8.965633,4.643791,3.971472,5.544244,3.587611,;Tsensor=;-0.2163369,-0.2163369,22.43568,23.82773,19.471,;Psensor=;97.56838,-11.51234,2.347447,64.48346,36.25045,;PAR=;0.2451326,;SlrkW =;0,;Windspeed =;0.719861,;roomT =;19.09168,;roomRH =;83.39314,;\n'

A=-1.044e4
B=-11.29
C=-2.7e-2
D=1.289e-5
E=-2.478e-9
F=6.456
def get_all_data_sensor():
#    ser = serial.Serial(
#    port=r'/dev/ttyS0',
#    baudrate = 4800,
#    parity=serial.PARITY_NONE,
#    stopbits=serial.STOPBITS_ONE,
#    bytesize=serial.EIGHTBITS,
#    timeout=1.0)
 #   x= ser.readline()
#    x=ser.readline().decode('utf8')
##    x=ser.readline().decode('utf8')
#    ser.close()
    x=string_test
    dic_data={}
#    FullBr=np.array(liste[5].split(","))[:8].astype(np.float)
#    print(pin,Resist,FullBr)
    if len(x)==0:
        return(False,dic_data)
    else:
        liste=x.split(";")
        dic_data['BattCR6']=float(liste[2][:-1])
        timestring=liste[4]
        month=int(timestring[0:2])
        day=int(timestring[3:5])
        year=int(timestring[6:10])
        hour=int(timestring[11:13])
        minute=int(timestring[14:16])
        second=int(timestring[17:19])
        date=datetime(year,month,day,hour,minute,second)
        dic_data['timestamp']=date
        dic_data['BattV']=float(liste[2][:-1])
    #    dic_data['Ptemp_C']=float(liste[6][:-5])
        dic_data['pin']=np.array(liste[5].split(","))[:7].astype(np.float)
        dic_data['Resist']=np.array(liste[7].split(","))[:7].astype(np.float)
        dic_data['FullBr']=np.array(liste[9].split(","))[:7].astype(np.float)
        dic_data['Tsensor']=np.array(liste[11].split(","))[:7].astype(np.float)
        dic_data['Psensor']=np.array(liste[13].split(","))[:7].astype(np.float)
        dic_data['PAR']=float(liste[15].split(',')[0])
        dic_data['SlrkW']=float(liste[17].split(',')[0])
        dic_data['Windspeed']=float(liste[19].split(',')[0])
        dic_data['roomT']=float(liste[21].split(',')[0])
        dic_data['roomRH']=float(liste[23].split(',')[0])
        Te=dic_data['roomT']
        RH= dic_data['roomRH']
        SVD = 5.018+0.32321*Te+8.1847e-3*Te**2+3.1243e-4*Te**3
        VD=RH/100*SVD
        dic_data['VPD']=SVD-VD
        return(True,dic_data)
#    return(pin,Resist,FullBr)


    
def update_WP_sensor(pin):
    return([-1,-1])


