import requests
import bs4
import json
import pickle
import os.path
import dump_cookies

question_types = {
    0: "short_answer",
    1: "paragraph",
    2: "multiple_choice",
    4: "checkboxes",
    3: "dropdown",
    8: "section_title",
    11: "weird_thing"
}

def analyze (token, info):
    pprint = lambda shit: print (json.dumps (shit, indent = 2))

    url = f"https://docs.google.com/forms/d/e/{token}/viewform"
    cookie_file_path = f"cookies/{info [0]}.p"
    if not os.path.isfile (cookie_file_path): dump_cookies.dump_cookies (info [0])
    with open (f"cookies/{info [0]}.p", "rb") as cookie_file:
        jar = pickle.load (cookie_file)
    response = requests.get (url, cookies = jar).text
    html = bs4.BeautifulSoup (response, "html.parser")
    if html.title.string == "Page Not Found":
        raise Exception ("Invalid token!")
    script_tags = list (html.find_all ("script"))
    last_script_tag = script_tags [-2].string
    BEGINNING = "var FB_PUBLIC_LOAD_DATA_ = "
    END = "\n;"
    last_script_tag = last_script_tag [len (BEGINNING):(len (last_script_tag) - len (END))]
    free_bird_public_load_data = json.loads (last_script_tag)
    # (These indices are extracted from a dump of a test form's HTML)
    detailed_info = free_bird_public_load_data [1]
    # noinspection PyUnusedLocal
    description = detailed_info [0]
    questions = detailed_info [1]
    # noinspection PyUnusedLocal
    name = detailed_info [8]
    # print (f"Description: {description}, name: {name}")
    out_questions = []
    section_count = 1
    for in_question in questions:
        question = {
            "id": in_question [0],
            "name": in_question [1]
        }
        if in_question [3] in question_types:
            question ["type"] = question_types [in_question [3]]
        else:
            question ["type"] = "unknown"
        if question ["type"] == "weird_thing": continue
        if question ["type"] == "section_title":
            section_count += 1
            continue
        question ["answer_info"] = in_question [4]
        out_questions.append (question)

    response_body = {}

    name = info [1].split (" ")
    cohort_number = info [2]

    # info is in the format ["reed.eric2022@istemghs.org", "Eric Reed", "Petrecca", "More gaming would be cool"]

    draft = []

    # noinspection PyUnusedLocal
    def add_normal (_answer_id, answer_value):
        response_body [f"entry.{_answer_id}"] = answer_value
    def add_draft (_answer_id, answer_value):
        draft.append ([None, _answer_id, [answer_value], 0])
    add = add_draft

    for question in out_questions:
        answer_id = question ['answer_info'] [0] [0]
        lower_name = question ["name"].lower ()
        type_is = lambda check_type: question ["type"] == check_type
        def is_yes_no (lenient = False):
            if not type_is ("multiple_choice"): return False
            _answer_list = question ["answer_info"] [0] [1]
            return _answer_list [0] [0] == "Yes" and (_answer_list [1] [0] == "No" or lenient)
        print (f"Question ID: {question ['id']}")
        print (f"Answer ID: {answer_id}")
        print (f"Lowercase name: {lower_name}")
        print (f"Type: {question ['type']}")

        if "first" in lower_name and "name" in lower_name and type_is ("short_answer"):
            print (f"DETECTED FIRST NAME, setting {answer_id} to {name [0]}")
            add (answer_id, name [0])
        elif "last" in lower_name and "name" in lower_name and type_is ("short_answer"):
            print (f"DETECTED LAST NAME, setting {answer_id} to {name [1]}")
            add (answer_id, name [1])
        elif "cohort" in lower_name and type_is ("multiple_choice"):
            answer_list = question ["answer_info"] [0] [1]
            selected = None
            for answer in answer_list:
                if cohort_number in answer [0].lower ():
                    selected = answer [0]
            if selected is None: raise Exception ("couldn't find selected")
            print (f"DETECTED COHORT SELECTION: {selected}")
            add (answer_id, selected)
        elif "ccp" in lower_name and type_is ("multiple_choice"):
            print ("DETECTED CCP")
            add (answer_id, "No")
        elif "understand" in lower_name and is_yes_no (lenient = True):
            print ("DETECTED UNNECESSARY CONFIRMATION")
            add (answer_id, "Yes")
        elif "breakout" in lower_name and not "second" in lower_name and not "third" in lower_name and type_is ("dropdown"):
            answer_list = question ["answer_info"] [0] [1]
            selected = None
            for answer in answer_list:
                if info [3] [0].lower () in answer [0].lower ():
                    selected = answer [0]
            if selected is None:
                print ("Taken, choosing alternative (default)")
                selected = answer_list [0] [0]
            add (answer_id, selected)
            print (f"DETECTED BREAKOUT SELECT, returning {selected}")
        elif "first" in lower_name and is_yes_no ():
            print ("DETECTED FIRST VALIDATION")
            add (answer_id, "Yes")
        elif "second" in lower_name and not "third" in lower_name and type_is ("dropdown"):
            answer_list = question ["answer_info"] [0] [1]
            selected = None
            for answer in answer_list:
                if info [3] [1].lower () in answer [0].lower ():
                    selected = answer [0]
            if selected is None:
                print ("Taken, choosing alternative (default)")
                selected = answer_list [0] [0]
            add (answer_id, selected)
            print (f"DETECTED SECONDARY BREAKOUT SELECT, returning {selected}")
        elif "third" in lower_name and type_is ("dropdown"):
            answer_list = question ["answer_info"] [0] [1]
            selected = None
            for answer in answer_list:
                if info [3] [2].lower () in answer [0].lower ():
                    selected = answer [0]
            if selected is None:
                print ("Taken, choosing alternative (default)")
                selected = answer_list [0] [0]
            add (answer_id, selected)
            print (f"DETECTED TERTIARY BREAKOUT SELECT, returning {selected}")
        elif "future" in lower_name and type_is ("paragraph"):
            add (answer_id, info [4])
            print (f"DETECTED FUTURE, returning {info [4]}")
        elif is_yes_no ():
            add (answer_id, "No")
            print (f"DETECTED OTHER YES/NO, returning no")
        else:
            print ("NO IDEA")
        print ("#" * 10)

    # Get token
    script_tags = list (html.find_all ("script"))
    TOKEN_BEGINNING = "_docs_flag_initialData="
    TOKEN_END = ";"
    script_tag = None
    for potential_script_tag in script_tags:
        if potential_script_tag.string is None: continue
        if potential_script_tag.string.startswith (TOKEN_BEGINNING):
            script_tag = potential_script_tag
            break
    if script_tag is None: raise Exception ("Couldn't find script tag")
    script_tag_text = script_tag.string
    token_json = script_tag_text [len (TOKEN_BEGINNING):(len (script_tag_text) - len (TOKEN_END))]
    token_data = json.loads (token_json)
    print (f"Extracted token: {token_data ['info_params'] ['token']}")

    input_tags = list (html.find_all ("input"))
    freebird_submission_token = None
    for input_tag in input_tags:
        if input_tag ["type"] != "hidden": continue
        if input_tag ["name"] != "fbzx": continue
        freebird_submission_token = input_tag ["value"]
    if freebird_submission_token is None: raise Exception ("Couldn't find fbzx")
    print (f"Extracted fbzx: {freebird_submission_token}")

    response_body ["emailReceipt"] = ""
    response_body ["fvv"] = "1"
    response_body ["token"] = token_data ["info_params"] ["token"]
    response_body ["fbzx"] = freebird_submission_token
    response_body ["draftResponse"] = json.dumps ([draft, None, freebird_submission_token, None, None, None, info [0], 0])
    response_body ["pageHistory"] = ','.join (str (page_number) for page_number in range (section_count))
    pprint (response_body)

    response = requests.post (f"https://docs.google.com/forms/d/e/{token}/formResponse", cookies = jar, data = response_body)
    print (response)
