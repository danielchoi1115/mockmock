from configs import corp_code
from scrapers import DartScraper
from parsers import DartParser
from storage import sender
import time



for code in corp_code:
    print(f"Scrapping {str(code)}")
    scraper = DartScraper(**code)
    scraper.set_time_range()
    scraped_data = scraper.scrap()

    print("Parsing data...")
    parser = DartParser(**code)
    parser.parse(scraped_data)

    if not parser.parsed_data:
        print("no item found")
        continue

    with open("sam.txt", "w") as f:
        f.write(str(parser.parsed_data))
    print("Sending data...")
    res = sender.send(parser.parsed_data)
    print(res)
    parser.clear_data()
    scraper.clear_data()
    time.sleep(10)
