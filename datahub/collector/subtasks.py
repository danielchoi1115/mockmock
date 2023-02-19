from naver.configs import stock_codeset
from naver.scrapers import NaverScraper
from naver.parsers import NaverParser

from ecos.configs import stat_codeset
from ecos.scrapers import EcosScraper
from ecos.parsers import EcosParser

from _global.storage import dataSender
from _global.configs import config

import time
import logging

log = logging.getLogger(__name__)


def run_naver(fake_run: bool):
    """_summary_

    Args:
        fake_run (bool, optional): When fake_run=True, it will not store anything to database. Defaults to False.
    """
    # Naver
    for code in stock_codeset:
        print(f"Scrapping {str(code)}")
        scraper = NaverScraper(**code)
        scraper.set_time_range()
        scraper.scrap()

        print("Parsing data...")
        parser = NaverParser(**code)
        parser.parse(scraper.scraped_data)

        if not parser.parsed_data:
            continue

        if fake_run:
            print("Skip storing data because fake_run=True")
            print(parser.parsed_data[:10])
        else:
            print("Sending data...")
            res = dataSender.send(
                bucket=config.influxdb.bucket.STOCK,
                data=parser.parsed_data
            )
            print(res)
        parser.clear_data()
        scraper.clear_data()
        time.sleep(2)


def run_ecos(fake_run: bool):
    for d in stat_codeset:
        print(f"Scrapping {str(d)}")
        scraper = EcosScraper(
            **d,
            auth_key=config.ecos.auth_key,
            req_start=0,
            req_end=0,
        )
        scraper.set_time_range()
        scraper.set_total_count()

        parser = EcosParser(
            **d
        )

        for data in scraper.scrap():
            print("Parsing data...")
            parser.parse(data)

            if fake_run:
                print("Skip storing data because fake_run=True")
                print(parser.parsed_data[:2], "...")
            else:
                print("Sending data...")
                res = dataSender.send(
                    bucket=config.influxdb.bucket.ECON,
                    data=parser.parsed_data
                )
                print(res)

            time.sleep(3)


def run_all(fake_run: bool = False):
    run_naver(fake_run)
    run_ecos(fake_run)
