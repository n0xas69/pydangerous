import os
import glob
import json
import time


log_path = os.environ["USERPROFILE"]+"\\Saved Games\\Frontier Developments\\Elite Dangerous"


# On trouve le dernier fichier de log
list_of_files = glob.glob(log_path+"/*.log")
latest_file = max(list_of_files, key=os.path.getctime)
print(latest_file)


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


def get_trade_raw():
    station = ""
    system = ""


def get_trade_manu():
    station = ""
    system = ""


def get_trade_data():
    station = ""
    system = ""


while True:
    time.sleep(2)
    get_fsd_jump()