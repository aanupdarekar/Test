# -*- coding: utf-8 -*-
"""
Created on Sun Dec  5 23:22:08 2021

@author: prerana
"""

"""
import csv
with open('RetailStoreItemData.csv', newline='') as csvfile:""
    spamreader = csv.reader(csvfile, delimiter=',')#, quotechar='|')
    #print(spamreader)
    for row in spamreader:
        print(row)
        print(', '.join(row))
#myDataFile = open("RetailStoreItemData.txt","rt")

"""
from Class import Store # import Store
#from Class import User 
from datetime import date 
    
if __name__ == "__main__":
    #print("inside main")
    shouldContinue = True
   
    myStore = Store('RetailStoreItemData.csv', 'ReplinishmentOrders.csv', 'Sales.csv')    
    myStore.loadCredentials('credentials.csv')
   
    #myStore.generateReceipt('1002')
    
    loginCount=1
    userTries={}
    
    while(loginCount<=3):
        #loginCount=loginCount+1
        loginCount=1
        print("\n-------Welcome to the POS System-------\n")
        userId = input("Please enter userid: ")
        password = input("Please enter password: ")
        
        loginResult = myStore.validateUser(userId, password)
        if loginResult == True:
            shouldContinue = True
            break
        elif loginResult == False and userId not in userTries.keys():
            userTries.update({userId: 1})
            #print(userTries)
        elif loginResult == False and userId in userTries.keys():
            userTries[userId] = userTries[userId]+1
            #print(userTries) 
            if userTries[userId]>=3: #Login result is false and three attempts done
                print("You have exceeded maximum number of tries. Your account is locked. Contact system admin.")
                myStore.lockUser(userId)
                shouldContinue = False
    
    #Login is successful
    while(shouldContinue==True):
        print("Please select an option: ")
        print("1 = New Sale    2 = Return item/s    3 = Backroom Operations    9 = Exit Application")
        mainOption = int(input())
        if mainOption==1:
            
            print("You selected New Sale")
            myStore.newSale(userId)
            ##########
        elif mainOption==2:
            print("You selected Return Item/s")
            myStore.returnItem()
            
            ##########
        elif mainOption==3:
            print("You selected Backroom Operations")
            print("Please select an option: ")
            print("1 = Create orders for Replinishment    2 = Print Inventory report    3 = Create today's Item Sold report    9 = Exit")
            boOption = int(input())
            if boOption==1:
                print("Status of orders as of " +str(date.today()))
                myStore.replinishmentOrders(userId)
                
            elif boOption==2:
                print("Inventory report as of "+str(date.today()))
                myStore.printInventoryReport()
                
            elif boOption==3:
                print("Sale report for "+str(date.today()))
                myStore.printSaleReport()
                
                pass
            elif boOption==9:
                break
                
            ##########
        elif mainOption==9:
            print("Exiting..Good bye")
            break
        else:
            print("Invalid value. Try again")
            shouldContinue = True
