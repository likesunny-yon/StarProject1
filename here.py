import json
import sys
import os
import sqlite3
from datetime import datetime

from utils.upwork.signup import signup
from utils.docx.createdocx import createdocx
from utils.mail.generator.tempemail import TempGmail, TempMinuteBoxMail, TempAnonaddyEmail
import config

def importProfile(filename = '1'):
    with open(os.path.join(config.Profile_Path, filename + '.json'), 'r', encoding='utf-8') as f:
        profile = json.load(f)
    return profile

def save2DB(tempemail):
    db_fullpath = os.path.join(config.DBPath, config.DBName)

    # Connect to the database (create a new one if it doesn't exist)
    conn = sqlite3.connect(db_fullpath)

    # Create a cursor object to execute SQL commands
    cur = conn.cursor()
    cur.execute("INSERT INTO accounts (email, name, status, timestamp) VALUES (?, ?, ?, ?)", (tempemail, name, 'active', str(datetime.now())))
    conn.commit()
    conn.close()

def createTempEmailObject(emailtype="gmail"):
    if (emailtype == "gmail"):
        tempEmailObject = TempGmail()
        tempEmailObject.set_origin_email(config.Original_Email)
    elif (emailtype == "minutebox"):
        tempEmailObject = TempMinuteBoxMail()
    elif (emailtype == "anonaddy"):
        tempEmailObject = TempAnonaddyEmail()
    else:
        print("ERROR: Input correct email type!")
        return False
    tempEmailObject.create_temp_email()
    print("INFO: Try signup with ", tempEmailObject.get_temp_email())
    return tempEmailObject

if __name__ == '__main__':
    # import profile data
    name = sys.argv[1]
    profile = importProfile(name)

    # create temporary docx for sign up
    docxpath = createdocx(name, profile, path=os.path.join(os.getcwd(), config.Profile_Path))

    # create tempemail object and get mail address.
    tempEmailObject = createTempEmailObject(config.TempEmailType)
    print(tempEmailObject.get_temp_email())
    if (tempEmailObject):
        signup(profile, tempEmailObject, profile_doc=docxpath)
        print("====================================================")
        print("INFO: Create account successfully with ", tempEmailObject.get_temp_email())
        print("====================================================")
        
        save2DB(tempEmailObject.get_temp_email())
    else:
        print("ERROR: Error ocuured.")