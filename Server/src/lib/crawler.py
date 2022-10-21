import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

import random, re, os
from bs4 import BeautifulSoup

import time, sys
from . import utils
# import utils                      # Testing Include
import requests, shutil


'''Checker Functions'''

# Get a new record
def get_new_record(logger, root):
    # Get New File Name
    file_dir = root + "record_cache/"
    file_name = "Hermes_Record_" + utils.get_time_str_now() + ".html"
    options = uc.ChromeOptions()
    options.headless=False
    ff = uc.Chrome(options=options)

    logger.log("Crawler", "created driver instance")

    ff.get("https://hermes.com/us/en")
    time.sleep(3.62)

    buttons = ff.find_element(By.ID, "collection-button").click()
    time.sleep(2.15)
    women_button_candidates = ff.find_elements(By.XPATH,"//li[@class='nav-item']")
    for candidate in women_button_candidates:
        if "Bags and clutches" in candidate.text:
            candidate.click()
            break
    
    time.sleep(3.38)
    ff.get("https://www.hermes.com/us/en/category/women/bags-and-small-leather-goods/bags-and-clutches/")
    time.sleep(1.4)
    logger.log("Crawler", "gotten first webpage")

    try:
        # Click load more button
        bt = ff.find_elements(By.CLASS_NAME, "button-base")
        fnd = False
        for ele in bt:
            if ele.text == "Load more items":
                logger.log("[Crawler] Found Load More Items Button")
                fnd = True
                ele.click()
                time.sleep(1.55)
        if fnd == False:
            logger.log("Crawler", "Load More Button Not Found")
        # Scroll Down 
        for i in range(0,6):
            # ff.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            for i in range(1, total_height, 5):
                ff.execute_script("window.scrollTo(0, {});".format(i))
            logger.log("Crawler", "Scrolled")
            time.sleep(1.26)
    except:
        logger.log("Crawler", "NO scrolled")

    # Write to temp file
    with open(file_dir + "temp_" + file_name, "w") as file:
        file.write(ff.page_source)
        file.close()
    time.sleep(3)
    ff.quit()
    
    # Rename completed file
    os.rename(file_dir + "temp_" + file_name, file_dir + file_name)
    if os.path.isfile(file_dir + "temp_" + file_name):
        os.remove(file_dir + "temp_" + file_name)
    logger.log("Crawler", "File {0} Created".format(file_name))
    return file_dir + file_name



def get_image(logger, root, link, name):
    image_cache_dir = root + "image_cache/"

    new_file_name = str(name) + ".png"
    logger.log("Crawler", "Getting image {0}".format(new_file_name))
    
    # Download and write new file
    response = requests.get(link, stream=True)
    with open(image_cache_dir + "temp_" + new_file_name, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response

    # change temp file to official file when write completes
    os.rename(image_cache_dir + "temp_" + new_file_name, image_cache_dir + new_file_name)
    if os.path.isfile(image_cache_dir + "temp_" + new_file_name):
        os.remove(image_cache_dir + "temp_" + new_file_name)
    logger.log("Crawler", "Gotten image {0}".format(new_file_name))
    return image_cache_dir + new_file_name




# Process last file
def extract(logger, file):
    names = []
    links = []
    images = []
    logger.log("Crawler", "Extracting File Content")

    if not os.path.isfile(file):
        logger.log("Crawler", "Extraction Failed: No Such File")
        return names, links, images

    lst = []
    with open(file) as fp:
        soup = BeautifulSoup(fp, "html.parser")
        # logger.log(soup.head.title.text)
        lst = soup.find_all("div", class_="product-item")
    logger.log("Crawler", "{0} Items in Parsed File".format(len(lst)))

    for element in lst:
        # Get item name
        item_name = ""
        try: 
            item_name = element.a.contents[1].span.text
            logger.log("Crawler", "Fetched item {0}".format(item_name))
        except: 
            logger.log("Crawler", "Failed to fetch item name")
            continue                                                    # If iten not parsed, skip
        # Get item URL  
        item_url = "None"
        try: item_url = "https://hermes.com" + element.a['href']
        except: item_url = "None"
        # Get item image URL
        image_url = "None"
        try:
            if 'data-srcset' in element.a.picture.source.attrs:
                image_url = "https:" + element.a.picture.source['data-srcset'].split("?")[0] + "?&wid=100&hei=100"
            elif 'srcset' in element.a.picture.source.attrs:
                image_url = "https:" + element.a.picture.source['srcset'].split("?")[0] + "?&wid=100&hei=100"
        except: image_url = "None"
        # Add to list
        names.append(item_name)     
        links.append(item_url)
        images.append(image_url)
    logger.log("Crawler", "Extracted {0} Items".format(len(names)))
    return names, links, images
    

def compare(logger, tracking_list, old_record, old_link, old_image, new_record, new_link, new_image):
    rtn_record = []
    rtn_links = []
    rtn_images = []
    logger.log("Crawler", "Comparing File Content {0} vs {1}".format(len(old_record), len(new_record)))
    
    # Generate regular expresion tracker
    regex = ""
    for bag in tracking_list:
        regex += '['+bag[0].lower()+bag[0].upper()+']' + bag[1:] + "|"
    pattern = re.compile(regex[:-1])
    # [Pp]icotin | [Ll]indy | 

    # Compare Old and New Content
    i=1
    while i < len(new_record):
        if new_record[i] not in old_record: 
            logger.log("Crawler", "Checking item {0}".format(new_record[i]))
            if re.findall(pattern, new_record[i]):
                rtn_record.append(new_record[i]); rtn_links.append(new_link[i]); rtn_images.append(new_image[i])
                logger.log("Crawler", "Found New Item")
            logger.log("Crawler", "Skipped Item")
        i+=1
    logger.log("Crawler", "Found {0} different Items".format(len(rtn_record)))
    return rtn_record, rtn_links, rtn_images




if __name__ == "__main__":
    extract(sys.argv[1])