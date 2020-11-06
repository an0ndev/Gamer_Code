from selenium import webdriver
import time
import pickle
import requests

def main (email):
    print (f"Please log in as {email}")
    driver = webdriver.Chrome ()
    driver.get ("https://docs.google.com/forms/d/e/1FAIpQLSeFEruSgyAyJiXwWMUENGO0YbOKH0PkI92vBzBAxGGy1h5b7g/viewform")
    while True:
        if driver.current_url.startswith ("https://docs.google.com/forms/d/e/1FAIpQLSeFEruSgyAyJiXwWMUENGO0YbOKH0PkI92vBzBAxGGy1h5b7g"): break
        time.sleep (0.5)
    jar = requests.cookies.RequestsCookieJar ()
    for cookie in driver.get_cookies ():
        jar.set (cookie ["name"], cookie ["value"], domain = cookie ["domain"], path = cookie ["path"])
    driver.close ()

    with open (f"cookies/{email}.p", "wb+") as cookie_file:
        pickle.dump (jar, cookie_file)

def dump_cookies (email = None):
    if email is None: email = input ("Enter your email associated with your account: ")
    main (email)
