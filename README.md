# Web-Scrapping-Spotify-Chart
This program scrap spotify weekly top songs global from [here](https://quotes.toscrape.com)

## Installation
1. Clone this repository
```
  git clone https://github.com/revaldyazura/scrap-web-py
```
2. Open in terminal and install the packages:
``` 
  pip install -r requirements.txt
```
3. Prepare the MySQL database:
    - Make a new database called `spotify_scrapping`.
    - Then Import `songs.sql` pada database `spotify_scrapping`.
    - Update detail database connection inside `app.py` (host, user, password).

## Usage

1. Run the python file:
```
  py app.py
```
  This command will start the program, and you'll see the charts on this link `http://127.0.0.1:5000/charts`.

## Notes

- This program built and run on Python 3.12
- Make sure your MySQL server running before you start this program.
- Make sure your chromedriver compatible with your chrome.

