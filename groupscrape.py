from telethon.sync import TelegramClient
import csv
import time

# get time from os
timestamp = time.strftime("%Y%m%d-%H%M%S")

# log in to telegram api
api_id = YOUR_API_ID
api_hash = 'YOUR_API_HASH'
phone = '+15555551234'
client = TelegramClient(phone, api_id, api_hash)

# telegram session login and otp
client.connect()
if not client.is_user_authorized():
	client.send_code_request(phone)
	client.sign_in(phone, input('Enter OTP code: '))


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
print('Choose a group to scrape members from:')
i=0
for g in groups:
    print(str(i) + '- ' + g.title)
    i+=1

g_index = input("Enter a Number: ")
target_group=groups[int(g_index)]

print(target_group)
# choose output name for csv - includes timestamp
csv_name = input("Enter output file name: ") + "_" + timestamp + ".csv"

# get group members and details
print('Fetching Members...')
all_participants = []
all_participants = client.get_participants(target_group, aggressive=True)

# save group member details
print('Saving In file...')
with open(csv_name,"w",encoding='UTF-8') as f:
    writer = csv.writer(f,delimiter=",",lineterminator="\n")
    writer.writerow(['username','user id', 'access hash','name','group', 'group id'])
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
        writer.writerow([username,user.id,user.access_hash,name,target_group.title, target_group.id])      
print('Members scraped successfully.')

# print output csv name
print('Created CSV ' + str(csv_name) +'.')
