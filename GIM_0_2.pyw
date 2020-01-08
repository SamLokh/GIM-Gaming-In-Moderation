from win32 import win32gui, win32process
#import win32ui, win32con, win32api
#import win32gui
import time
import psutil
import datetime
import re
import os
import shutil
import win32con
import stat

import mysql.connector

from win10toast import ToastNotifier

from elevate import elevate

#import notify2
#import Checkingprocesses
#import win32process


import ConstantMonitor
import TempCopy

import _thread


n=ToastNotifier()

time.sleep(15)

n.show_toast("GIM","GIM is up and running!",duration=8)

j=0
while j<1:
    for proc in psutil.process_iter(attrs=['pid', 'name', 'username']):
        if proc.info['name']=='mysqld.exe':
            j=2
            n.show_toast("GIM","MySQL is up and running!",duration=3)
            break
        #if proc.info['name']==nm:
            #pass
            #you can handle this condition later too, i.e. close the game until MySQL is not up and running.
        #else:
            #n.show_toast("GIM","MySQL is not yet up.",duration=3)
            

time.sleep(5)

mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root123",
    database="gim_0_2"
    )

mycursor=mydb.cursor()







def alive(nm):
    print("Inside alive function, nm: "+nm)
    for proc in psutil.process_iter(attrs=['pid', 'name', 'username']):
        if proc.info['name']==nm:
            return 1

    return 0


def getDate():
    todaysDate=str(datetime.date.today())
    #print("Today's Date: ",todaysDate)
    #n.show_toast("GIM","Today's Date: "+str(todaysDate),duration=3)
    return todaysDate

def countDown(appName):
    #appName=appTup[0]
    todaysDate=getDate()
    print("Inside countDown function.")
    global flagDictionary

    datePresentFlag=0

    justName=appName.split(".")
    justName=str(justName[0])
    print("justName: "+str(justName))
    
    sqlQuery1="SELECT Date FROM log"
    mycursor.execute(sqlQuery1)
    entries=mycursor.fetchall()
    for entry in entries:
        if re.search(todaysDate,str(entry)):
            #set flag
            datePresentFlag=1
            print("In entry entries")

            #sqlQuery3="SELECT %s FROM log WHERE Date='%s'"
            sqlQuery3="SELECT "+justName+" FROM log WHERE Date='"+todaysDate+"'"
            #print("sqlQuery3: "+sqlQuery3)
            #v3=(justName,todaysDate)
            #mycursor.execute(sqlQuery3,v3)
            mycursor.execute(sqlQuery3)
            res=mycursor.fetchone()
            dailyPool=res[0]
            print("dailyPool: "+str(dailyPool))

            if dailyPool==0:
                taskKillStatement='TASKKILL /F /IM '+appName
                os.system(taskKillStatement)
                #call delete folder function
                #TempCopy.dele()
                break

            while dailyPool>0:
                print("In the dailyPool while loop.")
                print("flagDictionary value: "+str(flagDictionary[appName]))
                #x=ConstantMonitor.alive()
                x=alive(appName)
                print("Value of x: "+str(x))
                if x=='1' or x==1:
                    print("So the task is alive!")
                    time.sleep(1)
                    #print(dailyPool)
                    dailyPool -= 1
                    tempPoolvar=dailyPool
                    if dailyPool==0:
                        taskKillStatement='TASKKILL /F /IM '+appName
                        os.system(taskKillStatement)
                        #call delete folder function
                        #TempCopy.dele()
                        break
                    
                    if dailyPool==600:
                        for proc in psutil.process_iter(attrs=['pid', 'name', 'username']):
                            if proc.info['name']==appName:
                                #switch task
                                #can use Auto Hot Key to execute alt+tab
                                
                                #print ("Warning! The Game is still running and your game time is about to come to an end!")
                                n.show_toast("GIM","Warning! The Game is still running and your game time is about to come to an end!",duration=15)

                    if tempPoolvar%500==0:
                        sqlQuery4="UPDATE log SET "+justName+"=%s WHERE Date=%s"
                        #sqlQuery4="UPDATE log SET "+justName+"="+str(tempPoolvar)+" WHERE Date="+todaysDate
                        v4=(tempPoolvar,todaysDate,)
                        mycursor.execute(sqlQuery4,v4)
                        #mycursor.execute(sqlQuery4)
                        mydb.commit()
                    
                else:
                    #print ("Task not alive anymore.")
                    n.show_toast("GIM","Task not alive anymore.",duration=3)
                    flagDictionary[appName]=0
                    break
            sqlQuery5="UPDATE log SET "+justName+"=%s WHERE Date=%s"
            #sqlQuery5="UPDATE log SET "+justName+"=%s WHERE Date="+todaysDate
            v5=(dailyPool,todaysDate,)
            #v5=(dailyPool)
            mycursor.execute(sqlQuery5,v5)
            #mycursor.execute(sqlQuery5)
            mydb.commit()
            flagDictionary[appName]=0
            return dailyPool

   
    if datePresentFlag==0:              #i.e. if todays date in not present in the table.
        #add date to the SQL table and initialise other columns
        sqlQuery2="INSERT INTO log VALUES ('"
        for i in range(0,appListLen):
            if i==0:
                sqlQuery2=sqlQuery2+todaysDate+"'"
            sqlQuery2=sqlQuery2+",7200"
            
        sqlQuery2=sqlQuery2+")"
        print(sqlQuery2)
        #v2=(todaysDate)
        mycursor.execute(sqlQuery2)
        mydb.commit()
        countDown(appName)
        
    flagDictionary[appName]=0
        
        
    




