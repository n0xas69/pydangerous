import os
import sys
import json
import requests
import time
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


def get_last_fsd_jump():
    last_jump = ""

    with open(latest_file, "r") as f:
        line = f.readlines()
        for l in line:
            if "FSDJump" in l:
                last_jump = l

    if last_jump is not None:
        x = json.loads(last_jump)
        system = x["StarSystem"]
        return system


def get_trade_raw():
    cmdr_position = get_last_fsd_jump()
    station = ""
    system = ""
    url = f"https://www.edsm.net/fr/search/stations/index/cmdrPosition/{cmdr_position}/economy/3/service/71/sortBy/distanceCMDR"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    for table in soup.findAll("tr"):
        if "Pur" in table.getText():
            for td in soup.findAll("td"):
                if td.strong is not None:
                    station = td.strong.getText()
                    system = td.small.getText()
                    break

    return station, system


def get_trade_manu():
    cmdr_position = get_last_fsd_jump()
    station = ""
    system = ""
    url = f"https://www.edsm.net/fr/search/stations/index/cmdrPosition/{cmdr_position}/economy/5/service/71/sortBy/distanceCMDR"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    for table in soup.findAll("tr"):
        if "Manufacturé" in table.getText():
            for td in soup.findAll("td"):
                if td.strong is not None:
                    station = td.strong.getText()
                    system = td.small.getText()
                    break

    return station, system


def get_trade_data():
    cmdr_position = get_last_fsd_jump()
    station = ""
    system = ""
    url = f"https://www.edsm.net/fr/search/stations/index/cmdrPosition/{cmdr_position}/economy/4/service/71/sortBy/distanceCMDR"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    for table in soup.findAll("tr"):
        if "Encodé" in table.getText():
            for td in soup.findAll("td"):
                if td.strong is not None:
                    station = td.strong.getText()
                    system = td.small.getText()
                    break

    return station, system


def clear():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')


def get_information():
    trade_raw = get_trade_raw()
    trade_manu = get_trade_manu()
    trade_data = get_trade_data()
    return trade_raw, trade_manu, trade_data


while True:
    informations = get_information()
    time.sleep(2)
    clear()
    print(f"Trader Brut     ---->   Station : {informations[0][0]} | Système :  {informations[0][1]} \n"
          f"Trader Fabriqué ---->   Station : {informations[2][0]} | Système :  {informations[2][1]} \n"
          f"Trader Data     ---->   Station : {informations[1][0]} | Système :  {informations[1][1]}")
