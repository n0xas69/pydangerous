import os
import sys
import json
import time
import requests
from bs4 import BeautifulSoup

if sys.platform == "windows":
    log_path = os.environ["USERPROFILE"]+"\\Saved Games\\Frontier Developments\\Elite Dangerous"
else:
    log_path = "/var/log"

# On trouve le dernier fichier de log
list_of_files = []
for file in os.listdir(log_path):
    if file.endswith(".log"):
        list_of_files.append(os.path.join(log_path, file))
print(list_of_files)
latest_file = max(list_of_files, key=os.path.getctime)


def get_fsd_jump():
    last_jump = ""

    with open(latest_file, "r") as f:
        line = reversed(f.readline())
        for l in line:
            if "FSDJump" in l:
                last_jump = line

    if not last_jump == "":
        get_system(last_jump)


def get_system(jump):
    x = json.load(jump)
    system = x["StarSystem"]
    get_trade_raw("maia")


def get_trade_raw(position):
    station = ""
    system = ""
    url = f"https://www.edsm.net/fr/search/stations/index/cmdrPosition/{position}/economy/3/service/71/sortBy/distanceCMDR"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    for table in soup.findAll("tr"):
        print(table.td[2].a.text)


def get_trade_manu():
    station = ""
    system = ""


def get_trade_data():
    station = ""
    system = ""


while True:
    time.sleep(2)
    get_fsd_jump()

