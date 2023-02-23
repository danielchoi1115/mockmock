from .accession_dto import Accession, AccessionDto
from typing import Dict, List
from pydantic import BaseModel
from datetime import datetime


class AccessionParser(BaseModel):
    accessionDto: AccessionDto = None
    date_format: str = "%Y-%m-%d"

    def initialize_adsh_list(self, ciks: str):
        self.accessionDto = AccessionDto(ciks=ciks)

    def parse(self, ciks: str, results: List[Dict]):
        self.initialize_adsh_list(ciks)
        data_to_parse = []
        key = 'hits'
        for result in results:
            if result.get(key) and result.get(key).get(key):
                data_to_parse.extend(result.get(key).get(key))

        for data in data_to_parse:
            self.accessionDto.accessions.append(
                Accession(
                    adsh=data["_source"]["adsh"],
                    reportDate=self.toDate(data["_source"]["period_ending"])
                )
            )

    def toDate(self, dateStr):
        return datetime.strptime(dateStr, self.date_format)

    class Config:
        arbitrary_types_allowed = True


accessionParser = AccessionParser()
