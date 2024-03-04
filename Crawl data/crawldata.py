from selenium import webdriver
from selenium.webdriver.common.by import By
import bs4
import requests
import numpy as np
import pandas as pd
import time

def getLink(link):
    output = ""
    for char in link:
        if char == '#':
            break
        output += char
    return output

def get_page_content(url):
   page = requests.get(url,headers={"Accept-Language":"en-US"})
   return bs4.BeautifulSoup(page.text,"html.parser")

def crawlDataChoTot(url):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(1)
    
    rawData = pd.DataFrame()

    # get link job
    els_links = driver.find_elements(By.CSS_SELECTOR, ".AdItem_wrapperAdItem__S6qPH  [href]")
    links = [getLink(i.get_attribute('href')) for i in els_links]

    #get title 
    els_titles = driver.find_elements(By.CSS_SELECTOR, '.AdItem_wrapperAdItem__S6qPH  .commonStyle_adTitle__g520j   ')
    title = [i.text for i in els_titles]    

    #get priceNormal
    els_prices = driver.find_elements(By.CSS_SELECTOR, '.AdItem_wrapperAdItem__S6qPH  .AdTitle_adPriceNormal__4ujtc   ')
    priceNormal = [i.text for i in els_prices]

    #get company name, location
    els_cp_name = driver.find_elements(By.CSS_SELECTOR, '.AdItem_wrapperAdItem__S6qPH  .AdBody_wrapperFooter__2hsfm')
    companyName = [i.text.split('\n')[0] for i in els_cp_name]
    els_location = driver.find_elements(By.CSS_SELECTOR, '.AdItem_wrapperAdItem__S6qPH  .AdBody_locationName__z_Sy6')
    location = [i.text.split('\n')[1] for i in els_cp_name]

    #get type of company
    typeCompany = []
    els_type_company = driver.find_elements(By.CSS_SELECTOR, '.AdItem_wrapperAdItem__S6qPH  .AdBody_wrapperFooter__2hsfm  .commonStyle_image__6q98n ')
    for type_company in els_type_company:
        if(type_company.get_attribute('src') == "https://static.chotot.com/storage/icons/owner/conpany.svg"):
            typeCompany.append('Công ty')
        else: typeCompany.append('Cá nhân')
    #get 
    decription = []
    salaryType = []
    contractType = []
    jobType = []
    experience = []
    gender = []
    vacacies = []
    education = []
    minAge = []
    maxAge = []
    benefit = []
    skill = []

    for link in links:
        soup = get_page_content(link)
        decription.append(soup.find('p', {'class':'AdDecription_adBody__qp2KG'}).text)
        salaryType.append(soup.find('span', {'itemprop':'salary_type'}).text)
        contractType.append(soup.find('span', {'itemprop':'contract_type'}).text)
        jobType.append(soup.find('span', {'itemprop':'job_type'}).text)
        if(soup.find('span', {'itemprop':'preferred_working_experience'}) is not None):
            experience.append(soup.find('span', {'itemprop':'preferred_working_experience'}).text)
        else: experience.append(np.nan)
        gender.append(soup.find('span', {'itemprop':'preferred_gender'}).text)
        vacacies.append(soup.find('span', {'itemprop':'vacancies'}).text)
        if(soup.find('span', {'itemprop':'preferred_education'}) is not None):
            education.append(soup.find('span', {'itemprop':'preferred_education'}).text)
        else: education.append(np.nan)
        if (soup.find('span', {'itemprop':'benefit'}) is not None):
            benefit.append(soup.find('span', {'itemprop':'benefit'}).text)
        else: benefit.append(np.nan)    
        if (soup.find('span', {'itemprop':'skills'}) is not None):
            skill.append(soup.find('span', {'itemprop':'skills'}).text)
        else: skill.append(np.nan)    
        minAge.append(soup.find('span', {'itemprop':'min_age'}).text)
        if (soup.find('span', {'itemprop':'max_age'}) is not None):
            maxAge.append(soup.find('span', {'itemprop':'max_age'}).text)
        else: maxAge.append(np.nan)

    rawData['link'] = links
    rawData['title'] = title
    rawData['priceNormal'] = priceNormal
    rawData['companyName'] = companyName
    rawData['location'] = location
    rawData['companyType'] = typeCompany
    rawData['decription'] = decription
    rawData['salaryType'] = salaryType
    rawData['contractType'] = contractType
    rawData['jobType'] = jobType
    rawData['experience'] = experience
    rawData['gender'] = gender
    rawData['vacacies'] = vacacies
    rawData['education'] = education
    rawData['minAge'] = minAge
    rawData['maxAge'] = maxAge
    rawData['benefit'] = benefit
    rawData['skill'] = skill
    rawData = pd.DataFrame(rawData)
    driver.quit()

    return rawData

# links = pd.read_csv('note.csv')
data = pd.DataFrame()
# add_link = ['', '?page=2', '?page=3', '?page=4', '?page=5', '?page=6', '?page=7', '?page=8', '?page=9', '?page=10']
add_link = ['', '?page=2', '?page=3', '?page=4', '?page=5', '?page=6', '?page=7', '?page=8', '?page=9', '?page=10']

# for link in links['links']:
#     for add in add_link:
#         page = crawlDataChoTot(link+add)
#         data = pd.concat([data, page], axis=0)

# data.to_csv('data_cho_tot.csv')

# Cào dữ liệu đối tác 
link = 'https://www.vieclamtot.com/viec-lam?f=shop_entitlement&f=protection_entitlement'
for i in range(21, 29):
    page = crawlDataChoTot(link+'?page='+str(i))
    data = pd.concat([data, page], axis=0)

data.to_csv('data_cho_tot_(doi_tac3).csv')



