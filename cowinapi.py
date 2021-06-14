import requests, json, time, os, csv
from datetime import datetime
from twilio.rest import Client

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
url="https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"
account_sid = "****************" #Twilio Credentials
auth_token = "****************"#Twilio Credentials
client = Client(account_sid, auth_token)

def do():
 d1 = datetime.today().strftime("%d-%m-%Y")
 p={"district_id":123,"date":d1}#Getting data for first district
 response=requests.get(url,params=p)
 myjson=json.loads(response.content)
 mylist=myjson["centers"]
 p={"district_id":456,"date":d1}#Getting data for second district
 response=requests.get(url,params=p)
 myjson=json.loads(response.content)
 for i in myjson["centers"]:
    mylist.append(i)
 with open(os.path.join(__location__, 'cowinapi.csv'),"a",newline='') as file:
     csvwriter=csv.writer(file)
     dt=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
     csvwriter.writerow(["Request Time",dt])
     places=[]
     total=0
     for i in mylist:
         ses=i["sessions"]
         for j in ses:
             if j["available_capacity"]>0 and j["min_age_limit"]==18:#Filter to print only non empty slots with min age 18 
                  print(j["date"],"|",j["vaccine"],"|",j["available_capacity"],"|",j[ "available_capacity_dose2"],"|",j["min_age_limit"],"|",i["name"])
                  csvwriter.writerow([i["name"],j["vaccine"],j["available_capacity"],j[ "available_capacity_dose2"],j["min_age_limit"]])
             if j["available_capacity_dose2"]>0 and  j["min_age_limit"]==18 and j["vaccine"]=="COVAXIN" and i["district_name"]=="Udham Singh Nagar" :#Filter to send sms only for a vaccine i want
                 places.append(i["name"])
                 total+=j["available_capacity_dose2"]
     if len(places)>0:
        mymessage=str(total)+" COVAXIN second doses for 18+ available at "+str(len(places))+" Centres, including "+places[0]
        message = client.messages \
        .create(body=mymessage, from_='+1**********',to='+91**********')
        print("SMS Sent")
#To add headers to csv (execute only once) 
# with open(os.path.join(__location__, 'cowinapi.csv'),"a",newline='') as file:
#  csvwriter=csv.writer(file)
#  csvwriter.writerow(["Name","Vaccine","Total","Dose 2","Age"])
while True:
    #Query evey minute
    print("Query Sent at",datetime.now().strftime("%H:%M:%S"))
    do()
    print("--------")
    time.sleep(60-time.time()%60)