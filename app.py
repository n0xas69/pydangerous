import os
import sys
import json
import requests
import time
from tabulate import tabulate
from bs4 import BeautifulSoup

# Le chemin par défaut du journal est déjà dans le code, vous pouvez le changer en renseignant cette variable
LOG_PATH = ""

if LOG_PATH:
    log_path = LOG_PATH

if sys.platform == "win32":
    log_path = os.environ["USERPROFILE"]+"\\Saved Games\\Frontier Developments\\Elite Dangerous"
else:
    log_path = "/var/log"

# On trouve le dernier fichier de log
try:
    list_of_files = []
    for file in os.listdir(log_path):
        if file.endswith(".log"):
            list_of_files.append(os.path.join(log_path, file))
    latest_file = max(list_of_files, key=os.path.getctime)
except Exception as e:
    print("ERREUR : Impossible de trouver les fichiers journaux.")


def get_last_fsd_jump():
    last_jump = ""

    try:
        with open(latest_file, "r") as f:
            line = f.readlines()
            for l in line:
                if "FSDJump" in l:
                    last_jump = l

        if last_jump is not None:
            x = json.loads(last_jump)
            system = x["StarSystem"]
            return system

    except Exception as e:
        print("ERREUR : Impossible d'ouvrir le fichier journal du jeu.")


def get_trade_raw(cmdr_position):
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


def get_trade_manu(cmdr_position):
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


def get_trade_data(cmdr_position):
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



def get_interest_body(cmdr_position):
    earth_like = []
    teraform_rocky_body = []
    teraform_hmetal_world = []
    teraform_water_world = []
    water_world = []
    ammonia_world = []
    params = {"systemName" : cmdr_position}

    r = requests.get("https://www.edsm.net/api-system-v1/bodies", params=params)
    data = r.json()
    for p in data["bodies"]:
        if p["subType"] == "High metal content world" and p["terraformingState"] == "Candidate for terraforming":
            teraform_hmetal_world.append(p["name"])
        elif p["subType"] == "Water world" and p["terraformingState"] == "Candidate for terraforming":
            teraform_water_world.append(p["name"])
        elif p["subType"] == "Rocky body" and p["terraformingState"] == "Candidate for terraforming":
            teraform_rocky_body.append(p["name"])
        elif p["subType"] == "Earth-like world" and p["terraformingState"] == "Candidate for terraforming":
            earth_like.append(p["name"])
        elif p["subType"] == "Water world":
            water_world.append(p["name"])
        elif p["subType"] == "Ammonia world":
            ammonia_world.append(p["name"])
            
    
    return earth_like, teraform_hmetal_world, teraform_rocky_body, teraform_water_world, water_world, ammonia_world
   


def clear():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')


def get_information():
    cmdr_position = get_last_fsd_jump()
    if cmdr_position is None:
        print("ERREUR : Impossible de localiser le joueur")
        return False
    else:
        interest_body = get_interest_body(cmdr_position)
        trade_raw = get_trade_raw(cmdr_position)
        trade_manu = get_trade_manu(cmdr_position)
        trade_data = get_trade_data(cmdr_position)
        return trade_raw, trade_manu, trade_data, interest_body


clear()
while True:
    informations = get_information()
    if informations:
        time.sleep(2)
        clear()
        table = [["Brut", informations[0][1], informations[0][0]], ["Fabriqué", informations[1][1],informations[1][0]], ["Encodé", informations[2][1], informations[2][0]]]
        headers = ["Type de matériaux", "Système", "Station"]
        table_body = [
            ["Abondant en métaux terraformable", informations[3][1]],
            ["Earth-like", informations[3][0]],
            ["Planète rocheuse terraformable", informations[3][2]],
            ["Monde aquatique terraformable", informations[3][3]],
            ["Monde ammoniac", informations[3][5]],
            ["Monde aquatique", informations[3][4]],
            ]
        headers_body = ["Type planète", "Nom"]
        print("Trader les plus proches : ")
        print(tabulate(table, headers, tablefmt="grid")+"\n")
        print("Point d'intérêt d'exploration : ")
        print(tabulate(table_body, headers_body, tablefmt="grid")+"\n")
    else:
        break
    
