import time, os
import sys

from check import setup_check, check
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

def process_link (link):
    for target in targets:
        execute_form (link, target)

def execute_form (link, target):
    # Automate calling the form based on the link and the target details
    pass

def main ():
    for info in targets:
        cookie_file_path = f"cookies/{info [0]}.p"
        if not os.path.isfile (cookie_file_path): dump_cookies (info [0])
    if len (sys.argv) == 2 and sys.argv [1] == "pre_login":
        print ("Done with logins")
        return

    # setup_check ()
    # while True:
    #     success, token = check ()
    #     if success: break
    #     time.sleep (0.25)
    token = "1FAIpQLSdmuiZiYFtEoAz2nF8D8mXz2uuvbtmxNs18ETCfmRWUhK76cQ"

    # we have the email ladies and gentlemen!
    # I'm hardcoding the token for right now (testing).
    # token = "1FAIpQLScyEdVTNejePdBXCtqAww7s-RMkhwRx5WmJRmOfy42Mhhf4lw"
    # token = "1FAIpQLSc5Cz0RYzqk_jHeF03V0l0CNnATZZ4JVFNBp5xxoEg7F-GR7g"
    # token = "1FAIpQLSeFEruSgyAyJiXwWMUENGO0YbOKH0PkI92vBzBAxGGy1h5b7g"
    for info in targets:
        analysis = analyze (token, info)


if __name__ == "__main__":
    main ()
