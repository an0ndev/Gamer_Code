from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import requests
import random
import json
import base64
import quopri
import re
import time

service = None

def setup_check ():
    global service
    creds = InstalledAppFlow.from_client_secrets_file (
        "client_secret.json",
        scopes= [
            "https://www.googleapis.com/auth/gmail.readonly"
        ]
    ).run_local_server(host='localhost',
    port=random.randrange (8080, 65535),
    authorization_prompt_message='Please visit this URL: {url}',
    success_message='The auth flow is complete; you may close this window.',
    open_browser=True)
    service = build ("gmail", "v1", credentials = creds)
    print (service)

def check ():
    global service
    # call users.messages.list
    # userId = me, includeSpamTrash = false, maxResults = 1, alt = json

    list_response = service.users ().messages ().list (userId = "me", includeSpamTrash = "false", maxResults = "1", alt = "json").execute ()
    message_id = list_response ["messages"] [0] ["id"]
    get_response = service.users ().messages ().get (userId = "me", id = message_id, format = "raw").execute ()
    # print (json.dumps (get_response, indent = 4))
    message_body_b64 = get_response ["raw"]
    message_body_bytes = base64.urlsafe_b64decode (message_body_b64)
    shitty_message_body = message_body_bytes.decode ("utf-8", errors = "ignore")
    message_headers, message_body = parse_shitty (shitty_message_body)
    subject_with_rest = message_headers.split ("Subject: ") [1]
    subject = subject_with_rest.split ("\n") [0]
    breakout_in_subject = "breakout" in subject.lower () or "here" in subject.lower ()
    print (f"{time.time ()}: breakout or here in subject: {breakout_in_subject}")
    if not breakout_in_subject: return False, None
    return True, get_token_from_target (message_body)

def get_token_from_target (target_):
    target = target_
    redirect_token_from_url = re.findall (r"(?<=https:\/\/forms.gle\/)[A-Za-z0-9]+(?=.,!?\s)?", target)
    if len (redirect_token_from_url) > 0:
        redirect_request = requests.get (f"https://forms.gle/{redirect_token_from_url [0]}", allow_redirects = False)
        target = redirect_request.headers ["Location"]
    page_token_from_url = re.findall (r"(?<=\/)[a-zA-Z0-9-_]+(?=\/viewform)", target) [0]
    return page_token_from_url

def parse_shitty (shitty):
    shitty_lines = shitty.split ("\n")
    shitter_splitter = None
    for shitty_line in shitty_lines:
        result = re.findall (r"(?<=Content-Type: multipart\/alternative; boundary=\")[\s\S]+(?=\")", shitty_line)
        if len (result) == 0: continue
        shitter_splitter = result [0]
        break
    if shitter_splitter is None: raise Exception ("shit")
    sections = shitty.split (f"--{shitter_splitter}")
    header = sections [0]
    body_types = sections [1:-1]
    text_body = None
    for body_type in body_types:
        body_type = body_type.strip ()
        if body_type.startswith ("Content-Type: text/plain; charset=\"UTF-8\""):
            text_body = body_type.replace ("Content-Type: text/plain; charset=\"UTF-8\"", "").strip ()
            break
    if text_body is None: raise Exception ("shit again, no text body")
    return header, text_body
