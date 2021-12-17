# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 17:13:13 2021

@author: prer
"""

import csv
import Item

#Create a Store class
class Store:

    itemsList = []
    
    def __init__(self,filename):
        with open(filename, newline='') as csvfile:
            lines = csv.reader(csvfile, delimiter=',')#, quotechar='|')
            #print(spamreader)
            count=0
            for row in lines:
                if count<=10:
                    count = count+1
                    print(row)
                    print(row[0], row[1])
                    #print(', '.join(row))

                    item = Item(row[0],row[1],row[2],row[3],row[4],row[5],row[6], row[7])           
                    print(item)
                    self.itemsList.append(item)

