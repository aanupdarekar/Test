# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 17:28:17 2021

@author: prer
"""

import csv
#import pandas as pd
from datetime import date                      
from tabulate import tabulate

#Create user class
class User:
    def __init__(self, userid,password,locked):
        self.userId = userid
        self.password = password
        self.locked = locked
        
    def setLock(self,userid):
       locked = "TRUE"
    
    """
    def getLock():
        return self.Locked
    """
    
    def getUserId(self):
        return self.userid
    
                

# Create an Item class
class Item:
    def __init__(self, UPC, Description, Item_Max_Qty, Order_Threshold
                 , replinishment_order_qty, Item_on_hand, Unit_price
                 , Order_placed):
        self.upc = UPC
        self.description = Description
        self.itemMaxQty = Item_Max_Qty
        self.orderThreshold = Order_Threshold
        self.replinishmentOrderQty = replinishment_order_qty
        self.itemOnHand = Item_on_hand
        self.unitPrice = Unit_price
        self.orderPlaced = Order_placed
    def __str__(self): 
        return "Test  upc:% s desc:%s itemOnHand:%s " % (self.upc,self.description,self.itemOnHand) 
#Create Replinishment class
class Replinishment:
    def __init__(self,upc, description , orderQty, orderDate, orderedBy, status) :
        self.upc = upc
        self.description = description
        self.orderQty = orderQty
        self.orderDate = orderDate
        self.orderedBy = orderedBy
        self.status = status
 
#Create sale class
class Sale:
    def __init__(self,receiptno, upc, description, quantity, orderdate,itemPrice, orderedby):
        self.receiptNo = receiptno
        self.upc=upc
        self.description=description
        self.quantity=quantity
        self.orderDate=orderdate
        self.itemPrice=itemPrice
        self.orderedBy=orderedby

    def __str__(self): 
        return "Test receiptNo:% s upc:% s desc:%s quan:%s order:%s itemPrice:%s" % (self.receiptNo, self.upc,self.description,self.quantity,self.orderDate,self.itemPrice) 
        
        
 
#Create a Store class
class Store:
    itemsDictionary = {}
    userCredentialsDictionary = {}
    replinishmentOrdersDictionary = {}
    salesDictionary ={}
    
    def __init__(self,itemsFile,replinishmentFile, salesFile):
        self.itemsFile = itemsFile
        self.replinishmentFile = replinishmentFile
        self.salesFile = salesFile
        
        with open(itemsFile, newline='') as csvFile:
            lines = csv.reader(csvFile, delimiter=',')#, quotechar='|')
            #print(spamreader)
            count=0
            headings = next(lines)
            for row in lines:
                if len(row)>0:
                    #if count<=10:
                        count = count+1
                        #print(row)
                        #print(row[0], row[1])
                        #print(', '.join(row))
                        upc = row[0]
                        description = row[1]
                        itemMaxQty = int(row[2])
                        orderThreshold = int(row[3])
                        replinishmentOrderQty = int(row[4])
                        itemOnHand = int(row[5])
                        unitPrice = float(row[6])
                        orderPlaced = int(row[7] if row[7] else 0)
                                            
                        item = Item(upc, description, itemMaxQty, orderThreshold
                                    , replinishmentOrderQty, itemOnHand, unitPrice
                                    , orderPlaced)           
                        #print(item)
                        self.itemsDictionary.update({upc: item})    
            
        with open(replinishmentFile, newline='') as csvFile:
            lines = csv.reader(csvFile, delimiter=',')#, quotechar='|')
            
            headings = next(lines)
            for row in lines:
                if len(row)>0:
                    #if count<=10:
                        upc = row[0]
                        description = row[1]
                        orderQty = int(row[2])
                        orderDate = row[3]
                        orderedBy = row[4]
                        status =  row[5]
                        replinishmentOrder = Replinishment(upc, description
                                                                , orderQty, orderDate
                                                                , orderedBy, status)           
                        
                        self.replinishmentOrdersDictionary.update({upc: replinishmentOrder})    
            
        with open(salesFile, newline='') as csvFile:
            lines = csv.reader(csvFile, delimiter=',')#, quotechar='|')
            
            headings = next(lines)
            for row in lines:
                if len(row)>0:
                    #if count<=10:
                        receiptNo =  row[0]
                        upc = row[1]
                        description = row[2]
                        quantity = int(row[3])
                        orderDate = row[4]
                        itemPrice = row[5]
                        orderedBy =  row[6] if row[6] else ''
                        print( receiptNo, upc, description, quantity, orderDate, itemPrice,orderedBy)
                        sales = Sale(receiptNo, upc, description, quantity, orderDate, itemPrice,orderedBy)
                        salesKey = str(receiptNo)+str(upc) #key is a unique combination of both these
                        print(salesKey)
                        self.salesDictionary.update({salesKey: sales})    
            
            
    
    
    def getItem(self, upc):
        if upc == self.itemsDictionary.keys():
            return self.itemsDictionary.get(upc)
        else:
            return None
     
    ### User related methods    
    def loadCredentials(self,filename):
        #load the credentials file
        #print("Inside load cred")
        with open(filename, newline='') as csvfile:
                lines = csv.reader(csvfile, delimiter=',')
                next(lines)
                for row in lines:
                    userId = row[0]
                    password = row[1]
                    locked = "FALSE"
                    #print(userId,password,locked)
                    user = User(userId,password,locked)
                    self.userCredentialsDictionary.update({userId:user})            
     
    def validateUser(self,userid,enteredpassword):
        #print("inside validareuser")
        if userid in self.userCredentialsDictionary.keys():#user exists
            actualPassword = self.userCredentialsDictionary.get(userid)
            if actualPassword.locked == "FALSE": #Account not locked
                if enteredpassword == actualPassword.password: #password matches
                    #print("Login successful.")
                    return True
                else: #password doesnt match
                    print("Invalid password. Try again.")
                    return False
        
            else : #Account locked
                print("User is locked out. Contact system admin.")
                return False
    
        else: #user doesnt exist
            print("User doesnt exist. Try again.")
            return False
    
    def lockUser(self,userid):
        #print("inside lockuser")
        if userid in self.userCredentialsDictionary.keys():
            obj = self.userCredentialsDictionary.get(userid)
            obj.setLock(userid)
            
    
    ##### Sale related methods
    def generateReceipt(self,rcptNo):
        saleReceipt=[]
        countItems=0
        totalAmount =0
        
        for key, value in self.salesDictionary.items():
            #print(key) 
            #print(key,value)
            #print(self.salesDictionary.get(key).receiptNo)
            if rcptNo == self.salesDictionary.get(key).receiptNo:
                    
                #receiptNo = self.salesDictionary.get(key).receiptNo
                upc =  self.salesDictionary.get(key).upc
                description = self.salesDictionary.get(key).description
                quantity = self.salesDictionary.get(key).quantity
                orderDate = self.salesDictionary.get(key).orderDate
                itemPrice=self.salesDictionary.get(key).itemPrice
                linePrice=self.salesDictionary.get(key).itemPrice*self.salesDictionary.get(key).quantity
                # orderedBy = self.salesDictionary.get(key).orderedBy
                
                saleReceipt.append( [rcptNo, upc,description,quantity,orderDate,itemPrice,linePrice])
                countItems=countItems+1
                totalAmount=totalAmount+linePrice
                
        
        saleReceipt.append( ['', '','','','','',''])
        
        
        saleReceipt.append( [countItems, '','','','','',totalAmount])
        
        print(tabulate(saleReceipt, headers =["Receipt No","UPC","Description","Quantity","Date","Unit Price","Line Total"]))
            
    
    
    # New sale
    def newSale(self,userId):
        saleContinue = 'y'
        receiptNo = 10001
        fileLength = len(self.salesDictionary.items())
        
        newReceiptNo = receiptNo + fileLength
       # print("newReceiptno" +str(newReceiptNo))
        
       # print(receiptNo)
        
        while(saleContinue=='y'):
            #if count==1: #first item
            saleInput = int(input("1 = Sell an item    2 = Cancel aded item   9 = Complete sale \n"))
            if saleInput == 1:
                saleContinue = 'y'
                enteredUpc = input("Please enter the UPC: ")
                if enteredUpc in self.itemsDictionary.keys():#upc present
                        print("You entered "+self.itemsDictionary.get(enteredUpc).description)
                        enteredQty = int(input("Please enter Quantity: "))
                        if enteredQty<=self.itemsDictionary.get(enteredUpc).itemOnHand:#required quantity available
                            print("Unit price is $"+str(self.itemsDictionary.get(enteredUpc).unitPrice))
                            print("Total line amount is $"+str(self.itemsDictionary.get(enteredUpc).unitPrice*enteredQty))
                            
                                                        
                            remainingQty = self.itemsDictionary.get(enteredUpc).itemOnHand - enteredQty
                            self.itemsDictionary.get(enteredUpc).itemOnHand = remainingQty
                            
                             
                            salesKey = str(newReceiptNo)+str(enteredUpc)
                            #self.salesDictionary[salesKey]=salesKey
                            
                            
                            description=self.itemsDictionary.get(enteredUpc).description
                            itemPrice = self.itemsDictionary.get(enteredUpc).unitPrice
                            orderDate=date.today()
                            
                            self.salesDictionary[salesKey]= Sale(newReceiptNo,enteredUpc, description,enteredQty,orderDate,itemPrice, userId)
                            #print(self.salesDictionary )
                            
                            # If item on hand <= order threshold then ..
                            # replinishing order and triggering orderPlaced column if not 1
                            #if self.itemsDictionary.get(enteredUpc).itemOnHand<=self.itemsDictionary.get(enteredUpc).orderThreshold:
                            #   self.itemsDictionary.get(enteredUpc).orderPlaced = 1
                                                 
                            #updating Retail csv
                            with open(self.itemsFile, 'w', newline="") as csvfile:
                                writer = csv.writer(csvfile)#, fieldnames=fieldNames)
                                
                                #write header
                                writer.writerow(["upc", "description", "itemMaxQty"
                                                 , "orderThreshold" 
                                                 , "replinishmentOrderQty"
                                                 , "itemOnHand", "unitPrice"
                                                 , "orderPlaced"])
                                
                                #writing values
                                for key, value in self.itemsDictionary.items():
                                    row = [self.itemsDictionary.get(key).upc,
                                               self.itemsDictionary.get(key).description,
                                               self.itemsDictionary.get(key).itemMaxQty,
                                               self.itemsDictionary.get(key).orderThreshold,
                                               self.itemsDictionary.get(key).replinishmentOrderQty,
                                               self.itemsDictionary.get(key).itemOnHand, 
                                               self.itemsDictionary.get(key).unitPrice,
                                               self.itemsDictionary.get(key).orderPlaced
                                            ]   
                                    writer.writerow(row)
                                
                            
                           
                            
                            ######add to sale csv
                            with open(self.salesFile, 'a', newline="") as csvfile:
                                lines = csv.writer(csvfile)#, fieldnames=fieldNames)
                                                            
                                #writing values
                                for key, value in self.salesDictionary.items():
                                    row = [self.salesDictionary.get(key).receiptNo,
                                               self.salesDictionary.get(key).upc,
                                               self.salesDictionary.get(key).description,
                                               self.salesDictionary.get(key).quantity,
                                               self.salesDictionary.get(key).orderDate,
                                               self.salesDictionary.get(key).itemPrice,
                                               self.salesDictionary.get(key).orderedBy
                                            ]   
                                    lines.writerow(row)
                                
                                                       
                        else:
                            print("Cannot add quantity. The quantity available is "
                                   +str(self.itemsDictionary.get(enteredUpc).itemOnHand))
                            
                else: #upc not present
                    print("Invalid UPC. Try again.")
                saleContinue = 'y'
                            
            
            elif saleInput == 2:
               #Cancel/ return  an item
                self.returnItem()
            
           
            elif saleInput==9:
                
                saleContinue = 'n'
                print("Generating receipt")
                #########call method here to Generate receipt
                self.generateReceipt(newReceiptNo)
                
            else:
                print("Invalid input. Try again.")
                saleContinue = 'y'
             
                    
    def returnItem(self):
       returnOption = int(input("1 = Return few items   2 = Return all items   9 = Exit \n"))
       
       shouldContinue = 'y'
       continueReturn ='y'
       countItems = 0
       
       if returnOption==1  :#return few items
           enteredReceiptNo = input("Please enter the receipt number: ")
          
           for key, value in self.salesDictionary.items():
                if enteredReceiptNo == self.salesDictionary.get(key).receiptNo:
                    shouldContinue='y'
                    break
                else:
                    shouldContinue='n'
                    
                    
           if shouldContinue == 'n':
               print("Invalid receipt number.Try again")
          
          #receipt present
                         
           while(shouldContinue == 'y'):
               enteredUpc = input("Please enter UPC to be returned: ")
               isUpcFound=False
               for key, value in self.salesDictionary.items():
                  
                   if enteredUpc == self.salesDictionary.get(key).upc and enteredReceiptNo == self.salesDictionary.get(key).receiptNo:
                                print(self.salesDictionary.get(key))
                                isUpcFound=True
                                shouldContinue='n'
                            #return can be processed
                                countItems = countItems+1
                                print("You entered " + self.salesDictionary.get(key).description)
                                while(True):
                                    enteredQuantity = int(input("Please enter quantity: "))
                                    if enteredQuantity <= self.salesDictionary.get(key).quantity:
                                        returnAmount = self.salesDictionary.get(key).itemPrice*enteredQuantity
                                        print("Return amount: $" +str(returnAmount))
                                        break
                                    else:
                                        print("Invalid Quantity selection. Try again.")
                                
                                #changes in salesDictionary and csv
                                self.salesDictionary.get(key).quantity = self.salesDictionary.get(key).quantity - enteredQuantity
                                #self.salesDictionary.get(key).lineTotal = self.salesDictionary.get(key).lineTotal - returnAmount
                                
                                #changes in itemsDictioanry
                                if enteredUpc in self.itemsDictionary:
                                        print( self.itemsDictionary.get(enteredUpc))
                                        self.itemsDictionary.get(enteredUpc).itemOnHand = self.itemsDictionary.get(enteredUpc).itemOnHand+enteredQuantity
                                else:    
                                    print("ERROR: Entered UPC doesnt exist in Retail file.")
                                    break    
                                #changes in sales.csv
                                with open(self.salesFile, 'w', newline="") as csvfile:
                                    lines = csv.writer(csvfile)#, fieldnames=fieldNames)
                                    #headings = next(lines)
                                    #write header
                                    lines.writerow(["receiptNo","upc", "description", "quantity", "orderDate" , "itemPrice", "orderedBy"])
                                                       
                                    #write rows if order not present already
                                    #checking orderPlaced column in items and if order is not fulfilled in replinishedmentorders
                                    for key,values in self.salesDictionary.items():
                                        row = [self.salesDictionary.get(key).receiptNo,
                                                   self.salesDictionary.get(key).upc,
                                                   self.salesDictionary.get(key).description,
                                                   self.salesDictionary.get(key).quantity,
                                                   self.salesDictionary.get(key).orderDate,
                                                   self.salesDictionary.get(key).itemPrice,
                                                   self.salesDictionary.get(key).orderedBy
                                                   ]
                                        lines.writerow(row)
                                
                                #changes in retail csv
                                with open(self.itemsFile, 'w', newline="") as csvfile:
                                    lines = csv.writer(csvfile)#, fieldnames=fieldNames)
                                    
                                    #write header
                                    lines.writerow(["upc", "description", "itemMaxQty", "orderThreshold" , "replinishmentOrderQty", "itemOnHand","unitPrice","orderPlaced"])
                                   
                                    for key, value in self.itemsDictionary.items():
                                        row = [self.itemsDictionary.get(key).upc,
                                                   self.itemsDictionary.get(key).description,
                                                   self.itemsDictionary.get(key).itemMaxQty,
                                                   self.itemsDictionary.get(key).orderThreshold,
                                                   self.itemsDictionary.get(key).replinishmentOrderQty,
                                                   self.itemsDictionary.get(key).itemOnHand, 
                                                   self.itemsDictionary.get(key).unitPrice,
                                                   self.itemsDictionary.get(key).orderPlaced
                                                ]   
                                        lines.writerow(row)
                                
                                continueReturn = input("Return another item?(y/n) :")
                                if continueReturn=='y':
                                    shouldContinue = 'y'
                                else:
                                    print(str(countItems)+" items returned for " +enteredReceiptNo)
                                    break 

               if not isUpcFound:
                    print("Invalid UPC. Try again.")
                    shouldContinue = 'y'
                                
                            
       elif returnOption == 2:# return all items
           enteredReceiptNo = input("Please enter the receipt number: ")
           shouldReturnAll = input("Are you sure you want to return all items? y=yes,n=no ")
           if shouldReturnAll == 'y':
                receiptNumberFound =False
                for key, value in self.salesDictionary.items():
                        if enteredReceiptNo == self.salesDictionary.get(key).receiptNo:
                            receiptNumberFound=True
                            returnedUpc=self.salesDictionary.get(key).upc
                            returnedQuantity =self.salesDictionary.get(key).quantity
                            if not returnedQuantity == 0:
                                returnAmount = self.salesDictionary.get(key).itemPrice*returnedQuantity
                                print("You entered " + self.salesDictionary.get(key).description)
                                print("Return amount: $" +str(returnAmount))
                                #changes in salesDictionary
                                self.salesDictionary.get(key).quantity=0    
                                
                                if returnedUpc in self.itemsDictionary:
                                            print( self.itemsDictionary.get(returnedUpc))
                                            self.itemsDictionary.get(returnedUpc).itemOnHand = self.itemsDictionary.get(returnedUpc).itemOnHand+returnedQuantity
                                else:    
                                        print("ERROR: Entered UPC doesnt exist in Retail file.")
                                        break    

                                #changes in sales.csv
                                with open(self.salesFile, 'w', newline="") as csvfile:
                                    lines = csv.writer(csvfile)#, fieldnames=fieldNames)
                                    #headings = next(lines)
                                    #write header
                                    lines.writerow(["receiptNo","upc", "description", "quantity", "orderDate" , "itemPrice", "orderedBy"])
                                                       
                                    #write rows if order not present already
                                    #checking orderPlaced column in items and if order is not fulfilled in replinishedmentorders
                                    for key,values in self.salesDictionary.items():
                                        row = [self.salesDictionary.get(key).receiptNo,
                                                   self.salesDictionary.get(key).upc,
                                                   self.salesDictionary.get(key).description,
                                                   self.salesDictionary.get(key).quantity,
                                                   self.salesDictionary.get(key).orderDate,
                                                   self.salesDictionary.get(key).itemPrice,
                                                   self.salesDictionary.get(key).orderedBy
                                                   ]
                                        lines.writerow(row)
                                
                                #changes in retail csv
                                with open(self.itemsFile, 'w', newline="") as csvfile:
                                            lines = csv.writer(csvfile)#, fieldnames=fieldNames)
                                            
                                            #write header
                                            lines.writerow(["upc", "description", "itemMaxQty", "orderThreshold" , "replinishmentOrderQty", "itemOnHand","unitPrice","orderPlaced"])
                                        
                                            for key, value in self.itemsDictionary.items():
                                                row = [self.itemsDictionary.get(key).upc,
                                                        self.itemsDictionary.get(key).description,
                                                        self.itemsDictionary.get(key).itemMaxQty,
                                                        self.itemsDictionary.get(key).orderThreshold,
                                                        self.itemsDictionary.get(key).replinishmentOrderQty,
                                                        self.itemsDictionary.get(key).itemOnHand, 
                                                        self.itemsDictionary.get(key).unitPrice,
                                                        self.itemsDictionary.get(key).orderPlaced
                                                        ]   
                                                lines.writerow(row)
                if not receiptNumberFound:
                            print("Invalid receipt number.Try again.")                
    
           
       else: 
           print("Invalid selection. Try again.")
                    
                        
        

    #### backroom operatrions    related methods
    def replinishmentOrders(self,userid): #creates order for replinishment
        oldOrders=[] 
        newOrders=[]
        countOldOrders=0
        countNewOrders=0
        #changes retail.csv orderPlaced column
        with open(self.itemsFile, 'w', newline="") as csvfile:
            writer = csv.writer(csvfile)#, fieldnames=fieldNames)
            #write header
            writer.writerow(["upc", "description", "itemMaxQty"
                                                 , "orderThreshold" 
                                                 , "replinishmentOrderQty"
                                                 , "itemOnHand", "unitPrice"
                                                 , "orderPlaced"])
                                                 
            for key, values in self.itemsDictionary.items():
                if self.itemsDictionary.get(key).orderPlaced == 0 and self.itemsDictionary.get(key).itemOnHand<=self.itemsDictionary.get(key).orderThreshold:
                    self.itemsDictionary.get(key).orderPlaced = 1
                    
                row = [self.itemsDictionary.get(key).upc,
                       self.itemsDictionary.get(key).description,
                       self.itemsDictionary.get(key).itemMaxQty,
                       self.itemsDictionary.get(key).orderThreshold,
                       self.itemsDictionary.get(key).replinishmentOrderQty,
                       self.itemsDictionary.get(key).itemOnHand, 
                       self.itemsDictionary.get(key).unitPrice,
                       self.itemsDictionary.get(key).orderPlaced
                       ]                            
                writer.writerow(row)                  
    
        #changes replinishmentOrders.csv based on replinishmentorderqt
        with open(self.replinishmentFile, 'a', newline="") as csvfile:
            lines = csv.writer(csvfile)#, fieldnames=fieldNames)
            #headings = next(lines)
            #write header
            #lines.writerow(["upc", "description", "orderQty", "orderDate" , "orderedBy", "status"])
                               
            #write rows if order not present already
            #checking orderPlaced column in items and if order is not fulfilled in replinishedmentorders
            for key,values in self.itemsDictionary.items():
                #print("item: " +self.itemsDictionary.get(key).upc)
                if self.itemsDictionary.get(key).orderPlaced == 1 :
                    #order already present in replinishmentorders
                    if self.replinishmentOrdersDictionary.get(key) != None:
                        #print("replinishment : "+self.replinishmentOrdersDictionary.get(key).upc)
                        if  len(self.replinishmentOrdersDictionary)>1 and self.itemsDictionary.get(key).upc == self.replinishmentOrdersDictionary.get(key).upc and self.replinishmentOrdersDictionary.get(key).status!='fulfilled':
                            #print("Item is already ordered and is in progress.")
                            oldOrders.append([self.replinishmentOrdersDictionary.get(key).upc,self.replinishmentOrdersDictionary.get(key).description, self.replinishmentOrdersDictionary.get(key).orderDate, self.replinishmentOrdersDictionary.get(key).orderedBy,self.replinishmentOrdersDictionary.get(key).status])
                            countOldOrders=countOldOrders+1
                        
                    elif self.replinishmentOrdersDictionary.get(key) ==None:
                            ####self.replinishmentOrdersDictionary[key]=self.itemsDictionary.get(key).upc
                            #print("replinish key: "+self.replinishmentOrdersDictionary[key])
                            
                            upc = self.itemsDictionary.get(key).upc
                            description = self.itemsDictionary.get(key).description
                            orderQty = self.itemsDictionary.get(key).replinishmentOrderQty
                            orderDate = date.today()
                            orderedBy = userid
                            status = 'placed'
                            
                            newOrders.append([upc, description, orderQty, orderDate, orderedBy, status])
                        
                            self.replinishmentOrdersDictionary[key] = Replinishment(upc, description, orderQty, orderDate, orderedBy, status)
                                                    
                            row = [self.replinishmentOrdersDictionary.get(key).upc,self.replinishmentOrdersDictionary.get(key).description 
                                   ,self.replinishmentOrdersDictionary.get(key).orderQty, self.replinishmentOrdersDictionary.get(key).orderDate
                                   ,self.replinishmentOrdersDictionary.get(key).orderedBy,self.replinishmentOrdersDictionary.get(key).status]
                            print(row)
                            lines.writerow(row)
                            
                            countNewOrders = countNewOrders+1
                            #upc	description	orderQty	orderDate	orderedBy	status
        print("Existing orders")
        print( tabulate(oldOrders, headers =["upc",	"description","orderQty","orderDate	","orderedBy","status"]))
        print("Total existing orders are "+str(countOldOrders))
        print("New orders")
        print( tabulate(newOrders, headers =["upc",	"description","orderQty","orderDate",	"orderedBy","status"]))
        print("Total new orders are "+str(countNewOrders))
            
        
       
    def printInventoryReport(self):
        print("")
        inventory=[]
        countItems=0
        totalPrice=0
        for key, value in self.itemsDictionary.items():
            inventory.append([self.itemsDictionary.get(key).upc,
                       self.itemsDictionary.get(key).description,
                       self.itemsDictionary.get(key).itemOnHand, 
                       self.itemsDictionary.get(key).unitPrice,
                       self.itemsDictionary.get(key).unitPrice*self.itemsDictionary.get(key).itemOnHand
                       ]    )
            countItems=countItems+1
            totalPrice = totalPrice+(self.itemsDictionary.get(key).unitPrice*self.itemsDictionary.get(key).itemOnHand)
        
        inventory.append([countItems,'', '','',totalPrice])
        print( tabulate(inventory, headers =["upc",	"description","itemsOnHand",	"unitPrice","lineTotal"]))
        
        pass
    
   
            
                
               
            
            
    
    
    
    
    
