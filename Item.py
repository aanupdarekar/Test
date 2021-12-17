# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 15:41:37 2021

@author: prer
"""

# Create an Item class
class Item:
    def __init__(self, UPC, Description, Item_Max_Qty, Order_Threshold
                 , replenishment_order_qty, Item_on_hand, Unit_price, Order_placed):
        self.UPC = UPC
        self.Description = Description
        self.Item_Max_Qty = Item_Max_Qty
        self.Order_Threshold = Order_Threshold
        self.replenishment_order_qty = replenishment_order_qty
        self.Item_on_hand = Item_on_hand
        self.Unit_price = Unit_price
        self.Order_placed = Order_placed
        


