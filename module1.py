from tqdm import tqdm
import time
import urllib
import urllib3
from bs4 import BeautifulSoup
import requests
import re
import os

def ask():
    songnum = " songs, download? [Y/n]"
    print("|",songnum)
    resstart = ""
    resstart = input("| Type here:")
    if resstart == 'Y' or resstart == 'y':
        isStart = True
        print("|","Starting...")
        return isStart
    elif resstart == 'n':
        isStart = False
        print("|","Stopping...")
        return isStart
    else:
        return ask()

test = {'JZM':'Gay', 'LL':"very Gay", '111':"not found", "222":"pop", "3333":"jiujiu"}
new = {'LL':"very Gay", 'JZM':'Gay', "Newsong":"shhhh"}
list1 = ["1","2","3"]
text = "What is love?:\""

testvalues = list(test.values())
print(testvalues)
newvalues = list(new.values())
for i in testvalues[:]:
    if i in newvalues[:]:
        print(i)
        testvalues.remove(i)
        newvalues.remove(i)
print(testvalues)
print(newvalues)
eval("{}")

print("|","Ursula".center(60),"|") 
print(text)

for banned in r'/\*:?"<>|':
    text = text.replace(banned,"#")

print(text)
Dstart = ask()
print(Dstart)


