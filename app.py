from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from urllib.request import urlopen
from flask import Flask, render_template
from mysql.connector import connect
from selenium.webdriver.chrome.service import Service as ChromeService
import re

app = Flask(__name__)

mySqlConnect=connect(
  host='localhost',
  port=3306,
  user='root',
  password='',
  database='spotify_scrapping'
)

def insert(title, rank, artist, linkOpen):
  cursor = mySqlConnect.cursor()
  try:
    cursor.execute(f'INSERT INTO `songs` (`title`, `rank`, `artist`, `link`) VALUES ("{title}","{rank}","{artist}","{linkOpen}")')
    mySqlConnect.commit()
  except Exception as err:
    mySqlConnect.rollback()
    print(err)
  finally:
    cursor.close()

def check(title, rank, artist, linkOpen):
  cursor = mySqlConnect.cursor()
  try:
    cursor.execute(f'SELECT * FROM `songs` WHERE `title` = "{title}" AND `rank` = "{rank}" AND `artist` = "{artist}" AND `link` = "{linkOpen}"')
    fetched = cursor.fetchone()
    return fetched is not None
  except Exception as err:
    print(err)
  finally:
    cursor.close()
    
def update(id, title, rank, artist, linkOpen):
  cursor = mySqlConnect.cursor()
  try:
    cursor.execute(f'UPDATE `songs` SET `title` = "{title}", `rank` = "{rank}", `artist` = "{artist}", `link` = "{linkOpen}" WHERE `id` = {id}')
    mySqlConnect.commit()
  except Exception as err:
    mySqlConnect.rollback()
    print(err)
  finally:
    cursor.close()

def getWeeklyTopSongs():
  link = 'https://charts.spotify.com/home'
  chromeDriver = ChromeService(executable_path='./browser/chromedriver.exe')
  driver = webdriver.Chrome(service=chromeDriver)
  driver.get((link))
  driver.implicitly_wait(30)
  
  soup = BeautifulSoup(driver.page_source, "html.parser")
  songs = []
  
  weekElement = soup.select_one('h3.encore-text.encore-text-body-medium.encore-internal-color-text-subdued.ChartsHomeSubtitle-sc-1ddoroh-0')
  week = weekElement.text
  
  for id, song in enumerate(soup.select('li.ChartsHomeEntries__ChartEntryItem-kmpj2i-1'), start=1):
    titleElement = song.find('p')
    rankElement = song.select_one('div span.encore-text')
    artistElement = song.select('div.ChartsHomeEntries__Title-kmpj2i-2 span a.ChartsHomeEntries__StyledHyperlink-kmpj2i-4')
    linkElement = song.select_one('a[href]')
    
    if titleElement and rankElement and artistElement and linkElement:
      title = titleElement.text
      artist = ', '.join([artist.text for artist in artistElement])
      linkOpen = linkElement.get('href')
      rank = rankElement.text if rankElement else "N/A"
      
      songs.append({
        'title': title,
        'rank': rank,
        'artist': artist,
        'link': linkOpen
      })
      
      if check(title, rank, artist, linkOpen):
        update(id, title, rank, artist, linkOpen)
      else:
        insert(title, rank, artist, linkOpen)
      
  driver.quit()
  
  return week, songs

@app.route('/charts', methods=['GET'])
def getCharts():
  week, songs = getWeeklyTopSongs()
  
  return render_template('index.html', topSongs = songs, week=week)

if __name__ == '__main__':
  app.run(debug=True)