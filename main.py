import json
import random
from time import sleep

from tqdm import tqdm
from extractor.extract import BacStatsFetcher, StatisticsProcessor, DataExtractor, DataVisualizer


def main():
    fetcher = BacStatsFetcher()
    processor = StatisticsProcessor()

    with open('extractor/juries.json', 'r') as f:
        all_jurys = json.load(f)

    for jury in tqdm(all_jurys):
        try:
            stats = fetcher.get_stats(jury['value'])
            data = DataExtractor.extract_data(stats.text)
            processor.process_jury(data)

            with open('stats.json', 'a') as append_file: # save just in case
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
