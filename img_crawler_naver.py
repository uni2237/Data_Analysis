from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import urllib.request
 
driver = webdriver.Chrome()
driver.get("https://search.naver.com/search.naver?where=image&sm=tab_jum&query=")
elem = driver.find_element_by_name("query")
elem.send_keys("조인성")
elem.send_keys(Keys.RETURN)
 
SCROLL_PAUSE_TIME = 1
 
last_height = driver.execute_script("return document.body.scrollHeight")
 
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
 
    time.sleep(SCROLL_PAUSE_TIME)
 
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height
 
images = driver.find_elements_by_css_selector("._image._listImage")
count = 1
for image in images:
    try: 
        image.click()
        time.sleep(2)
        imgUrl = driver.find_element_by_xpath('//*[@id="main_pack"]/section/div[2]/div[2]/div/div[1]/div[1]/div[1]/div/div/div[1]/div[1]/img').get_attribute("src")
        urllib.request.urlretrieve(imgUrl, str(count) + ".jpg")
        count = count + 1
    except:
        pass
 
driver.close()