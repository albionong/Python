# -*- coding: utf-8 -*-
"""
Project: Secret Santa E-mailer

Date Created: November 25, 2020
Last Update: November 25, 2020

Purpose: To peform a digital Secret Santa via e-mail.
Method:
    1. Take an input list (Name, Email, Wishlist)
    2. Match participants randomly (Cannot match with self, No duplicate 
                                    matches)
    3. Send email to participants (Santa and Receiver)
"""

import copy
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

names = ['name 1', 'name 2', 'name 3']
emails = ['email 1', 'email 2', 'email 3']
address = ['address 1', 'address 2', 'address 3']                                                 
wishlist = 'list 1', 'list 2', 'list 3']

def secret_santa(names):
    my_list = names
    choose = copy.copy(my_list)
    result = []
    for i in my_list:
        names = copy.copy(my_list)
        names.pop(names.index(i))
        chosen = random.choice(list(set(choose)&set(names)))
        result.append((i,chosen))
        choose.pop(choose.index(chosen))
    return result

ss_result = secret_santa(names)
final = zip(ss_result,emails,address,wishlist)

for x in final:
    findindex = names.index(str(x[0][1]))
    addressfind =  address[findindex]
    wishlistfind = wishlist[findindex]
    
    fromaddr = "YOUR EMAIL GOES HERE"
    toaddr = x[1]
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "SECRET EMAIL FOR SECRET SANTA!"
 
    body1 = "Hello, "+str(x[0][0])+"!"
    body2 = '''\n\nWelcome to Secret Santa!'''
    body3 = '''\n\nSince we are all stuck indoors and should practice social distancing, we will be doing this year's Secret Santa virtually!'''
    body4 = '''\n\nLet's get some rules out of the way:
    1. The budget is around $50.
    2. If you can, have the gift delivered to your recipient before December 18.
    3. Make it anonymous if possible.
    \nSo on to the fun part!'''
    body5 = "\n\nThis year your recipient will be "+str(x[0][1])+"!"
    body6 = "\n\nTheir mailing address is:\n"+addressfind
    body7 = "\n\nThis is their wishlist:\n"+wishlistfind
    body8 = "\n\nHave fun!"
    body = (body1+
            body2+
            body3+
            body4+
            body5+
            body6+
            body7+
            body8)
    msg.attach(MIMEText(body, 'plain'))
 
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("YOUR EMAIL ADDRESS", "YOUR PASSWORD")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
    print ("mail sent to "+x[1])