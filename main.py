import time, os
import sys
import concurrent.futures

from check import Checker
from analysis import analyze
from dump_cookies import dump_cookies

# check () returns bool (success), str or None (link)

targets = [
    # Name, Breakout, Recommendation
    ["reed.eric2022@istemghs.org", "Eric Reed", "4", ["Petrecca", "Falin", "Beattie"], "I'd really like a photography breakout. Also this definitely wasn't botted ;)"],
    ["orlando.william2022@istemghs.org", "William Orlando", "4", ["Petrecca", "Smith", "Wright"], "Woodworking"],
    ["kilmer.aiden2023@istemghs.org", "Aiden Kilmer", "5", ["Zobel", "Petrecca", "Wright"], "Add more game-type stuff"],
    ["jenkins.grayson2023@istemghs.org", "Grayson Jenkins", "5", ["Petrecca", "Falin", "Sandham"], "You should mail us all free food"],
    ["reminder.aaron2023@istemghs.org", "Aaron Reminder", "5", ["Petrecca", "Falin", "Young"], "Photography breakout"],
    ["pastor.owen2022@istemghs.org", "Owen Pastor", "4", ["Petrecca", "Sandham", "Wright"], "Gaming would be fun"],
    ["morris.maddox2022@istemghs.org", "Maddox Morris", "4", ["Petrecca", "Smith", "Sandham"], "Photography breakout would be cool"],
    ["pike.brandon2022@istemghs.org", "Brandon Pike", "4", ["Petrecca", "Falin", "Zobel"], "Programming breakout"],
    ["stehlik.blake2022@istemghs.org", "Blake Stehlik", "4", ["Petrecca", "Zobel", "Falin"], "Coding breakout"]
]

def main ():
    for info in targets:
        cookie_file_path = f"cookies/{info [0]}.p"
        if not os.path.isfile (cookie_file_path): dump_cookies (info [0])
    if len (sys.argv) == 2 and sys.argv [1] == "pre_login":
        print ("Done with logins")
        return

    checker = Checker ()
    while True:
        success, token = checker.check ()
        if success: break
        time.sleep (0.25)

    start = time.time ()
    with concurrent.futures.ThreadPoolExecutor () as executor:
        for info in targets:
            executor.submit (analyze, token, info)
    end = time.time ()
    print (f"submitted {len (targets)} responses in {end - start} seconds")


if __name__ == "__main__":
    main ()
