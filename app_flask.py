import requests
from flask import Flask
from bs4 import BeautifulSoup
import json

app = Flask(__name__)


@app.route('/', methods=['GET'])
def parse():
    url = 'https://www.nbrb.by/engl/statistics/rates/ratesdaily.asp'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    currency = soup.find_all('span', class_='text')
    amount = soup.find_all('td', class_='curAmount')
    cours = soup.find_all('td', class_='curCours')

    data_currency = []
    data_amount = []
    data_cours = []

    for i in range(0, len(currency)):
        data_currency.append(currency[i].text)

    for i in range(0, len(amount)):
        data_amount.append(amount[i].text)

    for i in range(0, len(cours)):
        data_cours.append(cours[i].text.strip() + ' BYN')

    data = {}

    for i in range(0, len(data_cours)):
        data.setdefault(data_currency[i], []).append({'Amount': data_amount[i]})
        data.setdefault(data_currency[i], []).append({'Cours': data_cours[i]})

    output = json.dumps(data, ensure_ascii=False, indent=4)

    with open('data.json', 'w') as f:
        json.dump(data, f)

    return f"<pre>{output}</pre>"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
