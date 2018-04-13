import serial,time,datetime
import pynmea2
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import pymysql as pms

gps_data= serial.Serial("COM12", 9600 , timeout=0.1) #COM port of GPS module.
gps_data.flush()
impact_data = serial.Serial("COM21", 9600 , timeout=0.1) #COM port of Arduino Nano.
impact_data.flush()

connection = pms.connect("localhost" ,"root" , "","accident_inf")
curs = connection.cursor()
curs.execute("TRUNCATE TABLE severity_data")

sever = 'no impact'
geolocator = Nominatim()
parsed = []
msg = 0
latit = longi = 0

while True:
    if(impact_data.inWaiting() > 0):
        data_impact = impact_data.readline()
        data_impact = data_impact.strip('\n')
        data_impact = data_impact.strip('\r')
        #print data_impact

        try:
            data_impact = int(data_impact)
            print data_impact
            if (data_impact < 100 and data_impact > 10):
                sever = 'low'
            elif (data_impact < 250 and data_impact > 10):
                sever = 'medium'
            elif (data_impact < 400 and data_impact > 10):
                sever = 'High'
            elif (data_impact < 800 and data_impact > 10):
                sever = 'Very High'
            elif (data_impact < 500 and data_impact > 10):
                sever = 'Maximum'
                
        except (ValueError or TypeError) :
            continue
        
        data_gps = gps_data.readline()
        if 'GPRMC' in data_gps:
            data_gps = data_gps.strip('\n')
            data_gps = data_gps.strip('\r')
            parsed.append(data_gps)
        for x in range(0,len(parsed)):            
            msg = pynmea2.parse(parsed[x])
            latit = msg.latitude
            longi = msg.longitude

        loc = str(latit) + ',' + str(longi)
        print loc
        msg = 0
        
        try:
            try:
                poa = str(geolocator.reverse(loc))
                poa = poa.split(',')
                for i in range(len(poa)):
                    try :
                        poa[i] = int(poa[i])
                        msg = 1
                        val = i
                        print poa[val]
                        
                    except (ValueError or TypeError) :
                        continue
            except TypeError:
                continue
            
        except GeocoderTimedOut as e:
            print("Error: geocode failed on input with message")
        

        time_now = str(datetime.datetime.now())
        if (msg == 1 and sever != 'no impact'):
            curs.execute("INSERT INTO severity_data(time,pincode,latitude,longitude,severity,google_maps) VALUES('"+str(time_now)+"',"+str(poa[val])+","+str(latit)+","+str(longi)+",'"+str(sever)+"','"+str("https://www.google.co.in/maps/@"+str(latit)+","+str(longi)+",17.21z")+"');")
            #print sever , data_impact
            sever = 'no impact'
            
        connection.autocommit(True)

        if len(parsed) > 15:
            parsed = []

        poa = []







