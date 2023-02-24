from accession import accessionScrapper, accessionParser
from report import reportScrapper, parsers, reportValidator
from configs import config
from subtasks import getAccessionDto
from accession import Accession
from datetime import datetime
# https://formthirteen.com/blog/3

if __name__ == "__main__":

    # for company in config.companies:
    #     accessionDto = getAccessionDto(
    #         company=company,
    #         scrapper=accessionScrapper,
    #         parser=accessionParser
    #     )
    #     with open('reportTest.txt', "w") as f:
    #         f.write(str(accessionDto.dict()))

    # reportScrapper.scrap(accessionDto=accessionDto)

    # with open('reportTest.txt', "w") as f:
    #     f.write(str(reportScrapper.scraped_data))

    with open("/home/sychoi/mockmock/datahub/collector/edgar/report/0001037389-23-000119.txt", 'r') as f:
        reportRaw = f.read()

    # acc = Accession(
    #     adsh="0001037389-01-500011",
    #     reportDate=datetime(2000, 3, 31, 0, 0)
    # )
    acc = Accession(
        adsh="0001037389-23-000119",
        reportDate=datetime(2022, 12, 31)
    )
    reportParser = parsers.ReportParserFactory.getParserOf(reportRaw=reportRaw, accesion=acc)

    reportParser.parse()
    reportParser.postProcess()
    print(reportParser.parsedData)
    # reportValidator.validateParsedData(reportParser)

    # with open("pandas2.txt", 'w') as f:
    #     f.write(reportParser.parsedData.to_csv())


