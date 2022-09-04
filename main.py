import zipfile
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import time

driver = webdriver.Chrome('D:\Development\chromedriver\chromedriver.exe')

def single_element_search(by_type, source_element, search_pattern):
    try:
        if by_type == 'xpath':
            element = source_element.find_element(By.XPATH, search_pattern)
            return element
        if by_type == 'id':
            element = source_element.find_element(By.ID, search_pattern)
            return element
        if by_type == 'name':
            element = source_element.find_element(By.TAG_NAME, search_pattern)
            return element
    except Exception as e:
        print(e)
        return False


def multiple_element_search(by_type, source_element, search_pattern):
    try:
        if by_type == 'xpath':
            element = source_element.find_elements(By.XPATH, search_pattern)
            return element
        if by_type == 'id':
            element = source_element.find_elements(By.ID, search_pattern)
            return element
        if by_type == 'name':
            element = source_element.find_elements(By.TAG_NAME, search_pattern)
            return element
    except:
        return False


def get_link_list_using_text_search(raw_block, search_pattern):
    link_list = []
    for item in raw_block:
        content = item.text.lower()
        if search_pattern in content:
            link_list.append(item.get_attribute('href'))
    return link_list


def get_links_from_container(search_type, driver, pattern):
    container = single_element_search(search_type, driver, pattern)
    if container:
        link_containers = multiple_element_search('xpath', container, './/a')
        links = [elem.get_attribute('href') for elem in link_containers]
        return links
    else:
        return None

def load_page(driver, target):
    driver.get(target)


load_page(driver, 'https://digital.nhs.uk/data-and-information/publications/statistical/nhs-workforce-statistics')

time.sleep(1)

file_links = get_links_from_container('id', driver, 'past-publications')

for link in file_links:
    print(link)
print(file_links[1])

for link in file_links:

    load_page(driver, link)

    resource_container = single_element_search('id', driver, 'resources')
    file_links = multiple_element_search('name', resource_container, 'a')

    csv_file_links = get_link_list_using_text_search(file_links, 'csv')

    base_dir = "C:\\tmp\dataStore"

    for zip_link in csv_file_links:
        filename = zip_link.split('/')[-1].replace("%20", "-")
        try:
            file_to_get = requests.get(zip_link)
            print("Download complete")

            # extract
            zip_file = zipfile.ZipFile(BytesIO(file_to_get.content))
            zip_file.extractall(base_dir)

        except Exception as e:
            print(e)
