from telethon.sync import TelegramClient
import csv
import time
import os.path
import credentials
from slugify import slugify


# get time from os
timestamp = time.strftime("%Y%m%d-%H%M%S")

# log in to telegram api

client = TelegramClient(credentials.phone, credentials.api_id, credentials.api_hash)

# telegram session login and otp
client.connect()
if not client.is_user_authorized():
	client.send_code_request(credentials.phone)
	client.sign_in(credentials.phone, input('Enter OTP code: '))


# get current groups
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
chats = []
last_date = None
chunk_size = 200
groups=[]

result = client(GetDialogsRequest(
             offset_date=last_date,
             offset_id=0,
             offset_peer=InputPeerEmpty(),
             limit=chunk_size,
             hash = 0
         ))
chats.extend(result.chats)

for chat in chats:
    try:
        if chat.megagroup== True:
            groups.append(chat)
    except:
        continue

# id and select group
print('Choose a group to scrape members from: \n')
i=0
for g in groups:
    print(str(i) + '- ' + g.title)
    i+=1

g_index = input("\n Enter a Number: ")
target_group=groups[int(g_index)]

print("Configuring Scrape for " + str(target_group.title) + ": ")

# clean group name for file save
cleantitle = slugify(target_group.title)

print("Scraping from group " + str(cleantitle) + "... \n")

'''
uncommenting below will allow you to specify a file prefix for the csv export.
'''

# csv_name = input("Enter output file name: ") + "_" + timestamp + ".csv"
csv_name = "csv/" + str(cleantitle) + "_" + timestamp + ".csv"

# get group members and details
print('Fetching Members from group... \n')
all_participants = []
all_participants = client.get_participants(target_group, aggressive=True)


# check for csv directory and create if needed
directory = './csv/'
currdir = os.getcwd()
filepath = os.path.join(currdir, csv_name)
if not os.path.isdir(directory):
    os.mkdir(directory)


# save group member details
print('Saving Group Details to CSV... \n')
with open(filepath,"w",encoding='UTF-8') as f:
    writer = csv.writer(f,delimiter=",",lineterminator="\n")
    writer.writerow(['username','user id', 'access hash','name','group', 'group id','onlinestatus'])
    for user in all_participants:
        if user.username:
            username= user.username
        else:
            username= ""
        if user.first_name:
            first_name= user.first_name
        else:
            first_name= ""
        if user.last_name:
            last_name= user.last_name
        else:
            last_name= ""
        name= (first_name + ' ' + last_name).strip()
        writer.writerow([username,user.id,user.access_hash,name,target_group.title, target_group.id,user.status])      
print(str(target_group.title) + ' Members scraped successfully. \n')

# print output csv name
print('Created User CSV: ' + str(filepath) +'.')
