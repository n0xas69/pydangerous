import os
import sys
import json
import time
import requests
from bs4 import BeautifulSoup


if sys.platform == "win32":
    log_path = os.environ["USERPROFILE"]+"\\Saved Games\\Frontier Developments\\Elite Dangerous"
else:
    log_path = "/var/log"

# On trouve le dernier fichier de log
list_of_files = []
for file in os.listdir(log_path):
    if file.endswith(".log"):
        list_of_files.append(os.path.join(log_path, file))
latest_file = max(list_of_files, key=os.path.getctime)


def get_fsd_jump():
    last_jump = ""

    with open(latest_file, "r") as f:
        line = f.readlines()
        for l in line:
            if "FSDJump" in l:
                last_jump = l

    if not last_jump == "":
        return last_jump


def get_system():
    jump = get_fsd_jump()
    x = json.loads(jump)
    system = x["StarSystem"]
    return system


def get_trade_raw():
    cmdr_position = get_system()
    station = ""
    system = ""
    url = f"https://www.edsm.net/fr/search/stations/index/cmdrPosition/{cmdr_position}/economy/3/service/71/sortBy/distanceCMDR"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    for table in soup.findAll("tr"):
        if "pur" in table.getText():
            for td in soup.findAll("td"):
                if not td.strong == None:
                    station = td.strong.getText()
                    system = td.small.getText()
                    break

    print(f"Système : {system} | Station : {station}")
    return station, system


def get_trade_manu():
    cmdr_position = get_system()
    station = ""
    system = ""
    url = f"https://www.edsm.net/fr/search/stations/index/cmdrPosition/{cmdr_position}/economy/5/service/71/sortBy/distanceCMDR"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    for table in soup.findAll("tr"):
        if "Manufacturé" in table.getText():
            for td in soup.findAll("td"):
                if not td.strong == None:
                    station = td.strong.getText()
                    system = td.small.getText()
                    break

    print(f"Système : {system} | Station : {station}")
    return station, system


def get_trade_data():
    cmdr_position = get_system()
    station = ""
    system = ""
    url = f"https://www.edsm.net/fr/search/stations/index/cmdrPosition/{cmdr_position}/economy/4/service/71/sortBy/distanceCMDR"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    for table in soup.findAll("tr"):
        if "Encodé" in table.getText():
            for td in soup.findAll("td"):
                if not td.strong == None:
                    station = td.strong.getText()
                    system = td.small.getText()
                    break

    print(f"Système : {system} | Station : {station}")
    return station, system


while True:
    time.sleep(3)
    get_trade_data()
    get_trade_manu()
    get_trade_raw()

