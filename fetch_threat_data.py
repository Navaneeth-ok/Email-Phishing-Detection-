
#fetch_threat_data.py

import requests
import sqlite3

def get_phishtank_data():
    url = 'http://data.phishtank.com/data/online-valid.json'
    response = requests.get(url)
    if response.status_code == 200:
         return response.json()
    else:
         raise Exception('Failed to fetch data from Phishtank')


def store_phishtank_data(data):
    conn = sqlite3.connect('threat_intel.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS phishing_urls (url TEXT)''')

    for entry in data:
        c.execute("INSERT INTO  phishing_urls (url) VALUES (?)", (entry['url'],))

    conn.commit()
    conn.close()

phishtank_data = get_phishtank_data()
store_phishtank_data(phishtank_data)
