from bs4 import BeautifulSoup
import requests
import pprint


URL = 'https://www.oddsshark.com/stats/gamelog/basketball/nba/20722/2019'
page = requests.get(URL)

soup = BeautifulSoup(page.content,'html.parser')


results = soup.find(id='ResultsContainer')
job_elems = results.find_all('section',class_ = 'card-content')

'''
for job_elem in job_elems:
    title_elem = job_elem.find('h2',class_='title')
    company_elem = job_elem.find('div',class_ = 'company')
    location_elem = job_elem.find('div',class_='location')
    if None in (title_elem,company_elem,location_elem):
        continue
    print(title_elem.text.strip())
    print(company_elem.text.strip())
    print(location_elem.text.strip())
    print()
'''