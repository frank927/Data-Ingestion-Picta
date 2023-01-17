from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import sleep
from PictaSQLITE import*
import re

documentales=[]
linklist=[]
CommentsList=[]
filtro=[]

path='C:\webdriver\chromedriver.exe'
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))


url='https://www.picta.cu/categoria/Documental'

driver.get(url)
sleep(1)   
driver.maximize_window()




soup = BeautifulSoup(driver.page_source, 'html.parser')

video = soup.find_all('mat-card', {'class':'mat-card mat-focus-indicator p-0 ng-star-inserted'})

for link in video:
      url=link.find('a')['href']
      documentales.append(url)
     

pos=0

def getComments():
      WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH,"//span[@class='mat-title']")))
      soup = BeautifulSoup(driver.page_source, 'html.parser')

      count = soup.find('span', {'class':'mat-title'}).text

      new=int(count.replace(' hasta el momento',''))
      
      if(new>10):    
           previous_offset = -1
           x=250
           current_offset = driver.execute_script('return window.pageYOffset;')
           while previous_offset!=current_offset:
               previous_offset = current_offset
               driver.execute_script(f"window.scrollTo(0,{x});")
               sleep(3)
               current_offset = driver.execute_script('return window.pageYOffset;')
               x=x+250
    
      soup = BeautifulSoup(driver.page_source, 'html.parser')

      commets = soup.find_all('div', {'class':'d-flex flex-row ng-star-inserted'})

      for c in commets:
         data=c.find('h5', {'class':'post-video-data mt-3'}).text
         CommentsList.append(data)
     
     
      if(CommentsList):
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        day = soup.find('h3', {'class':'post-video-data ng-star-inserted'}).text

        replace=day.replace('Publicado el ','')

        for i in CommentsList:
            emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
            filtro.append(emoji_pattern.sub(r'', i))      
        cursor.execute("INSERT OR REPLACE INTO Comments VALUES(?,?,?,?,?)", (str('https://www.picta.cu')+str(linklist[pos]),str(filtro), str(len(filtro)),('Documentales'),str(replace)))
        connection.commit()
     
for m in documentales:
      WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, f"//a[starts-with(@href,'{m}')]"))).click()
      sleep(3)
      link = m.replace("documental", "medias")
      linklist.append(link)
      WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, f"//a[starts-with(@href,'{link}')]"))).click()
      sleep(3)
      getComments()
      sleep(2)
      pos+=1
      CommentsList.clear()
      filtro.clear()
      driver.back()
      sleep(3)
      driver.back()
      sleep(3)


driver.quit()


