import time
from turtle import st
from unittest import skip

from selenium import webdriver
from selenium.webdriver.common.by import By

import requests

import io

from PIL import Image

PATH = "D:\otavi\Driver\chromedriver.exe"

wd = webdriver.Chrome(PATH)

def get_image_urls(wd, delay, max_images):
    def scroll_down(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)

    url = "https://www.google.com/search?q=egrilo&sxsrf=ALiCzsbCbNPLeVXeVHYBY_-cnmQ8-HjoNg:1662817764370&source=lnms&tbm=isch&sa=X&ved=2ahUKEwi0l6_xror6AhV3rpUCHZuRASgQ_AUoAXoECAEQAw&biw=1920&bih=975&dpr=1"

    wd.get(url)

    image_urls = set()
    skips = 0
    
    while len(image_urls) + skips < max_images:
        scroll_down(wd)

        thumbnails = wd.find_elements(By.CLASS_NAME, "Q4LuWd")

        for img in thumbnails[len(image_urls) + skips:max_images]:
            try:
                img.click()
                time.sleep(delay)

            except Exception:
                continue
        
            images = wd.find_elements(By.CLASS_NAME, "n3VNCb")

            for image in images:

                if image.get_attribute('src') in image_urls:
                    max_images += 1
                    skips += 1
                    break

                if image.get_attribute('src') and 'http' in image.get_attribute('src'):
                    image_urls.add(image.get_attribute('src'))
                    print(f"Found: {len(image_urls)}")

    return image_urls


def download_image(download_path, url, file_name):
    try:
        image_content = requests.get(url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)
        file_path = download_path + file_name

        with open(file_path, "wb") as f:
            image.save(f, "JPEG")

        print("Success")

    except Exception as e:
        print('FAILED - ', e)

urls = get_image_urls(wd, 5, 10)

for i, url in enumerate(urls):
    download_image("imgs/", url, str(i) + ".jpg")

wd.quit()