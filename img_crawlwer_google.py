from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import urllib.request
 
def search_selenium(search_name,search_limit,folder_name):
    time.sleep(2)
    driver = webdriver.Chrome()
    driver.get("https://www.google.co.kr/imghp?hl=ko&ogbl")
    elem = driver.find_element_by_name("q")
    elem.send_keys(search_name)
    elem.send_keys(Keys.RETURN)
 
    SCROLL_PAUSE_TIME = 1
 
    last_height = driver.execute_script("return document.body.scrollHeight")
 
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
 
        time.sleep(SCROLL_PAUSE_TIME)
 
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            try:
                driver.find_element_by_css_selector(".mye4qd").click()
            except:
                break
        last_height = new_height
 
    images = driver.find_elements_by_css_selector(".rg_i.Q4LuWd")
    count = 0
    for image in images:
        try: 
            if count==search_limit:
                break
            image.click()
            time.sleep(2)
            imgUrl = driver.find_element_by_xpath('/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div/div[2]/a/img').get_attribute("src")
            urllib.request.urlretrieve(imgUrl, "D:/졸프/data_crawling/" +folder_name+ str(count) + ".jpg")
            count = count + 1
        except:
            pass
 
    driver.close()
    print("=============== "+search_name+" 크롤링 끝! ================")

if __name__ == "__main__" :
    
    search_selenium("꿀꽈배기",100, "봉지과자/꿀꽈배기/")
    #search_selenium("새우깡", 100, "봉지과자/새우깡/")
    #search_selenium("오감자 그라탕",  100, "봉지과자/오감자/")
    #search_selenium("포스틱",  100, "봉지과자/포스틱/")
    #search_selenium("허니버터칩",  100, "봉지과자/허니버터칩/")

    #search_selenium("메로나",  100, "아이스크림/메로나/")
    #search_selenium("보석바",  100, "아이스크림/보석바/")
    #search_selenium("비비빅",  100, "아이스크림/비비빅/")
    #search_selenium("스크류바",  100, "아이스크림/스크류바/")
    #search_selenium("쌍쌍바",  100, "아이스크림/쌍쌍바/")

    #search_selenium("밀키스 캔",  100, "캔/밀키스/")
    #search_selenium("비락식혜 캔",  100, "캔/비락식혜/")
    #search_selenium("웰치스 포도 캔",  100, "캔/웰치스/")
    #search_selenium("칠성사이다 캔",  100, "캔/칠성사이다/") 
    #search_selenium("코카콜라 캔",  100, "캔/코카콜라/")


    #search_selenium("까르보불닭 컵", 100, "컵라면/까르보불닭/")
    #search_selenium("신라면 컵",  100, "컵라면/신라면/")
    #search_selenium("왕뚜껑 컵",  100, "컵라면/왕뚜껑/")
    #search_selenium("짜장범벅",  100, "컵라면/짜장범벅/")
    #search_selenium("팔도비빔면 컵",  100, "컵라면/팔도비빔면/")


    #search_selenium("밀키스 페트",  100, "페트병/밀키스/")
    #search_selenium("비락식혜 페트",  100, "페트병/비락식혜/")
    #search_selenium("웰치스 포도 페트",  50, "페트병/웰치스/")
    #search_selenium("웰치스 포도 1.5",  50, "페트병/웰치스/")
    #search_selenium("칠성사이다 페트",  100, "페트병/칠성사이다/")
    #search_selenium("코카콜라 페트", 100, "페트병/코카콜라/")

    
    print("크롤링 전체 끝!")
    