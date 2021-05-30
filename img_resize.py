from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, \
    ElementNotInteractableException
from PIL import Image
from urllib.request import urlretrieve
import os


def filtering(search_limit,folder_name):
    
    filtered_count = 0
    dir_name = "D:/졸프/data_crawling/" +folder_name
    for index, file_name in enumerate(os.listdir(dir_name)):
        try:
            if filtered_count==search_limit:
                return
            file_path = dir_name+ str(filtered_count) + ".jpg"
            img = Image.open(file_path)

            # 이미지 해상도의 가로와 세로가 모두 416이하인 경우
            if img.width < 416 or img.height < 416:
                img.close()
                os.remove(file_path)
                print(f"{index} 번째 사진 삭제 ({img.width},{img.height})")
                
            else:
                # 이미지 crop
                #area = (0,0,416,416)
                #crop_image = img.crop(area)
                #crop_image= crop_image.convert("RGB")
                #crop_image.save(dir_name+ str(filtered_count) + "_.jpg")
                #print(f"{index} 번째 사진 변환 후 사이즈 ({img.width},{img.height})->({crop_image.width},{crop_image.height})")

                # 이미지 resize
                img_resize_lanczos = img.resize((416, 416), Image.LANCZOS)
                img_resize_lanczos.save(dir_name+ str(filtered_count) + "_.jpg")
                print(f"{index} 번째 사진 변환 후 사이즈 ({img.width},{img.height})->({img_resize_lanczos.width},{img_resize_lanczos.height})")

            filtered_count += 1
        except :
            filtered_count += 1
            pass
        
        
        
        
    
    print(folder_name+" 끝!")


if __name__ == "__main__" :
    
    #filtering(100,"봉지과자/꿀꽈배기/")
    #filtering(100, "봉지과자/새우깡/")
    filtering( 100, "봉지과자/오감자/")
    filtering( 100, "봉지과자/포스틱/")
    filtering( 100, "봉지과자/허니버터칩/")

    filtering(  100, "아이스크림/메로나/")
    filtering( 100, "아이스크림/보석바/")
    filtering( 100, "아이스크림/비비빅/")
    filtering( 100, "아이스크림/스크류바/")
    filtering( 100, "아이스크림/쌍쌍바/")

    filtering( 100, "캔/밀키스/")
    filtering( 100, "캔/비락식혜/")
    filtering(  100, "캔/웰치스/")
    filtering(  100, "캔/칠성사이다/") 
    filtering(  100, "캔/코카콜라/")


    filtering( 100, "컵라면/까르보불닭/")
    filtering(  100, "컵라면/신라면/")
    filtering(  100, "컵라면/왕뚜껑/")
    filtering(  100, "컵라면/짜장범벅/")
    filtering(  100, "컵라면/팔도비빔면/")


    filtering( 100, "페트병/밀키스/")
    filtering(  100, "페트병/비락식혜/")
    filtering(  50, "페트병/웰치스/")
    filtering( 50, "페트병/웰치스/")
    filtering(  100, "페트병/칠성사이다/")
    filtering( 100, "페트병/코카콜라/")

    
   