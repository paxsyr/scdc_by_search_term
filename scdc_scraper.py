import argparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import json

parser = argparse.ArgumentParser(
    description="Scape the SCDC system for the contents of each job posting and store it in a .json"
)
parser.add_argument("-u", "--username", help="your Drexel abc123 (without @drexel.edu)")
parser.add_argument("-p", "--password", help="your Drexel password")
parser.add_argument(
    "-m",
    "--majors_to_search",
    nargs="*",
    help="the major(s) to search for. Arguments should be the 'value' of the <option> HTML tag (ex. EN-COM EN-ELEC for 'Eng. - Computer Engineering' and 'Eng. - Electrical Engineering')",
)
parser.add_argument(
    "-f", "--file_name", help="the name of the output file (without .json)"
)
args = parser.parse_args()

print("A new Chrome window should open momentarily")

chrome_options = Options()
# chrome_options.add_experimental_option(
#     "detach", True
# )  # used for testing - keeps window open after script terminates naturally
chrome_options.add_experimental_option(
    "excludeSwitches", ["enable-logging"]
)  # prevents "DevTools listening on . . ." and other messages from  outputting
driver = webdriver.Chrome(options=chrome_options)

driver.get("https://one.drexel.edu/")

wait = WebDriverWait(driver, 10)

sign_in_button = wait.until(
    EC.presence_of_element_located((By.NAME, "_eventId_proceed"))
)
sign_in_button.click()

if args.username == None:
    print("Input your abc123@drexel.edu in the window")
else:
    user_id_field = wait.until(EC.presence_of_element_located((By.NAME, "loginfmt")))
    user_id_field.send_keys(args.username + "@drexel.edu")
    user_id_field.send_keys(Keys.RETURN)

while "Enter password" not in driver.page_source:
    pass

if args.password == None:
    print("Input your password in the window")
else:
    password_field = wait.until(EC.presence_of_element_located((By.NAME, "passwd")))
    password_field.send_keys(args.password)
    password_field.send_keys(Keys.RETURN)

while "Approve sign in request" not in driver.page_source:
    pass

print("Approve the sign in request")

while driver.title != "Welcome - drexel.edu":
    pass

print("Wait while the program navigates to the SCDC system")

try:
    link = wait.until(
        EC.presence_of_element_located((By.LINK_TEXT, "CO-OP+CAREER SERVICES"))
    )
    link.click()
except:
    print('Failed to find "CO-OP+CAREER SERVICES"')
    driver.quit()

try:
    link = wait.until(
        EC.presence_of_element_located((By.LINK_TEXT, "Search for Co-op Jobs"))
    )
    link.click()
except:
    print('Failed to find "Search for Co-op Jobs"')
    driver.quit()

try:
    driver.switch_to.window(driver.window_handles[1])
except:
    print("Failed to switch current tab in Selenium")

if args.majors_to_search == None:
    print(
        'Select the major(s) you want to search for and then click "Search" at the bottom of the page'
    )
else:
    try:
        select_element = wait.until(EC.element_to_be_clickable((By.ID, "i_a_cmajs_id")))
        for major in args.majors_to_search:
            Select(select_element).select_by_value(major)
    except:
        print("Failed to select", major)
    try:
        search_button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//input[@type='submit' and @value='Search']")
            )
        )
        search_button.click()
    except:
        print('Failed to find "Search"')
        driver.quit()

while driver.title != "Job Search Results":
    pass

print("Wait while the program scrapes the contents of each job listing")

try:
    link_elements = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a"))
    )

    link_texts = [element.text for element in link_elements]

    if "2" in link_texts:
        page_max = "2"
        while True:
            if str(int(page_max) + 1) in link_texts:
                page_max = str(int(page_max) + 1)
            else:
                break
    else:
        page_max = "1"
except:
    print("Failed to get max page number")
    driver.quit()

co_ops_and_their_descriptions = {}

for page in range(1, int(page_max) + 1):
    if page != 1:
        try:
            link = wait.until(EC.presence_of_element_located((By.LINK_TEXT, str(page))))
            link.click()
        except:
            print('Failed to find "Search"')
            driver.quit()

    try:
        link_elements = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a"))
        )

        link_texts = [element.text for element in link_elements]

        co_op_link_texts = []

        for element in link_texts:
            if "(" in element and ")" in element:
                co_op_link_texts.append(element)
    except:
        print("Failed to get all the link texts on page", page)
        driver.quit()

    for link_text in co_op_link_texts:
        try:
            link = wait.until(
                EC.presence_of_element_located((By.LINK_TEXT, link_text.strip()))
            )  # Have to strip because a job title started with a space
            link.click()

            co_ops_and_their_descriptions[link_text] = driver.page_source

            driver.back()
        except:
            print("Failed to get the info for", link_text)
            driver.quit()

if args.username == None:
    print(
        "Input a filename for the results in the terminal (without .json). WARNING: This will overwrite any existing file of the same name"
    )
    file_name = input()
else:
    file_name = args.file_name

file_name = file_name + ".json"

with open(file_name, "w") as fp:
    json.dump(co_ops_and_their_descriptions, fp, indent=2)

print()
print(
    f'The file "{file_name}" now contains the information for all the jobs postings for the major(s) you selected'
)
print("Now use search_scdc_dump.py to search the jobs postings by keywords")
