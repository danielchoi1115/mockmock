from accession import AccessionScrapper, AccessionParser, AccessionDto
from configs import Company


def getAccessionDto(
    company: Company,
    scrapper: AccessionScrapper,
    parser: AccessionParser
) -> AccessionDto:  
    scrapper.setDriver()
    scrapper.setUrl(company)
    scrapper.scrap()
    parser.parse(
        ciks=company.ciks,
        results=scrapper.results
    )

    return parser.accessionDto
