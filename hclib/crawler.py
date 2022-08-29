from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions

import random, re, os
# import requests
from bs4 import BeautifulSoup

import time
from . import htime
import requests, shutil


'''
Checker Functions
'''



# Get a new record
def get_new_record():
    # Get New File Name
    file_name = "hermes_hist_" + htime.get_time_str_now() + ".html"

    # object of FirefoxOptions
    try:
        options = webdriver.FirefoxOptions()
        # set options.headless to True
        # options.headless = True
        driver = webdriver.Firefox(options=options)
        print("[Crawler] created driver instance")
    except:
        print("[Crawler] NO created driver instance")
        return "None"
    try:
        # Access webpage
        driver.implicitly_wait(0.4)
        driver.get("https://www.hermes.com/us/en/category/women/bags-and-small-leather-goods/#|")
        time.sleep(4)
        print("[Crawler] gotten first webpage")
    except:
        pass
        print("[Crawler] NO first webpage")
        driver.quit()
        return "None"

    try:
        # Click load more button
        buttons = driver.find_element(By.CLASS_NAME, "button-base").click()
        # Scroll Down 7 times
        for i in range(0,9):
            print("[Crawler] Scrolled")
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight);") 
            time.sleep(2)
    except:
        print("[Crawler] NO scrolled")
        pass

    temp_file_name = "temp_" + file_name
    with open(temp_file_name, "w") as file:
        file.write(driver.page_source)
        file.close()

    driver.quit()
    os.rename(temp_file_name, file_name)
    if os.path.isfile(temp_file_name):
        os.remove(temp_file_name)
        
    print("[Crawler] File Created")
    return file_name


'''
def legacy_get_new_record(self, new_file_name):
    # Get new file
    r = requests.get("https://www.hermes.com/us/en/category/women/bags-and-small-leather-goods/#|")
    new_temp_file_name = "temp_" + new_file_name

    with open(new_temp_file_name, "w") as file:
        file.write(r.text)
        file.close()
    # change temp file to official file when write completes
    os.rename(new_temp_file_name, new_file_name)
    if os.path.isfile(new_temp_file_name):
        os.remove(new_temp_file_name)
'''


def get_image(link, name):
    # Define New File
    if not os.path.isdir("img_cache"):
        os.path.mkdir("img_cache")

    new_file_name = str(name) + ".png"
    new_temp_file_name = "img_cache/temp_" + new_file_name
    print("[Crawler] Getting image {0}".format(new_file_name))
    
    # Download and write new file
    response = requests.get(link, stream=True)
    with open(new_temp_file_name, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response

    # change temp file to official file when write completes
    os.rename(new_temp_file_name, "img_cache/" + new_file_name)
    if os.path.isfile(new_temp_file_name):
        os.remove(new_temp_file_name)
    print("[Crawler] Gotten image {0}".format(new_file_name))
    # os.chdir("..")
    return "img_cache/" + new_file_name


def is_blocked(file):
    with open(file) as fp:
        soup = BeautifulSoup(fp, "html.parser")
        lst = soup.find_all("div", class_="product-item")
    if len(lst) == 0:
        return True
    return False

# Process last file
def extract(file):
    names = []
    links = []
    images = []
    print("[Crawler] Extracting File Content")

    if not os.path.isfile(file):
        print("[Crawler] Extraction Failed: No Such File")
        return names, links, images

    with open(file) as fp:
        soup = BeautifulSoup(fp, "html.parser")
        # print(soup.head.title.text)
        lst = soup.find_all("div", class_="product-item")

    for element in lst:
        # Item Name
        item_name = ""
        try: item_name = element.a.h4.text
        except: continue
        # Item URL
        item_url = "None"
        try: item_url = "https://hermes.com" + element.a['href']
        except: item_url = "None"
        # Item Image URL
        image_url = "None"
        try:
            if 'data-srcset' in element.a.picture.source.attrs:
                image_url = "https:" + element.a.picture.source['data-srcset'].split("?")[0] + "?&wid=200&hei=200"
            elif 'srcset' in element.a.picture.source.attrs:
                image_url = "https:" + element.a.picture.source['srcset'].split("?")[0] + "?&wid=200&hei=200"
        except: image_url = "None"
        # Add to list
        names.append(item_name)     
        links.append(item_url)
        images.append(image_url)
    print("[Crawler] Extracted {0} Items".format(len(names)))
    return names, links, images
    


def compare(old_record, old_link, old_image, new_record, new_link, new_image):
    rtn_record = []
    rtn_links = []
    rtn_images = []
    print("[Crawler] Comparing File Content {0} vs {1}".format(len(old_record), len(new_record)))
    pattern = re.compile("[Ll]indy|[Pp]icotin")
    # [Pp]icotin | [Ll]indy | 

    # Compare Old and New Content
    i=1
    while i < len(new_record):
        if new_record[i] not in old_record: 
            print("[Crawler] Checking item {0}".format(new_record[i]))
            if re.findall(pattern, new_record[i]):
                rtn_record.append(new_record[i])
                rtn_links.append(new_link[i])
                rtn_images.append(new_image[i])
                print("[Crawler] Found New Item")
            print("[Crawler] Skipped Item")
        i+=1
    print("[Crawler] Found {0} different Items".format(len(rtn_record)))
    return rtn_record, rtn_links, rtn_images




if __name__ == "__main__":
    # extract("TestPage2.html")
    # Get New Record
    # new_file = get_new_record()

    # Process history
    '''
    new_record, new_links, new_images = extract(new_file)
    if len(new_images):
        print(new_images[0])
    '''
    print(is_blocked("hermes_hist_2022_8_18_22_13_30.html"))