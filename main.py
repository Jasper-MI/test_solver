from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import google.generativeai as genai

genai.configure(api_key="**************")
model = genai.GenerativeModel("gemini-1.5-flash")

# Set up the Selenium WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open the webpage
url = "https://lms.bht-berlin.de/mod/quiz/review.php?attempt=753871&cmid=987649"
driver.get(url)

# Wait for the page to load (adjust sleep time as needed or use WebDriverWait)
driver.implicitly_wait(100)

# Locate the qtext class
try:
    qtext_divs = driver.find_elements(By.CLASS_NAME, 'qtext')
    answer_divs = driver.find_elements(By.CLASS_NAME, 'answer')


    if len(qtext_divs) != len(answer_divs):
        print("The number of questions and answers are not the same!")

    for index, (qtext, answer) in enumerate(zip(qtext_divs, answer_divs), start=1):

        response_quote = "Gebe zu folgender Aufgabe eine sehr kurze Antwort, welche Antwortmöglichkeit richtig ist. " + qtext.text + answer.text
        response = model.generate_content(response_quote)
        #print("--------Question---------\n" , qtext.text , "\n-----------------")
        #print("\n")
        #print("--------Answers---------\n" , answer.text , "\n-----------------")
        #print("\n")
        print("--------Answers---------\n", index , ". ", response.text , "\n-----------------")
        print("\n")

except Exception as e:
    print("Could not find qtext class:", e)

# Close the browser
# driver.quit()
