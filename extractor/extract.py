import os

import requests
from bs4 import BeautifulSoup
import json
from time import sleep
import random
from tqdm import tqdm
import matplotlib.pyplot as plt
from dotenv import load_dotenv

load_dotenv()


class BacStatsFetcher:
    def __init__(self):
        self.url = 'https://www.officebacniger.com/jury/statistics'
        self.headers = {
            'accept': 'text/vnd.turbo-stream.html, text/html, application/xhtml+xml',
            'accept-language': 'en-US,en;q=0.9,fr;q=0.8',
            'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'cookie': os.environ.get('COOKIE'),
            'dnt': '1',
            'origin': 'https://www.officebacniger.com',
            'priority': 'u=1, i',
            'referer': 'https://www.officebacniger.com/',
            'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
            'x-csrf-token': os.environ.get('TOKEN'),
        }

    def get_stats(self, jury_id=2628, group=1):
        payload = {
            'authenticity_token': os.environ.get('TOKEN'),
            'jury_id': str(jury_id),
            'group_synched': str(group),
            'commit': 'Voir les Statistiques'
        }

        response = requests.post(self.url, headers=self.headers, data=payload)
        return response


class DataExtractor:
    @staticmethod
    def extract_data(html_content):
        soup = BeautifulSoup(html_content, 'html.parser')

        jury = soup.find_all("div", {"id": "jury-capture"})[0]
        jury_name = jury.find("div", {"class": "md:text-xl"}).find_all("p")[1].string.split(":")[1].strip()
        jury_slug = jury_name.lower().replace(" ", "_")

        table = jury.find("table", {"id": "results-table"})
        data_results = json.loads(table.get('data-results'))

        table_rows = table.find("tbody").find_all("tr")
        table_data = []

        for row in table_rows:
            cols = row.find_all("td")
            table_data.append({
                "category": cols[0].text.strip(),
                "effectif": int(cols[1].string.strip()),
                "nb_filles_admises": int(cols[2].string.strip()),
                "nb_garcons_admis": int(cols[3].string.strip()),
                "nb_filles": int(cols[4].string.strip()),
                "nb_garcons": int(cols[5].string.strip()),
            })

        return {
            "jury": jury_name,
            "jury_slug": jury_slug,
            "chart_data": data_results,
            "table_data": table_data
        }


class StatisticsProcessor:
    def __init__(self):
        self.jury_statistics = []
        self.jury_tallies = []
        self.totals = {
            'Admis 1er groupe': 0,
            'Composent au 2nd groupe': 0,
            'Refusé(s)': 0,
            'Absents': 0
        }

    def process_jury(self, data):
        self.jury_statistics.append(data)

        for chart_entry in data['chart_data']:
            if chart_entry['label'] in self.totals:
                self.totals[chart_entry['label']] += chart_entry['value']

        tally = {
            'jury': data['jury'],
            'jury_slug': data['jury_slug'],
            'effectif': 0,
            'nb_filles_admises': 0,
            'nb_garcons_admis': 0,
            'nb_filles': 0,
            'nb_garcons': 0
        }

        for table_entry in data['table_data']:
            for key in ['effectif', 'nb_filles_admises', 'nb_garcons_admis', 'nb_filles', 'nb_garcons']:
                tally[key] += table_entry[key]

        self.jury_tallies.append(tally)

    def save_results(self):
        with open('stats_final.json', 'w') as json_file:
            json.dump(self.jury_statistics, json_file, indent=2)

        with open('tallies.json', 'w') as json_file:
            json.dump(self.jury_tallies, json_file, indent=2)


class DataVisualizer:
    @staticmethod
    def plot_pie_chart(totals):
        categories = list(totals.keys())
        values = list(totals.values())

        plt.figure(figsize=(8, 8))

        def func(pct, allvalues):
            absolute = int(pct / 100. * sum(allvalues))
            return f"{pct:.1f}%\n({absolute})"

        plt.pie(values, labels=categories, autopct=lambda pct: func(pct, values), startangle=140,
                colors=['skyblue', 'lightgreen', 'salmon', 'gold'])
        plt.title('bac 2024')
        plt.axis('equal')
        plt.show()


def main():
    fetcher = BacStatsFetcher()
    processor = StatisticsProcessor()

    with open('juries.json', 'r') as f:
        all_jurys = json.load(f)

    for jury in tqdm(all_jurys):
        try:
            stats = fetcher.get_stats(jury['value'])
            data = DataExtractor.extract_data(stats.text)
            processor.process_jury(data)

            with open('stats.json', 'a') as append_file:
                json.dump(data, append_file)
                append_file.write(',\n')
        except Exception as e:
            print(f'Could not get data for jury {jury["label"]} ({jury["value"]}): {e}')
        sleep(random.choice(range(4)))

    processor.save_results()
    print('Statistics appended to juries.json')

    DataVisualizer.plot_pie_chart(processor.totals)


if __name__ == "__main__":
    main()
