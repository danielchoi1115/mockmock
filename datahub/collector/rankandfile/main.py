from requests.sessions import Session
from requests.adapters import HTTPAdapter, Retry, MaxRetryError
import logging
from datetime import datetime 
logging.basicConfig(
        filename='error.log',
        encoding='utf-8',
        level=logging.WARNING,
        format='%(asctime)s:%(levelname)s:%(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )
log = logging.getLogger(__name__)

# http://rankandfiled.com/#/data/tickers

SAVE_PATH = '/home/sychoi/mockmock/datahub/collector/rankandfile/cik_list.csv'

def run(url: str, method: str = 'get'):
    with Session() as session:
        connect = 10
        read = 0
        backoff_factor = 0.3
        RETRY_AFTER_STATUS_CODES = (429, 500)

        retry = Retry(
            total=(connect + read),
            connect=connect,
            read=read,
            backoff_factor=backoff_factor,
            status_forcelist=RETRY_AFTER_STATUS_CODES,
        )

        adapter = HTTPAdapter(max_retries=retry)
        # http:// 로 시작하면 adapter 내용을 적용
        session.mount("http://", adapter)
        # https:// 로 시작하면 adapter 내용을 적용
        session.mount("https://", adapter)
        
        try:
            session.request(method=method, url=url)
            res = session.get(url=url)
        except MaxRetryError:
            log.warning(f"Request failed. url: {url}")
            return False, []
        
        print(f"{datetime.now()}: status: {res.status_code} - {url.split('?')[1]}")
        return True, res.json()['list']
        
def main():
    offset = 0
    step = 101
    retryList = []

    while offset < 20000:
        url = f"http://rankandfiled.com//data/identifiers?start={offset}"
        result, data = run(url)
        if not result:
            retryList.append(offset)
        elif not data:
            break
        else:
            with open(SAVE_PATH, "a", encoding='utf8') as f:
                f.write("\n".join(data)+"\n")
        offset += step

    log.info(f"Retry List: {retryList}")
if __name__ == "__main__":
    main()