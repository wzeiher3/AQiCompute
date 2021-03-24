import random
import boto3
from itertools import count
from boto3.dynamodb.conditions import Key, Attr
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time
import threading
import numpy 


from env import AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY, AWS_REGION

dynamodb = boto3.resource('dynamodb', aws_access_key_id=AWS_ACCESS_KEY,
                            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                            region_name=AWS_REGION)

table = dynamodb.Table('AirQualityData')

plt.style.use('fivethirtyeight')



def animate(i):
    now=int(time.time())
    timestampold=now-1000
    response = table.scan(
        FilterExpression=Attr('timestamp').gt(timestampold)  
    )

    items = response['Items']

    with open('data.csv', 'w') as f:
        fieldNames = ['stationID', 'timestamp', 'latitude', 'pm2_5', 'so2', 'pm10', 'co', 'longitude']
        thewriter = csv.DictWriter(f, fieldnames=fieldNames)
        thewriter.writeheader()
        for item in items:
            thewriter.writerow({'stationID': item['payload']['stationID'],
                                'timestamp': item['payload']['timestamp'],
                                'latitude': item['payload']['latitude'], 
                                'pm2_5': item['payload']['pm2_5'],
                                'so2': item['payload']['so2'],
                                'pm10': item['payload']['pm10'],
                                'co': item['payload']['co'],
                                'longitude': item['payload']['longitude']}) 



    data = pd.read_csv('data.csv') 
    arr = numpy.array(data)

    mask1 = (arr[:, 0] == "ST102")
    st102 = arr[mask1, :]
    print(st102)
    print("BREAK")

    mask2 = (arr[:, 0] == "ST105")
    st105 = arr[mask2, :]
    print(st105)

    st102xVal = st102[:, 1]
    st102pm2_5Val = st102[:, 3]
    st102pm10Val = st102[:, 5]
    st102so2Val = st102[:, 4]
    st102coVal = st102[:, 6]


    st105xVal = st105[:,1]
    st105pm2_5Val = st105[:, 3]
    st105pm10Val = st105[:, 5]
    st105so2Val = st105[:, 4]
    st105coVal = st105[:, 6]

    x = st102xVal
    y = st102pm2_5Val

    plt.cla()
    plt.subplot(2, 4, 1)
    plt.plot(st102xVal, st102pm2_5Val, color='blue')
    plt.xlabel("Time")
    plt.ylabel("pm2_5")
    plt.title("ST102 pm2_5")
  
    plt.subplot(2, 4, 2)
    plt.plot(st102xVal, st102pm10Val, color='blue')
    plt.xlabel("Time")
    plt.ylabel("pm10")
    plt.title("ST102 pm10")

    
    plt.subplot(2, 4, 3)
    plt.plot(st102xVal, st102so2Val, color='blue')
    plt.xlabel("Time")
    plt.ylabel("so2")
    plt.title("ST102 so2")
    
    plt.subplot(2, 4, 4)
    plt.plot(st102xVal, st102coVal, color='blue')
    plt.xlabel("Time")
    plt.ylabel("co")
    plt.title("ST102 co")

    plt.subplot(2, 4, 5)
    plt.plot(st105xVal, st105pm2_5Val, color='blue')
    plt.xlabel("Time")
    plt.ylabel("pm2_5")
    plt.title("ST105 pm2_5")

    plt.subplot(2, 4, 6)
    plt.plot(st105xVal, st105pm10Val, color='blue')
    plt.xlabel("Time")
    plt.ylabel("pm10")
    plt.title("ST105 pm10")


    plt.subplot(2, 4, 7)
    plt.plot(st105xVal, st105so2Val, color='blue')
    plt.xlabel("Time")
    plt.ylabel("so2")
    plt.title("ST105 so2")


    plt.subplot(2, 4, 8)
    plt.plot(st105xVal, st105coVal, color='blue')
    plt.xlabel("Time")
    plt.ylabel("co")
    plt.title("ST105 co")



    plt.tight_layout()




# fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2, figsize=(15, 7))
ani = FuncAnimation(plt.gcf(), animate, interval=1000)


print("SHOW HERE")
plt.tight_layout()
plt.show()