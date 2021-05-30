#캔: 코카콜라/ 밀키스/ 칠성사이다/ 비락식혜/ 월체스(보라)
#컵라면 : 신라면/ 팔도비빔면 / 왕뚜껑/ 까르보불닭/ 짜장범벅
#아이스크림: 메로나 보석바 스크류바 쌍쌍바 비비빅
#페트병:코카콜라/ 밀키스/ 칠성사이다/ 비락식혜/ 월체스(보라)
#봉지과자:새우깡/ 허니버터칩 /꿀꽈배기 /오감자 /포스틱
from selenium import webdriver
from bs4 import BeautifulSoup as soups
from selenium.common.exceptions import WebDriverException
from urllib.error import HTTPError, URLError
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, \
    ElementNotInteractableException
from PIL import Image
from urllib.request import urlretrieve
import os
import time
import socket


def filtering(folder_name):
    print("ㅡ 필터링 시작 ㅡ")
    filtered_count = 0
    dir_name = "D:/졸프/data_crawling/" +folder_name
    for index, file_name in enumerate(os.listdir(dir_name)):
        try:
            file_path = dir_name+ str(filtered_count) + ".jpg"
            img = Image.open(file_path)

            # 이미지 해상도의 가로와 세로가 모두 416이하인 경우
            if img.width < 416 or img.height < 416:
                img.close()
                os.remove(file_path)
                print(f"{index} 번째 사진 삭제 ({img.width},{img.height})")
                
            else:
                area = (0,0,416,416)
                crop_image = img.crop(area)
                crop_image= crop_image.convert("RGB")
                crop_image.save(dir_name+ str(filtered_count) + "_.jpg")
                print(f"{index} 번째 사진 변환 후 사이즈 ({img.width},{img.height})->({crop_image.width},{crop_image.height})")

        except :
            pass
        
        
        
        filtered_count += 1
            

    
def click_and_retrieve(folder_name,driver,index, img, img_list_length,count):
    
    try:
        img.click()
        driver.implicitly_wait(3)
        #src = driver.find_element_by_xpath(
        #    '//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div[1]/div[1]/div/div[2]/a/img').get_attribute('src')
        src=driver.find_element_by_xpath("/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div/div[2]/a/img").get_attribute('src')
        # src.split('.')[-1] = 확장자
        urlretrieve(src,"D:/졸프/Data_Analysis/data_crawling/" +folder_name+ str(count) + ".jpg")

    except HTTPError:
        print("ㅡ HTTPError & 패스 ㅡ")
        pass

    except NoSuchElementException:
        print("ㅡ NoSuchElementException ㅡ")
        pass

def search_selenium(search_name, search_path, search_limit, folder_name) :
    search_url = "https://www.google.com/search?as_st=y&tbm=isch&hl=ko&as_q=" + str(search_name) + "&as_epq=&as_oq=&as_eq=&cr=&as_sitesearch=&safe=images&tbs=itp:photo"
    
    driver = webdriver.Chrome('D:/졸프/Data_Analysis/chromedriver.exe')
    options=webdriver.ChromeOptions()
    #options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("--window-size=1920,1080")
    driver.get(search_url)
    driver.maximize_window()
    
    
    div = driver.find_element_by_xpath('//*[@id="islrg"]/div[1]')
    img_list = div.find_elements_by_css_selector(".rg_i.Q4LuWd")

    cnt=0
    for index,img in enumerate(img_list):
        if (cnt==search_limit):
            break
        try:
            click_and_retrieve(folder_name,driver,index, img, len(img_list),cnt)
            cnt=cnt+1
        except ElementClickInterceptedException:
            print("ㅡ ElementClickInterceptedException ㅡ")
            driver.execute_script("window.scrollTo(0, window.scrollY + 100)")
            print("ㅡ 100만큼 스크롤 다운 및 3초 슬립 ㅡ")
            time.sleep(3)
            click_and_retrieve(folder_name,driver,index, img, len(img_list),cnt)
            cnt=cnt+1
        
        except NoSuchElementException:
            print("ㅡ NoSuchElementException ㅡ")
            driver.execute_script("window.scrollTo(0, window.scrollY + 100)")
            print("ㅡ 100만큼 스크롤 다운 및 3초 슬립 ㅡ")
            time.sleep(3)
            click_and_retrieve(folder_name,driver,index, img, len(img_list),cnt)
            cnt=cnt+1

        except ConnectionResetError:
            print("ㅡ ConnectionResetError & 패스 ㅡ")
            pass

        except URLError:
            print("ㅡ URLError & 패스 ㅡ")
            pass

        except socket.timeout:
            print("ㅡ socket.timeout & 패스 ㅡ")
            pass

        except socket.gaierror:
            print("ㅡ socket.gaierror & 패스 ㅡ")
            pass

        except ElementNotInteractableException:
            print("ㅡ ElementNotInteractableException ㅡ")
            break
 
        
    driver.close()
    
    filtering(folder_name)


if __name__ == "__main__" :


    search_path = "Your Path"

    search_selenium("꿀꽈배기", search_path,100, "봉지과자/꿀꽈배기/")
    
    print("끝!")
    