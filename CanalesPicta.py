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

path='C:\webdriver\chromedriver.exe'
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

ListCh=[]
linklist=[]
CommentsList=[]
filtro=[]
pos=0

url='https://www.picta.cu/canal-list'

driver.get(url)
sleep(1)   
driver.maximize_window()
sleep(2)

def getUrlsChannel():
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    video = soup.find_all('mat-card', {'class':'mat-card mat-focus-indicator p-0 ng-star-inserted'})
     
    for link in video:
        url=link.find('a')['href']
        ListCh.append(url)
    
def getUrlsVideo():
    
    sleep(2)  
    page=WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, 'html')))
    page.send_keys(Keys.END)
    sleep(1)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    video = soup.find_all('div', {'class':'video-card ng-star-inserted'})

    for link in video:
        url=link.find('a', {'class':'play-img'})['href']
        linklist.append(url)
   
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
        cursor.execute("INSERT OR REPLACE INTO Comments VALUES(?,?,?,?,?)", (str('https://www.picta.cu')+str(linklist[pos]),str(filtro), str(len(filtro)),('Canales'),str(replace)))
        connection.commit()
     
getUrlsChannel()
sleep(3)
    
for i in ListCh:
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, f"""//a[starts-with(@href,"{i}")]"""))).click()
    sleep(5)
    getUrlsVideo()
    for y in linklist:
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, f"//a[starts-with(@href,'{y}')]"))).click()
            sleep(5)
            getComments()
            sleep(2)
            pos+=1
            CommentsList.clear()
            filtro.clear()
            driver.back()
            sleep(5)         
    driver.back() 
    linklist.clear()
    pos=0
    sleep(5)  

            
driver.quit()   

 