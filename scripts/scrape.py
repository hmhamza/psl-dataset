from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json


VOCAB_FILE = '../configs/vocab.json'
URLS_FILE = '../configs/urls.json'
TIMEOUT = 10


def click(driver, xpath, max_tries=5):
    tries = 0
    done = False
    while not done:
        try:
            WebDriverWait(driver, TIMEOUT).until(
                EC.element_to_be_clickable((By.XPATH, xpath))).click()
            done = True
        except Exception:
            tries += 1
            if tries > max_tries:
                return False
            print('Trying again..', end='  ')
            driver.refresh()
    return True        


def navigate_to_category(driver, baseURL, category):
    driver.get(baseURL)

    # Clicking "PSL Dictionary" in the navbar
    xpath = "//*[@id=\"navbarNavDropdown\"]/ul/li[2]/a"
    click(driver, xpath)
    
    # Clicking the required category
    xpath = "//img[contains(@alt,'"+category+"')]"
    click(driver, xpath)


def navigate_to_word(driver, word):
    xpath = '//*[text()="'+word+'"]'
    if not click(driver, xpath):
        return False, None
   
    xpath = '//div[contains(@class, "plyr__video-wrapper")]'
    WebDriverWait(driver, TIMEOUT).until(EC.visibility_of_element_located((By.XPATH, xpath)))

    html_source = driver.page_source

    soup = BeautifulSoup(html_source, 'html.parser')
    links = soup.findAll('source', {'size': True})

    data = {'word': word}
    for link in links:
        data[link['size']] = link['src']

    return True, data


def scrape():
    options = webdriver.ChromeOptions()
    options.add_argument('--kiosk')
    driver = webdriver.Chrome(options=options)

    config = json.load(open(VOCAB_FILE))

    results = dict()
    results['links'] = []

    total_words = 0
    success_count = 0
    for category in config['vocabulary']:
        navigate_to_category(driver, config['baseURL'], category['category'])
        for word in category['words']:
            print('\n[Total: '+str(total_words)+'  Failed: '+str(total_words -
                  success_count)+']   Word: '+word['word']+'', end='        ')
            success, data = navigate_to_word(driver, word['word'])

            if success:
                success_count += 1
                results['links'].append(data)
                driver.back()

            total_words+=1

    driver.close()
    driver.quit()

    print('\n\nTotal words: '+str(total_words) +
          '   Successfully scraped: '+str(success_count))

    jsonResults = json.dumps(results, indent=4)
    jsonFile = open(URLS_FILE, 'w')
    jsonFile.write(jsonResults)
    jsonFile.close()


scrape()