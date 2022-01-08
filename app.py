import os
import glob


log_path = os.environ["USERPROFILE"]+"\\Saved Games\\Frontier Developments\\Elite Dangerous"


# On trouve le dernier fichier de log
list_of_files = glob.glob(log_path+"/*.log")
latest_file = max(list_of_files, key=os.path.getctime)
print(latest_file)


# On cherche le dernier saut FSD, si il est égal au précédent, alors le joueur n'a pas changé de système
def get_fsd_jump():
    last_jump = ""
    previous_jump = ""

    with open(latest_file, "r") as f:
        line = f.readline()
        for l in line:
            if "FSDJump" in l:
                last_jump = line

    if not last_jump == previous_jump:
        if not last_jump == "":
            # Saut FSD détecté
            pass

    previous_jump = last_jump