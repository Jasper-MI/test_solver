from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import google.generativeai as genai

# set up some things
genai.configure(api_key="***********")
model = genai.GenerativeModel("gemini-1.5-flash")

# Set up the Selenium WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

counter = 1

# Open the webpage
url = "https://lms.bht-berlin.de/mod/quiz/review.php?attempt=748510&cmid=1136083&showall=0"
driver.get(url)

# Wait for the page to load (adjust sleep time as needed or use WebDriverWait)
driver.implicitly_wait(100)


# login-page 
user_name = ""
user_password = ""

if ((user_name != "") and (user_password != "")): 
    input_name = driver.find_element(By.ID, "username")
    input_password = driver.find_element(By.ID, "password")

    input_name.send_keys(user_name)
    input_password.send_keys(user_password)

    login_button = driver.find_element(By.ID, "loginbtn")
    login_button.click()


while True:

    break_condition = 0

    # Locate the qtext class
    try:
        qtext_divs = driver.find_elements(By.CLASS_NAME, 'qtext')
        answer_divs = driver.find_elements(By.CLASS_NAME, 'answer')


        if len(qtext_divs) != len(answer_divs):
            print("The number of questions and answers are not the same!")

        for index, (qtext, answer) in enumerate(zip(qtext_divs, answer_divs), start=1):
            break_condition = index
            response_quote = "Gebe zu folgender Aufgabe eine sehr kurze Antwort, welche Antwortmöglichkeit richtig ist. " + qtext.text + answer.text
            response = model.generate_content(response_quote)
            #print("--------Question---------\n" , qtext.text , "\n-----------------")
            #print("\n")
            #print("--------Answers---------\n" , answer.text , "\n-----------------")
            #print("\n")

            print("--------Answers---------\n", counter , ". ", response.text , "\n-----------------")
            print("\n")

            # check the box
            check_box_answer = response.text[0]
            correct_option_parent = driver.find_element(By.CLASS_NAME, "answer")
            if (check_box_answer == "a") or (check_box_answer == "b") or (check_box_answer == "c") or(check_box_answer == "d"):
                match check_box_answer:
                    case "a":
                        correct_option_child = correct_option_parent.find_elements(By.XPATH, "./div")[0]
                    case "b":
                        correct_option_child = correct_option_parent.find_elements(By.XPATH, "./div")[1]
                    case "c":
                        correct_option_child = correct_option_parent.find_elements(By.XPATH, "./div")[2]
                    case "d":
                        correct_option_child = correct_option_parent.find_elements(By.XPATH, "./div")[3]
                
                if not correct_option_child.is_selected():
                    correct_option_child.click()

            counter = counter + 1
            

    except Exception as e:
        print("Could not find qtext class:", e)
    
    if break_condition > 1:
        driver.quit()
        exit()
    
    try:
        driver.find_element(By.CSS_SELECTOR, "a.arrow_link.mod_quiz-next-nav")
        print("Arrow found")
        link = driver.find_element(By.CSS_SELECTOR, "a.arrow_link.mod_quiz-next-nav")
        link.click()
        driver.implicitly_wait(10)
    except Exception:
        print("closed")
        driver.quit()
        exit()

