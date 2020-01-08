from tkinter import *
from tkinter import ttk
from tkinter import filedialog

import re
import mysql.connector



def addProc(path):

    #You may even, at a later stage, ask the user to enter time to be allocated per day for the application.

    mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root123",
    database="gim_0_2"
    )
    
    mycursor=mydb.cursor()

    
    procNamesFile=open(r"F:\My HP ProBook 4440s\Projects\Gaming in Moderation\Log files\procNamesFile.txt","r+")
    procList=[]
    procList=procNamesFile.readlines()
    print("\n File path: "+str(path))
        
    i=-1
    nm = []
    
    while path[i]!=r'/':    #Could have used split function too instead of this.
        #print(path[i])
        nm.append(path[i])
        i=i-1

    #print(nm)
    #print("nm type before join: "+str(type(nm)))
    nm="".join(nm)
    #print("nm type after join: "+str(type(nm)))

    l=int(-len(nm))
    finalnm=[]
    j=-1
    while j>=l:
        finalnm.append(nm[j])
        j=j-1
        
    finalnm="".join(finalnm)
    print("\n Final name: "+finalnm)

    #print(procList)

    procExistsFlag=0
    for proc in procList:
        #if str(proc)==finalnm:
        if re.search(finalnm,str(proc)):
            procExistsFlag=1
    
    if procExistsFlag==1:
        print("\n This application is already present in the GIM list.")
        procExistsFlag=0
    else:
        procNamesFile.write("\n"+str(finalnm))
        justnm=finalnm.split(".")
        #print(justnm[0])
        
        #sqlQ="ALTER TABLE log ADD COLUMN %s int"

        sqlQ="ALTER TABLE log ADD COLUMN "+justnm[0].strip()+" int"
        #print(sqlQ)
        
        #v=(str(justnm[0]),)
        #v=(finalnm,)
        #mycursor.execute(sqlQ,v)
        mycursor.execute(sqlQ)
    
 
class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.title("GIM - GetProcName")
        self.minsize(640, 400)
        #self.wm_iconbitmap('icon.ico')
 
        #self.labelFrame = ttk.LabelFrame(self, text = "Select the .exe file:")
        #self.labelFrame.grid(column = 0, row = 1, padx = 20, pady = 20)
 
        self.button()
 
 
 
    def button(self):
        self.button = ttk.Button(self, text = "Browse",command = self.fileDialog)
        self.button.grid(column = 1, row = 1)
 
 
    def fileDialog(self):
 
        self.filename = filedialog.askopenfilename(initialdir =  "C://", title = "Select A File", filetype =
        (("jpeg files","*.jpg"),("all files","*.*")) )
        self.label = ttk.Label(self, text = "")
        self.label.grid(column = 1, row = 2)
        self.label.configure(text = self.filename)
        #self.button = Button(self, text="Ok", command=addProc(self.filename))
        command=addProc(self.filename)

 
 
root = Root()
root.mainloop()
