# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 14:37:52 2023

@author: Dr.Salama Ikki
"""

import imaplib
import email
import time
import RPi.GPIO as GPIO

import rpi_lcd
from rpi_lcd import LCD

import pygame

def PiAction(numberOfEmails):
  print("New Email")
  led = 25
  hold_blink = 10
  GPIO.setup(led, GPIO.OUT)
  GPIO.output(led, GPIO.HIGH) # Turn LED on
  pygame.mixer.music.play() # play notification sound
  lcd.clear()
  lcd.text("===New  Email===", 1)
  lcd.text("New : {}".format( numberOfEmails ), 2)
  time.sleep(hold_blink)                   # Delay for 10 second
  GPIO.output(led, GPIO.LOW)  # Turn LED off
  

pygame.mixer.init() # set up sound system
pygame.mixer.music.load("ping.mp3")
  
  
# Pi and LCD Config
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
lcd = LCD()
# email info stuff
imap_server = "imap.outlook.com"
email_addr = "testthissystem@outlook.com"
password = "#UwU-1234"
select_star = "inbox"
# 'sent' shows the correct amount
# 'inbox' was off and not updating
# deleted entire mailbox, works
# throws exception if inbox empty
# kinda cant send email from that email lol

# due to suspicious activity, account locked
# likely needs a special email just cuz policies

# fixed cuz stuff
# now updates on a 10 second delay, can be changed with DELAY
# searches for unread emails
# number updates when :
#         1.  new ones come
#         2.  emails are read
# if the last check has less unread emails than the current check, new email
# however, if you read and email at the same time as when u get a new email, the function may not call
# since this is unlikely and you will be on the app when this occurs, it is not an important flaw, but one nonetheless
led = 25
hold_blink = 1
print("hello")
GPIO.setup(led, GPIO.OUT)
GPIO.output(led, GPIO.HIGH) # Turn LED on
time.sleep(hold_blink)                   # Delay for 1 second
GPIO.output(led, GPIO.LOW)  # Turn LED off
# choosing server and logging in
mail = imaplib.IMAP4_SSL(imap_server)
print("hello")
lcd.text("*Hello*", 1)
mail.login(email_addr, password)

NumberOfEmailsInBox = 0
loopedOnce = False
DELAY = 10


# loops forever
while(1 == 1 or 0 == 0):
  lcd.clear()
  # chooses inbox
  mail.select(select_star)
  data = mail.search(None, 'UnSeen') # chooses unread emails in inbox
  mail_ids = data[1]
  try:
      id_list = mail_ids[0].split()  # holds all ids of unread emails
      first_email_id = int(id_list[0]) # email ids stuff
      latest_email_id = int(id_list[-1])
  
      print( len(id_list) ) # length of unread email id array = # of unread emails
      lcd.text("Unread : {}".format( len(id_list) ) ,1)
  
  # if a baseline is established and the last loop has less unread emails
      if loopedOnce == True and NumberOfEmailsInBox < len(id_list):
        PiAction( len(id_list)-NumberOfEmailsInBox ) # do stuff with the raspberry pi
  except:
      print("0")
      lcd.text("No Unread Emails", 1)
  #mail.logout() # the old idea was to login and logout each time
    # not neccesary, just update it while youre still on it
  time.sleep(DELAY) # wait a little to not overburden the server
  NumberOfEmailsInBox = len(id_list)
  loopedOnce = True # makes sure that the baseline has been established
