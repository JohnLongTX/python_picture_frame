import os
import sys
import imaplib
import array
import email
import email.header
from datetime import datetime

host = '*********'  #email host name
user = '*********'  #email user name
password = '***********'    #mailbox password

def getMail():
    # Connect to the server
    print('Connecting to ' + host)
    mailBox = imaplib.IMAP4_SSL(host)
    # Login to account
    mailBox.login(user, password)
    print("Connecting as: " + user)
    boxList = mailBox.list()
    print(boxList)
    mailBox.select()
    searchQuery = '(UNSEEN)'
    result, data = mailBox.uid('search', None, searchQuery)
    ids = data[0]
    local_date = ''
    id_list = ids.split()
    i = len(id_list)
    #iterate through useen emails
    for x in range(i):
        latest_email_uid = id_list[x]
        result, email_data = mailBox.uid('fetch', latest_email_uid, '(RFC822)')
        raw_email = email_data[0][1]
        raw_email_string = raw_email.decode('utf-8')
        email_message = email.message_from_string(raw_email_string)

        for part in email_message.walk():
            filename = part.get_filename()
            date_tuple = email.utils.parsedate_tz(email_message['Date'])
            if date_tuple:
                local_date = datetime.fromtimestamp(
                    email.utils.mktime_tz(date_tuple))
                print(local_date)
            if filename:
                filepath = os.path.join(os.getcwd(), filename)
                if not os.path.isfile(filepath):
                    with open(filepath, 'wb') as f:
                        f.write(part.get_payload(decode=True))
                    print("{0:.<20} downloaded successfully".format(filename))
    mailBox.close()
    mailBox.logout()
    print("Mail retrieved")
getMail()
