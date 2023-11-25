import imaplib
import email
import getpass
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt


username =  'OUTLOOK_EMAIL_ID'
password = 'PASSWORD'
mail = imaplib.IMAP4_SSL('imap.outlook.com')
mail.login(username, password)

#Printing Mail List
print(mail.list())
#Selecting Inbox
mail.select("Inbox")


#list uids
result, numbers = mail.uid('search', None, "ALL")
uids = numbers[0].split()
uids = [id.decode("cp1252") for id in uids ]


#printing the messages 
try:
    result, messages = mail.uid('fetch', ','.join(uids), '(BODY[HEADER.FIELDS (SUBJECT FROM DATE)])')
    
except Exception:
    pass



#creating dataset  date, subject, sender
date_list = []
from_list = [] 
subject_text = []
from_list1 = []
for i, message in messages[::2]:
    msg = email.message_from_bytes(message)
    decode = email.header.decode_header(msg['Subject'])[0]
    if isinstance(decode[0],bytes):
        decoded = decode[0].decode('ISO-8859-1')
        subject_text.append(decoded)
    else:
        subject_text.append(decode[0])
    date_list.append(msg.get('date'))
    from_list = msg.get('From')
    #from_list = from_list.split("<")[0].replace('"', '')
    from_list1.append(from_list)
date_list = pd.to_datetime(date_list)
date_list1 = []
for item in date_list:
    date_list1.append(item.isoformat(' ')[:-6])
print(len(subject_text))
print(len(from_list))
print(len(date_list1))
df = pd.DataFrame(data={'Date':date_list1, 'Sender':from_list1, 'Subject':subject_text})

print (df["email_id"] = df["Sender"].str.extract(r'([^@\s]+)'))
print (df["domain"] = df["Sender"].str.extract(r'@([^.>]+(?:\.[^<>\s]+)+)'))




#printing world cloud from email subjects



# Create a list of words
text = ""
for item in emails["Subject"]:
    if isinstance(item,str):
        text += " " + item
    text.replace("'", "")
    text.replace(",","")
    text.replace('"','')


# Create the wordcloud object
wordcloud = WordCloud(width=800, height=800, background_color="white")

# Display the generated image:
wordcloud.generate(text)
plt.figure(figsize=(8,8))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.margins(x=0, y=0)
plt.title("Most Used Subject Words", fontsize=20,ha="center", pad=20)
plt.show()