appNamesFile=open(r"F:\My HP ProBook 4440s\Projects\Gaming in Moderation\Log files\procNamesFile.txt","r+")
appList=[]
appList=appNamesFile.readlines()

flagDictionary={}
newAppList=[]

for app in appList:
    if app=="\n":
        continue
    app=app.split("\n")[0]
    #app=temp[0]
    newAppList.append(app)
    flagDictionary[app]=0

#print(flagDictionary)

appListLen=len(newAppList)

while True:
    #w=win32gui
    ##n.show_toast("GIM","GIM Task Started",duration=2)
    #nm=str(w.GetWindowText(w.GetForegroundWindow()))

    #print("In while True loop.")

    #flagThreadCreated=0

    flagDuplicate=0

    t=time.localtime()
    currentTime=time.strftime("%H:%M:%S",t)
    tempname=""
    for a in newAppList:
        for nm in psutil.process_iter(attrs=['pid', 'name', 'username']):
            #print(nm.info)
            #print(nm.info['name'])
            
            if a==nm.info['name'] and flagDictionary[a]==0:
                #if currentTime>="16:00:00" and currentTime<"23:59:59":
                if 1==1:
                    flagDictionary[a]=1
                    print("Starting a new thread.")
                    #flagThreadCreated=1
                    _thread.start_new_thread(countDown,(a,))
                    #print("About to execute the break statement.")
                    #flagDictionary[a]=0
                    print("Back in main.")
                    tempname=a
                    break
                else:   #Omae wa mou shindeiru :'D
                    taskKillStatement='TASKKILL /F /IM '+a
                    os.system(taskKillStatement)

            '''
            elif a==nm.info['name'] and flagDictionary[a]==1 and flagDuplicate==0:
                taskKillStatement='TASKKILL /F /IM '+a
                os.system(taskKillStatement)
                flagDuplicate=1
            '''     
            '''
            if nm.info['name']=='mysql.exe':        #Severe restriction
                mysqlCliKillStatement='TASKKILL /F /IM '+'mysql.exe'
                #print(mysqlCliKillStatement)
                os.system(mysqlCliKillStatement)
            
            if nm.info['name']=='rundll32.exe':     #Severe restriction
                datetimeSetKillStatement='TASKKILL /F /IM '+'rundll32.exe'
                os.system(datetimeSetKillStatement)
            '''
            '''
            if nm.info['name']=='Taskmgr.exe':     #Severe restriction
                taskmgrKillStatement='TASKKILL /F /IM '+'Taskmgr.exe'
                os.system(taskmgrKillStatement)
                '''
            

    #print("So that break statement just broke out of the innermost loop.")
    #flagDictionary[tempname]=0
