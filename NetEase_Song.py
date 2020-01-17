from bs4 import BeautifulSoup
import requests
import re
import urllib
import urllib3
from tqdm import tqdm
import time
import os

songlist_url_default = "https://music.163.com/playlist?id=3141073931"
download_path_default = r"C:\Users\WBR1\Downloads\Music\NetEase" + "\\"
download_url_raw = "http://music.163.com/song/media/outer/url?id="
songlist = {}
templist = {}
downloadlist = {}
basicinfo = {"songlist":songlist_url_default, "downloadpath":download_path_default, "downloadraw":download_url_raw}

headers = {
    'Accept': 'text/html, application/xhtml+xml, application/xml; q=0.9, */*; q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-Hans-CN, zh-Hans; q=0.8, en-US; q=0.5, en; q=0.3',
    'Connection': 'Keep-Alive',
    'Host': 'music.163.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'User-Agent:Mozilla/5.0(Macintosh;IntelMacOSX10_7_0)AppleWebKit/535.11(KHTML,likeGecko)Chrome/17.0.963.56Safari/535.11'
}


def ask():
    global songlist
    songnum = str(len(songlist)) + " songs, download? [Y/n]"
    print("|",songnum)
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
    


#info = BeautifulSoup(requests.get(url).content,"html.parser")
#print(info)
print("|","Welcome to NetEase downloader!")
print("|","Copy your songlist url below, or type 'default' if you want to use")
print("|"," 'https://music.163.com/playlist?id=3141073931'")
songlist_url = input("| Copy or type here:")
if not songlist_url == "default":
    basicinfo["songlist"] = songlist_url

print("|","Now insert your preferred download path, or type 'default' if you want to use")
print("|"," 'C:\\Users\\WBR1\\Downloads\\Music\\Netease'")
download_path = input("| Copy or type here:")
if not download_path == "default":
    basicinfo["downloadpath"] = download_path + "\\"

if not os.path.exists(basicinfo["downloadpath"] + "\\0"):
    os.mkdir(basicinfo["downloadpath"] + "\\0")

s = requests.session()
#print(basicinfo["songlist"])
log = open(basicinfo["downloadpath"] + "\\0\\log.txt", "a", encoding="utf-8")

if not os.path.exists(basicinfo["downloadpath"] + "\\0\\songnamelist.txt"):
    songnamelist_file = open(basicinfo["downloadpath"] + "\\0\\songnamelist.txt","w", encoding="utf-8")
    songnamelist_file.write("{}")
    songnamelist_file.close()

songnamelist_file = open(basicinfo["downloadpath"] + "\\0\\songnamelist.txt", "r+", encoding="utf-8")

if os.path.getsize(basicinfo["downloadpath"] + "\\0\\songnamelist.txt") == 0:
    songnamelist_file.write("{}")

soup = BeautifulSoup(s.get(str(basicinfo["songlist"]), headers=headers).content, 'html.parser')
soup = soup.ul
songlist_raw = soup.find_all("a")
#print(songlist_raw)

for child in soup.children:
    songname = child.string
    songid = child.a['href'][9:]
    print("|","√\t",songname)
    songlist[songname] = songid

#songnamelist_file.write(str(songlist)
songread = songnamelist_file.read()
#print(songread)
if songread == "":
    songread = "{}"

songnamelist_content = eval(songread)#origin 字典转换要用eval不用dict!!!

#print(songnamelist_content)
songnamelist_content = eval(str(songnamelist_content))
songnamelist_content = list(songnamelist_content.keys())
#print("Songname: " + str(songnamelist_content))
songnamelist_file.close()
songnamelist_file = open(basicinfo["downloadpath"] + "\\0\\songnamelist.txt", "w+", encoding="utf-8")

#print("Song: " + str(songlist))
templist = songlist#new backup
#print("Temp: " + str(templist))
songlist = eval(str(songlist))
downloaddict = songlist.copy()
songlist = list(songlist.keys())

for i in songnamelist_content[:]:  
    if i in songlist[:]:
        songlist.remove(i)
        #print("remove: " + i)
        downloaddict.pop(i)

#print("New list: " + str(templist))
#print("New id list: " + str(songlist))
#print("Download dict: " + str(downloaddict))
Dstart = ask()

if Dstart:
    songnamelist_file.write(str(templist))
    for i in tqdm(range(len(downloaddict))):
        songinfo = downloaddict.popitem()
        songid_out = songinfo[1]
        songname_out = str(songinfo[0])

        for banned in r'/\*:?"<>|':
            songname_out = songname_out.replace(banned,"#")

        download_url = basicinfo["downloadraw"] + songid_out + ".mp3"
        download_path = basicinfo["downloadpath"] + songname_out + ".mp3"
        #print(download_url+ "\t" + download_path)
        urllib.request.urlretrieve(download_url, download_path)
        log.write("√\t" + songname_out + "\t" + time.asctime(time.localtime(time.time())) + "\n")
    
    print("|","Done!")
    print("|","Check the log file 'log.txt' for more info.")

else:
    print("|","Stopped")

print("|","Written with love by WBR")
log.close()
songnamelist_file.close()

input("| Press Enter to exit")
