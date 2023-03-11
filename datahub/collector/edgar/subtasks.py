from accession import AccessionScraper, AccessionParser, AccessionDto
from configs import Company


def getAccessionDto(
    company: Company,
    scraper: AccessionScraper,
    parser: AccessionParser
) -> AccessionDto:  
    scraper.setDriver()
    scraper.setUrl(company)
    scraper.scrap()
    parser.parse(
        ciks=company.ciks,
        results=scraper.results
    )

    return parser.accessionDto
