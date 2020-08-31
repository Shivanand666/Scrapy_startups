

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')  # Last I checked this was necessary.
# driver = webdriver.Chrome(r'E:\Web_scrap\billboard\billboard\spiders\chromedriver.exe', chrome_options=options)
driver = webdriver.Chrome(r'E:\Web_scrap\billboard\billboard\spiders\chromedriver.exe')





no_of_company =250
def get_company_link_from_table(companies):
  company_links =[]
  for index,company in enumerate(companies):
    if index != 0:
      link = company.find_all('a',attrs={'class':'startuplink'})
      if len(link) == 1:
        #print(link[0])
        company_links.append(link[0].get('href'))
  
  return company_links

# driver = webdriver.Chrome(ChromeDriverManager().install())
# driver = webdriver.Chrome()

url = 'https://e27.co/startups/'
driver.get(url)
time.sleep(20)
current_company_no=0
print('fetching company links')
while (current_company_no < no_of_company):
    time.sleep(20)
    driver.find_element_by_xpath("//span[contains(text(),'Load more')]").click()
    html3 = driver.execute_script("return document.documentElement.outerHTML")
    
    # print(html3)
    sel_soup3 = BeautifulSoup(html3,'html.parser')
    gdp_table3 = sel_soup3.find("table", attrs={"class": "table"})
    gdp_table_data3 = gdp_table3.tbody.find_all("tr")
    current_company_no = len(gdp_table_data3)
    print(current_company_no)
print('company links fetched')
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
html = driver.execute_script("return document.documentElement.outerHTML")
sel_soup = BeautifulSoup(html,'html.parser')
gdp_table = sel_soup.find("table", attrs={"class": "table"})
gdp_table_data = gdp_table.tbody.find_all("tr")
# print("---------------------------------------------------------------")
# print(gdp_table_data)
company_links = get_company_link_from_table(gdp_table_data)
# print(company_links)
company_links = company_links[:no_of_company]
data=pd.DataFrame(company_links)
data.to_csv('URLS.csv')
# print(company_links)

time.sleep(20)
comp_data=pd.read_csv('URLS.csv')
company_links=list(comp_data['0'].values)
print(company_links)
all_company_data =[]
print('fetching individual company data')
for company in company_links:
    print('company',company)
    driver.get(company)
    time.sleep(1)
    company_details = driver.execute_script("return document.documentElement.outerHTML")
    # print(company_details)

    company_details_bs4 = BeautifulSoup(company_details,'html.parser')
    # print(company_details_bs4)

    data = {}
    
    Comp_Name = company_details_bs4.find('strong',attrs={'class':'startup-name'}).text
    e27_url=company
    Comp_Short_Descr= company_details_bs4.find('h2',attrs={'class':'startup-short-description'}).text
    Comp_Long_descr = company_details_bs4.find('p',attrs={'class':'profile-desc-text startup-description'}).text
    Comp_website = company_details_bs4.find_all('a',attrs={'class':'startup-website'})[0].get('href')
    Comp_Location = company_details_bs4.find('span',attrs={'class':'startup-startup_location'}).text
    Comp_founded = company_details_bs4.find('p',attrs={'class':'startup-date-founded'}).text
    founders=[]
    team_members= company_details_bs4.find('div',attrs={'class':'row team teammembers-container teammembers-parent-active teammember-parent-node'})
    # print('team_members',team_members)
    if (team_members) !=None:
      if len(team_members) != 0:
        for a in team_members:
          ff = a.find_all_next('a',attrs={'class':'teammember-name'})
          for i in ff:
            if len(i.text) >0:
              founders.append(i.text)
    CEO= ','.join(founders)


    tag_list=[]
    tag = company_details_bs4.find('p',attrs={'class':'startup-startup_market'}).find_all('a')
    for a in tag:
        tag_list.append(a.text)
    Tags= ' '.join(tag_list)
    Phone=''
    Email=''
    Emp_range=''


    company_data = {
    'Company Name':Comp_Name,
    'e27_url' :e27_url,
    'Short_description':Comp_Short_Descr,
    'Long_description':Comp_Long_descr,
    'Company website':Comp_website,
    'Location':Comp_Location,
    'Founded Date':Comp_founded,
    'CEO':CEO,
    'Tags':Tags,
    'Phone':Phone,
    'Email':Email,
    'Emp_range':Emp_range,

    }
    all_company_data.append(company_data)
# print(all_company_data)
dataframe = pd.DataFrame(all_company_data)
dataframe.to_csv('companydata.csv')

print('check current directory file is saved with name companydata.csv')
driver.close()
